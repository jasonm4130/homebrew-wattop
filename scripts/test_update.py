import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from update import generate


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.previous = Path.cwd()
        os.chdir(self.directory.name)
        self.addCleanup(self.directory.cleanup)
        self.addCleanup(os.chdir, self.previous)
        self.release = {"tag_name": "v0.1.0", "draft": False, "prerelease": False}

    def download(self, args, **kwargs):
        if args[1:3] == ["release", "download"]:
            root = Path(args[args.index("--dir") + 1])
            (root / "wattop_0.1.0_darwin_arm64.tar.gz").write_bytes(b"test archive")
            digest = hashlib.sha256(b"test archive").hexdigest()
            (root / "checksums.txt").write_text(f"{digest}  wattop_0.1.0_darwin_arm64.tar.gz\n")

    def test_verified_release_generates_pinned_cask(self):
        with patch("update.subprocess.check_output", return_value=json.dumps(self.release)), \
             patch("update.subprocess.run", side_effect=self.download) as run:
            generate()
        cask = Path("Casks/wattop.rb").read_text()
        self.assertIn('version "0.1.0"', cask)
        self.assertIn(hashlib.sha256(b"test archive").hexdigest(), cask)
        verification = run.call_args_list[-1].args[0]
        self.assertEqual(verification[1:3], ["attestation", "verify"])
        self.assertIn("refs/tags/v0.1.0", verification)

    def test_rejects_untrusted_release_without_writing(self):
        for change in ({"tag_name": 'v0.1.0"; system("bad")'}, {"prerelease": True}, {"draft": True}):
            with self.subTest(change=change), \
                 patch("update.subprocess.check_output", return_value=json.dumps(self.release | change)):
                with self.assertRaises(ValueError):
                    generate()
                self.assertFalse(Path("Casks/wattop.rb").exists())

    def test_bad_checksum_preserves_existing_cask(self):
        Path("Casks").mkdir()
        Path("Casks/wattop.rb").write_text("existing")
        def corrupt(args, **kwargs):
            self.download(args, **kwargs)
            root = Path(args[args.index("--dir") + 1])
            (root / "wattop_0.1.0_darwin_arm64.tar.gz").write_bytes(b"corrupt")
        with patch("update.subprocess.check_output", return_value=json.dumps(self.release)), \
             patch("update.subprocess.run", side_effect=corrupt):
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                generate()
        self.assertEqual(Path("Casks/wattop.rb").read_text(), "existing")

    def test_failed_attestation_does_not_publish(self):
        def reject(args, **kwargs):
            self.download(args, **kwargs)
            if args[1:3] == ["attestation", "verify"]:
                raise subprocess.CalledProcessError(1, args)
        with patch("update.subprocess.check_output", return_value=json.dumps(self.release)), \
             patch("update.subprocess.run", side_effect=reject):
            with self.assertRaises(subprocess.CalledProcessError):
                generate()
        self.assertFalse(Path("Casks/wattop.rb").exists())


if __name__ == "__main__":
    unittest.main()

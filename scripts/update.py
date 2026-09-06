#!/usr/bin/env python3
"""Generate the cask from a stable release after checksum/provenance validation."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

REPO = "jasonm4130/wattop"


def generate():
    release = json.loads(subprocess.check_output(["gh", "api", f"repos/{REPO}/releases/latest"]))
    tag = release["tag_name"]
    if release["draft"] or release["prerelease"] or not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError(f"Expected a stable version tag, got {tag!r}")
    version = tag[1:]
    archive = f"wattop_{version}_darwin_arm64.tar.gz"
    with tempfile.TemporaryDirectory(prefix="wattop-release-") as directory:
        subprocess.run(["gh", "release", "download", tag, "--repo", REPO,
                        "--pattern", archive, "--pattern", "checksums.txt", "--dir", directory], check=True)
        root = Path(directory)
        hashes = {}
        for line in (root / "checksums.txt").read_text().splitlines():
            digest, filename = line.split(maxsplit=1)
            hashes[filename.lstrip("*")] = digest
        expected = hashes[archive]
        if not re.fullmatch(r"[a-f0-9]{64}", expected):
            raise ValueError("Invalid release checksum")
        actual = hashlib.sha256((root / archive).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError("Release archive checksum mismatch")
        subprocess.run(["gh", "attestation", "verify", str(root / archive), "--repo", REPO,
                        "--signer-workflow", f"{REPO}/.github/workflows/release.yml",
                        "--source-ref", f"refs/tags/{tag}"], check=True)
    cask = f'''cask "wattop" do
  version "{version}"
  sha256 "{expected}"

  url "https://github.com/{REPO}/releases/download/v#{{version}}/wattop_#{{version}}_darwin_arm64.tar.gz"
  name "wattop"
  desc "Apple Silicon hardware and coding-agent activity monitor"
  homepage "https://github.com/{REPO}"

  depends_on arch: :arm64
  depends_on macos: :sonoma

  binary "wattop"

  # The release is not Apple-notarized. Permit this verified CLI to run.
  postflight do
    system_command "/usr/bin/xattr",
                   args: ["-dr", "com.apple.quarantine", "#{{staged_path}}/wattop"],
                   must_succeed: true
  end
end
'''
    Path("Casks").mkdir(exist_ok=True)
    Path("Casks/wattop.rb").write_text(cask)
    print(f"Generated wattop {version}; verified SHA256 {expected}")


if __name__ == "__main__":
    generate()

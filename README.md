# Homebrew tap for wattop

Install [wattop](https://github.com/jasonm4130/wattop), a terminal dashboard for
Apple Silicon hardware and Claude Code / Codex activity.

```sh
brew install --cask jasonm4130/wattop/wattop
wattop
```

Requires Apple Silicon and macOS 14 or newer. Hardware readings depend on the
chip and macOS version; see wattop's documented limitations. The binary is not
Apple-notarized. GitHub release provenance and SHA256 checksums identify its build.
The cask removes the quarantine attribute from its installed `wattop` binary
so macOS can execute this unsigned CLI.

## Update

```sh
brew update
brew upgrade --cask wattop
```

The tap checks stable wattop releases hourly. Before publishing a cask update,
its workflow verifies the archive checksum and GitHub build provenance, then
installs and runs the binary on an Apple Silicon runner. Scheduled jobs can
be delayed; maintainers can run the **update** workflow manually after a release.
Prereleases are excluded. No personal access token is required.

GitHub may disable scheduled workflows in public repositories after 60 days
without activity. If updates stop, enable the workflow and run it manually.

## Maintainers

Run `gh workflow run update.yml --repo jasonm4130/homebrew-wattop` after publishing
a stable wattop release. Inspect its result before announcing Homebrew availability.
To generate the cask locally, authenticate `gh` and run `python3 scripts/update.py`.
Commit only after testing `brew install --cask jasonm4130/wattop/wattop`.

Report dashboard bugs in [wattop](https://github.com/jasonm4130/wattop/issues).
Report packaging bugs in this repository. The tap is MIT licensed; wattop's
release archive includes its license and third-party notices.

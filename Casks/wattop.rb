cask "wattop" do
  version "0.2.0"
  sha256 "7c1d9d974335a02dd624e998bee8aaf9fdd9cd4d1a8a731759a5cc68a1f7cdaa"

  url "https://github.com/jasonm4130/wattop/releases/download/v#{version}/wattop_#{version}_darwin_arm64.tar.gz"
  name "wattop"
  desc "Apple Silicon hardware and coding-agent activity monitor"
  homepage "https://github.com/jasonm4130/wattop"

  depends_on arch: :arm64
  depends_on macos: :sonoma

  binary "wattop"

  # The release is not Apple-notarized. Permit this verified CLI to run.
  postflight do
    system_command "/usr/bin/xattr",
                   args: ["-dr", "com.apple.quarantine", "#{staged_path}/wattop"],
                   must_succeed: true
  end
end

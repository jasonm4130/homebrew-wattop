cask "wattop" do
  version "0.3.0"
  sha256 "a9068757ea0e8df0218cc916b5f7b92177f9a41fb4a4294d4a6468f98330ac3a"

  url "https://github.com/jasonm4130/wattop/releases/download/v#{version}/wattop_#{version}_darwin_arm64.tar.gz"
  name "wattop"
  desc "Apple Silicon hardware and coding-agent activity monitor"
  homepage "https://github.com/jasonm4130/wattop"

  depends_on arch: :arm64
  depends_on macos: :sonoma

  binary "wattop"

  # The release is not Apple-notarized. Permit this verified CLI to run.
  postflight_steps do
    run "/usr/bin/xattr",
        args: ["-dr", "com.apple.quarantine", "{{staged_path}}/wattop"]
  end
end

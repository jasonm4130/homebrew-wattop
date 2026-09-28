cask "wattop" do
  version "0.3.1"
  sha256 "8174a6797a19b451b331c65409085721f87f042e17706be452fb5dfa3fd855ba"

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

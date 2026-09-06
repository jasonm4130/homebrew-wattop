cask "wattop" do
  version "0.1.0"
  sha256 "0fb71ea3a5d7218f7ae7b9ff25c4ba9b91a3bee5f58ec04cc6753bd4471aa617"

  url "https://github.com/jasonm4130/wattop/releases/download/v#{version}/wattop_#{version}_darwin_arm64.tar.gz"
  name "wattop"
  desc "Apple Silicon hardware and coding-agent activity monitor"
  homepage "https://github.com/jasonm4130/wattop"

  depends_on arch: :arm64
  depends_on macos: ">= :sonoma"

  binary "wattop"
end

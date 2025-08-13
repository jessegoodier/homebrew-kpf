class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/09/f8/bef2bb1162b92ac0c86ca459f899ee82d6726d01da15a90026457ab546c3/kpf-0.1.20.tar.gz"
  sha256 "76af9ce91110c2437b328fe2df7972a6517e2c6a28e6f5de606f4a0ce030b471"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_create(libexec, "python3.12")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "kpf==0.1.20"
    
    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")
    
    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf 0.1.20", version_output
  end
end
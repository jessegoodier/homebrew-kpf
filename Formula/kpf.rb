class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/f8/37/97874fac5a0beb4a2f06bc2d07a7a6cc05f0c0e3b7b788699a7de50cccf6/kpf-0.2.0.tar.gz"
  sha256 "4fe450d2f8bb6f58fd9f1d82047b1e9e7b7ad63f6ec059a3ef1a64cf21accdb7"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_create(libexec, "python3.12")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "kpf==0.2.0"
    
    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")
    
    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf 0.2.0", version_output
  end
end
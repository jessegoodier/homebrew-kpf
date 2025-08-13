class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/a5/84/fa3bd843f44425cec76f4144743c11fe6b6e27e6fc6d4d735d280ce1e2d5/kpf-0.1.19.tar.gz"
  sha256 "71c2421e66cc0615ffd9fade160e195cd4ab5f1b0abaf91da55ef8a97ea8d383"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_create(libexec, "python3.12")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "kpf==0.1.19"
    
    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")
    
    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf 0.1.19", version_output
  end
end
class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/20/8c/838c77ea4d0c22e94a45a33bfb1e984e5272c1a87702de328c878ca477a2/kpf-0.1.12.tar.gz"
  sha256 "47078648f86460289e41c90bb729cb36b1aae875a518e535277e7c39eb78a3de"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_create(libexec, "python3.12")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "kpf==0.1.12"
    
    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")
    
    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf 0.1.12", version_output
  end
end
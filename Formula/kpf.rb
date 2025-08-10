class Kpf < Formula
  include Language::Python::Virtualenv

  desc "A terminal utility to run kubectl port-forward and automatically restart it when endpoint changes are detected"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/39/82/113d6817f59ced1a9302a1f7ea2e5d4d442591700f401979e51af3885547/kpf-0.1.10.tar.gz"
  sha256 "bad1f4671d313f3c4ea4603ee44c18f426477f090bcd1de3138b23941300d37a"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_create(libexec, "python3.12")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "kpf==0.1.10"
    
    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")
    
    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf #{version}", version_output
  end
end
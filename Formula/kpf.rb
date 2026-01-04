class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/d5/23/cc9155017e1ec2243cde579b25767a384a2a93c7a3770f1542f87101ee0b/kpf-0.5.1.tar.gz"
  sha256 "93dd8597e3de62f440577ba786eece566dac71aa43d59c78daed40527a2605ad"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf==0.5.1"
    
    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"

    # Install shell completions
    # bash_completion.install tap.path/"completions/kpf.bash" => "kpf"
    # zsh_completion.install tap.path/"completions/_kpf" => "_kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")
    
    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf 0.5.1", version_output
  end
end
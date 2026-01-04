class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/71/67/4ed1b3fa276863f06bfcee88766ff5079d2d8390e4851201f0f354fcfe07/kpf-0.5.0.tar.gz"
  sha256 "b77492cc9c5080e94435f4be535d7b555b5d05cf3e036b4443001eb0a1167ef5"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "kpf==0.5.0"
    
    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"

    # Install shell completions
    bash_completion.install tap.path/"completions/kpf.bash" => "kpf"
    zsh_completion.install tap.path/"completions/_kpf" => "_kpf"

  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")
    
    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf 0.5.0", version_output
  end
end
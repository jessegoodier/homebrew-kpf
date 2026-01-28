class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/05/65/8b813f923f9e776a35fcac0e63764b2847f28a8145dd4d777a2a5a0e2558/kpf-0.8.1.tar.gz"
  sha256 "c1fed7f44ece47ab8344d5b871bcae13f929c05f76af9851ddc77bcd3968c19c"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")

    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf==0.8.1"

    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"

    # Install shell completions
    bash_completion.install "src/kpf/completions/kpf.bash" => "kpf"
    zsh_completion.install "src/kpf/completions/_kpf" => "_kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")

    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf 0.8.1", version_output
  end
end
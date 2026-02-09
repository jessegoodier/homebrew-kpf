class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/e7/f9/c6f84bc7bcc52d1a00c2a4d75db6bb9379ece7323022ba7624782e39248b/kpf-0.9.1.tar.gz"
  sha256 "1f1b80310c3565f48a1b2a98961553284791e5720e4f749d5b8c70cce41e467c"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")

    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf==0.9.1"

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
    assert_match "kpf 0.9.1", version_output
  end
end
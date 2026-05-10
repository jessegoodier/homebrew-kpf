class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/8f/89/2fc0daf573006777d4f69f44c8d686f81124e98c36e643b6f5df132b9e61/kpf-0.12.2.tar.gz"
  sha256 "3cdbfe9ce6c0c8ce073470ceef3674d076233b50b9583926df6f5c4eed48c412"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")

    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf==0.12.2"

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
    assert_match "kpf 0.12.2", version_output
  end
end
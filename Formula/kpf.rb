class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/ca/d6/f9417f8f328b4581f333141c1cc24d1445310efd311c455167893e5b83d8/kpf-0.10.1.tar.gz"
  sha256 "309fe07ce643d2b3e093153a6b39fab2238609fa005e14d90d4733cbc985c03d"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")

    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf==0.10.1"

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
    assert_match "kpf 0.10.1", version_output
  end
end
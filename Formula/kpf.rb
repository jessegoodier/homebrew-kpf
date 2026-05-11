class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/6b/be/f5dbc12d0e548e84f8922a49fb79fa5957c6acc3680d0a08cedd5f5acf74/kpf-0.12.5.tar.gz"
  sha256 "3d58a9b7f2af74222a32fd37cb114a3abd183b2b72c182e1df0fe1d1083dbe40"
  license "MIT"

  depends_on "python@3.14"

  def caveats
    <<~EOS
      kpfh is installed alongside kpf.
      Use kpfh to quickly reconnect to previously used port-forwards.
    EOS
  end

  def install
    virtualenv_create(libexec, "python3.14")

    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf==0.12.5"

    # Create binary symlinks
    bin.install_symlink libexec/"bin/kpf"
    bin.install_symlink libexec/"bin/kpfh"

    # Install shell completions
    bash_completion.install "src/kpf/completions/kpf.bash" => "kpf"
    zsh_completion.install "src/kpf/completions/_kpf" => "_kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")

    # Test that the kpfh command exists and shows help
    assert_match "Usage:", shell_output("#{bin}/kpfh --help")

    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf 0.12.5", version_output
  end
end

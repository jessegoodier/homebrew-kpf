class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/9f/04/23b345ebc62c85c97a08d2f405970c2c3385b0344512184bd760684077df/kpf-0.5.3.tar.gz"
  sha256 "90c6bcd1d4b567a29031abd29b74e49d603ab5ffffc17c287b6c6d0310c83e5a"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf==0.5.3"
    
    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"

    # Install shell completions
    bash_completion.install "completions/kpf.bash" => "kpf"
    zsh_completion.install "completions/_kpf" => "_kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{bin}/kpf --help")
    
    # Test version output
    version_output = shell_output("#{bin}/kpf --version")
    assert_match "kpf 0.5.3", version_output
  end
end
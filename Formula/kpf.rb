class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/b8/a8/772bd518bf89b834e2aac0b6c009aa67dca7930c66faec9079d8df0902a7/kpf-0.5.2.tar.gz"
  sha256 "8371d10bafb38155a18eab08886c767cf41c1741d91a199d52999f93b8d86e4c"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf==0.5.2"
    
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
    assert_match "kpf 0.5.2", version_output
  end
end
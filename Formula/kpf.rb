class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "https://github.com/jessegoodier/kpf"
  url "https://files.pythonhosted.org/packages/d7/2c/56dec785c8e7ded9334c1bf04a729687307c42be0eab47e65f3c6fe4edb2/kpf-0.6.0.tar.gz"
  sha256 "e62c3c4b364ce1dd2321895bdef83d3d7a54fab954642ab3d3e09ab4a8923897"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf==0.6.0"
    
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
    assert_match "kpf 0.6.0", version_output
  end
end
# homebrew-kpf

Homebrew tap for [kpf](https://github.com/jessegoodier/kpf) - A better way to port-forward with kubectl.

## Installation

```bash
brew tap jessegoodier/kpf
brew install kpf
```

Or install directly:

```bash
brew install jessegoodier/kpf/kpf
```

## About kpf

kpf is a Python utility that dramatically improves the experience of port-forwarding with kubectl. It's essentially a wrapper around `kubectl port-forward` that adds:

- 🔄 **Automatic Restart**: Monitors endpoint changes and restarts port-forward automatically
- 🎯 **Interactive Selection**: Choose services with a colorful, intuitive interface
- 🌈 **Color-coded Status**: Green for services with endpoints, red for those without
- 🔍 **Multi-resource Support**: Services, pods, deployments, and more
- 📊 **Rich Tables**: Beautiful formatted output with port information
- 🏷️ **Namespace Aware**: Work with specific namespaces or across all namespaces

## Usage

```bash
# Interactive mode (recommended)
kpf --prompt

# Interactive selection in specific namespace
kpf --prompt -n production

# Show all services across all namespaces
kpf --all

# Include pods and deployments with ports defined
kpf --all-ports

# Traditional kubectl port-forward syntax (backward compatible)
kpf svc/frontend 8080:8080 -n production
```

## Requirements

- kubectl configured with cluster access
- Python 3.11+ (automatically handled by Homebrew)

## Issues

For issues with the kpf tool itself, please visit the [main repository](https://github.com/jessegoodier/kpf/issues).

For issues with this Homebrew formula, please [open an issue here](https://github.com/jessegoodier/homebrew-kpf/issues).
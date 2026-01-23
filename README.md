# InOrbit Connector Cookiecutter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Test CookieCutter Template](https://github.com/inorbit-ai/inorbit-connector-cookiecutter/actions/workflows/test-cookiecutter.yml/badge.svg)](https://github.com/inorbit-ai/inorbit-connector-cookiecutter/actions/workflows/test-cookiecutter.yml)

This is a [cookiecutter](https://cookiecutter.readthedocs.io/) template for creating InOrbit connectors. It generates the necessary files and directories for a new Edge Connector project with a standardized structure, configuration, and testing setup.

## Features

- **Standardized Project Structure**: Consistent layout for all InOrbit connectors
- **Configuration Management**: Pydantic-based configuration models with environment variable support
- **Testing Framework**: Pre-configured pytest and tox setup
- **Docker Support**: Ready-to-use Dockerfile and docker-compose examples
- **CI/CD Ready**: GitHub Actions workflow templates included
- **Type Safety**: Full type hints and mypy support
- **Code Quality**: Pre-configured ruff, coverage, and tox setup

## Status

**Tested Python Versions**: 3.10, 3.11, 3.12, 3.13

These versions match all Python versions supported by [inorbit-connector-python](https://github.com/inorbit-ai/inorbit-connector-python). If this is not the case, please [open an issue](https://github.com/inorbit-ai/inorbit-connector-cookiecutter/issues).

## Quick Start

### Prerequisites

- Python 3.10 or later
- [pipx](https://pipx.pypa.io/) (recommended) or pip

### Generate a New Connector

1. Install and run cookiecutter:

```bash
pipx run cookiecutter gh:inorbit-ai/inorbit-connector-cookiecutter
```

2. Follow the interactive prompts:

   - **connector_target**: The name of your connector target
   - **author**: Your name or organization
   - **github_author**: Your GitHub username or organization
   - **email**: Contact email
   - **version**: Initial version (default: 0.1.0)
   - **python_version**: Minimum Python version (default: 3.13)
   - **use_current_directory**: Whether to generate in current directory (default: y)

3. Navigate to the generated project and install dependencies:

```bash
cd <your-connector-name>-connector
uv sync --extra=dev
```

4. Run tests to verify everything works:

```bash
uv run tox
```

## What Gets Generated

The template generates a complete Python package with:

- **Source Code Structure**:
  - Connector implementation with base class inheritance
  - Configuration models with validation
  - Entry point script

- **Configuration Files**:
  - `pyproject.toml` with dependencies and tool configurations
  - Example environment file (`.env`)
  - Example fleet configuration (YAML)

- **Testing**:
  - Pytest configuration
  - Example test files
  - Tox configuration for multiple Python versions

- **Docker Support**:
  - Multi-stage Dockerfile
  - Docker Compose example
  - Build scripts

- **Documentation**:
  - README template
  - Contributing guidelines
  - License files

- **CI/CD**:
  - GitHub Actions workflow template

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Reporting Issues

If you encounter any issues or have suggestions:

- [Open an issue](https://github.com/inorbit-ai/inorbit-connector-cookiecutter/issues) on GitHub
- Contact us at support@inorbit.ai

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [inorbit-connector-python](https://github.com/inorbit-ai/inorbit-connector-python): The base connector framework
- [InOrbit Developer Docs](https://developer.inorbit.ai/)

## Support

- **Documentation**: [InOrbit Developer Docs](https://developer.inorbit.ai/)
- **Issues**: [GitHub Issues](https://github.com/inorbit-ai/inorbit-connector-cookiecutter/issues)
- **Email**: support@inorbit.ai

---

**Powered by InOrbit** | [www.inorbit.ai](https://www.inorbit.ai)

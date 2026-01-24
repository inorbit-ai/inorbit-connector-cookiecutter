# InOrbit Connector Cookiecutter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Test CookieCutter Template](https://github.com/inorbit-ai/inorbit-connector-cookiecutter/actions/workflows/test-cookiecutter.yml/badge.svg)](https://github.com/inorbit-ai/inorbit-connector-cookiecutter/actions/workflows/test-cookiecutter.yml)

This is a [cookiecutter](https://cookiecutter.readthedocs.io/) template for creating InOrbit connectors. It generates the necessary files and directories for a new Edge Connector project with a standardized structure, configuration, and testing setup.

## Features

- **CI/CD Ready**: GitHub Actions workflow templates included
- **Type Safety**: Full type hints and mypy support
- **Code Quality**: Pre-configured ruff, coverage, and tox setup
- **Docker Support**: Ready-to-use Dockerfile and docker-compose examples
- **Standardized Project Structure**: Consistent layout for all InOrbit connectors

## Status

**Tested Python Versions**: 3.10, 3.11, 3.12, 3.13

These versions match all Python versions supported by [inorbit-connector-python](https://github.com/inorbit-ai/inorbit-connector-python). If this is not the case, please [open an issue](https://github.com/inorbit-ai/inorbit-connector-cookiecutter/issues).

## Quick Start

### Prerequisites

To utilize the cookiecutter:
- [pipx](https://pipx.pypa.io/) for running cookiecutter

To use the generated project:
- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [git](https://git-scm.com/downloads)
- [make](https://www.gnu.org/software/make/) (optional)

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
   - **use_current_directory**: Whether to generate in current directory (good for running within empty repositories) (default: y)

3. Navigate to the generated project and install dependencies:

```bash
cd <your-connector-name>-connector
uv sync --extra=dev
```

Refer to the official documentation for installing `uv`: https://docs.astral.sh/uv/getting-started/installation/

4. Run tests to verify everything works:

```bash
uv run tox
```

## What Gets Generated

The template generates a complete Python package with:

- **Sample source code structure**:
  - Sample connector implementation with base class inheritance
  - Sample configuration models with validation
  - Entry point script

- **Configuration files**:
  - `pyproject.toml` with dependencies and tool configurations
  - Example environment file (`.env`)
  - Example fleet configuration (YAML file)
  - [`ruff`](https://docs.astral.sh/ruff/) configuration for code linting and formatting
  - A Makefile for version bumping which:
    - Requires no external dependencies other than `uv` and `git`
    - Supports dry-run mode and checking for a clean working tree
    - Uses `uv version` to bump the version in `pyproject.toml` and `uv.lock`
    - Creates a commit and a tag with the new version following the rules that trigger the publish job in the GitHub Actions workflow

- **Testing**:
  - Pytest configuration
  - Example test files
  - [`tox`](https://tox.wiki/en/4.34.1/) configuration for automated linting and testing

- **Docker packaging**:
  - Multi-stage Dockerfile
  - Docker Compose example
  - Build scripts

- **Documentation**:
  - README template
  - Contributing guidelines
  - License files
  - REUSE compliance configuration

- **CI/CD**:
  - GitHub Actions workflow template for:
    - Linting and testing
    - REUSE compliance checking
    - Docker build and push

## Testing

This cookiecutter template includes tests to verify the post-generation hook and Makefile functionality.

### Running Tests

1. Install dependencies using `uv`:
   ```bash
   uv sync --extra=dev
   ```

2. Run the tests:
   ```bash
   uv run pytest tests/ -v
   ```

### Test Requirements

The tests require:
- `pytest` - Test framework
- `git` - For testing version bump functionality
- `make` - For testing Makefile commands
- `uv` - For testing version bumping (used by the Makefile)

### Test Coverage

- **Post-generation hook tests**: Verify file movement, backup functionality, nested directory handling, and git exclusion
- **Version bump tests**: Verify version bumping, dry-run mode, git integration, and clean working tree requirements

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

<img width="6400" height="400" alt="image" src="https://github.com/user-attachments/assets/d50bbacf-6e6f-434a-9b44-8c743a6de1f9" />


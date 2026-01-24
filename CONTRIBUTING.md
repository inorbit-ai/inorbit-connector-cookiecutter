<!--
SPDX-FileCopyrightText: 2026 InOrbit, Inc.

SPDX-License-Identifier: MIT
-->

# Contributing

Contributions are encouraged, and they are greatly appreciated! Every little bit helps, and credit will always be given.

> [!IMPORTANT]
> Any contribution that you make to this repository will be under the MIT license, as dictated by that [license](https://opensource.org/licenses/MIT).

## Get Started

Ready to contribute? Here's how to set up `inorbit-connector-cookiecutter` for local development.

1. Fork the `inorbit-connector-cookiecutter` repo on [GitHub](https://github.com/inorbit-ai/inorbit-connector-cookiecutter).

2. Clone your fork locally:

   ```bash
   git clone git@github.com:{your_username_here}/inorbit-connector-cookiecutter.git
   ```

3. Install `uv` if you haven't already. Refer to the official documentation: https://docs.astral.sh/uv/getting-started/installation/.

4. Install dependencies:

   ```bash
   cd inorbit-connector-cookiecutter
   uv sync --extra=dev
   ```

5. Create a branch for local development:

   ```bash
   git checkout -b {your_development_type}/short-description
   ```

   Ex: feature/read-tiff-files or bugfix/handle-file-not-found<br>
   Now you can make your changes locally.

6. Run tests to verify your changes:

   ```bash
   uv run pytest tests/ -v
   ```

7. Commit your changes and push your branch to GitHub:

   ```bash
   git add .
   git commit -m "Resolves #xyz. Your detailed description of your changes."
   git push origin {your_development_type}/short-description
   ```

8. Submit a pull request through the [GitHub](https://github.com/inorbit-ai/inorbit-connector-cookiecutter/pulls) website.

## Version bump and release - Maintainers only

Releases use `uv version --bump`, which updates both `pyproject.toml` and `uv.lock` (if present).

To release a new version:

1. Ensure you're on the latest `main` branch and working tree is clean:

   ```bash
   git checkout main
   git pull
   ```

2. Preview the version bump (optional):

   ```bash
   uv version --bump patch --dry-run
   ```

   Available parts: `patch`, `minor`, `major`, `alpha`, `beta`, `rc`, `post`, `dev`, `stable`

3. Bump the version:

   ```bash
   uv version --bump patch
   # or for minor/major releases:
   uv version --bump minor
   uv version --bump major
   ```

   This updates the version in `pyproject.toml` and `uv.lock` (if present).

4. Commit the version changes:

   ```bash
   git add pyproject.toml uv.lock
   git commit -m "Bump version: <old-version> → <new-version>"
   ```

5. Create a tag:

   ```bash
   git tag -a "v<new-version>" -m "Release v<new-version>"
   ```

6. Push the commit and tag:

   ```bash
   git push
   git push --tags
   ```

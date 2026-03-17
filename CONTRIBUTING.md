# Contributing to steer-materials

Thank you for your interest in contributing to steer-materials! This document provides guidelines and instructions for contributing.

## Reporting Bugs

If you find a bug, please open an issue on [GitHub Issues](https://github.com/stanford-developers/steer-materials/issues) with:

- A clear description of the problem
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your Python version and OS

## Suggesting Features

Feature requests are welcome. Please open an issue describing:

- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered

## Development Setup

1. Fork the repository and clone your fork:

   ```bash
   git clone https://github.com/YOUR-USERNAME/steer-materials.git
   cd steer-materials
   ```

2. Install in development mode:

   ```bash
   pip install -e ".[dev]"
   ```

3. Run the tests to make sure everything works:

   ```bash
   pytest
   ```

## Making Changes

1. Create a new branch for your changes:

   ```bash
   git checkout -b your-feature-branch
   ```

2. Make your changes and add tests for new functionality.

3. Ensure all tests pass:

   ```bash
   pytest
   ```

4. Format your code with black and check with flake8:

   ```bash
   black steer_materials/ test/
   flake8 steer_materials/ test/
   ```

5. Commit your changes with a clear message and push to your fork.

6. Open a Pull Request against the `main` branch.

## Code Style

- We use [black](https://github.com/psf/black) for code formatting (line length 88).
- We use [flake8](https://flake8.pycqa.org/) for linting.
- Write docstrings for public classes and methods.
- Add type hints where practical.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

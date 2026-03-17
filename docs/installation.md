# Installation

## Requirements

- Python 3.10 or later
- [steer-core](https://github.com/stanford-developers/steer-core) (installed automatically)

## From PyPI

```bash
pip install steer-materials
```

## From source

Clone the repository and install in editable mode:

```bash
git clone https://github.com/stanford-developers/steer-materials.git
cd steer-materials
pip install -e .
```

## Optional extras

Install development tools (testing, linting, formatting):

```bash
pip install -e ".[dev]"
```

Install documentation tools:

```bash
pip install -e ".[docs]"
```

## Verify the installation

```python
import steer_materials
print(steer_materials.__version__)
```

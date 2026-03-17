# Developer Guide

## Setting up for development

```bash
git clone https://github.com/stanford-developers/steer-materials.git
cd steer-materials
pip install -e ".[dev]"
```

This installs the package in editable mode along with all development tools:
pytest, pytest-cov, black, flake8, mypy, build, and twine.

## Running tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=steer_materials --cov-report=term-missing
```

## Code style

The project uses [black](https://github.com/psf/black) for formatting and [flake8](https://flake8.pycqa.org/) for linting:

```bash
# Format code
black steer_materials/ test/

# Check linting
flake8 steer_materials/ test/
```

Black is configured with a line length of 88 (see `pyproject.toml`).

## Project structure

```
steer-materials/
├── steer_materials/
│   ├── __init__.py        # Package version
│   └── Base.py            # _Material, Metal, Solvent, _VolumedMaterialMixin
├── test/
│   ├── conftest.py        # Shared fixtures
│   ├── test_material.py   # Tests for _Material, Metal, Solvent
│   └── test_volumed_material.py  # Tests for _VolumedMaterialMixin
├── docs/                  # MkDocs documentation (this site)
├── .github/workflows/     # CI: tests + linting
├── pyproject.toml         # Build config, dependencies, tool settings
├── LICENSE                # AGPL-3.0-or-later
├── CITATION.cff           # Citation metadata
├── CONTRIBUTING.md        # Contribution guidelines
└── CODE_OF_CONDUCT.md     # Contributor Covenant v2.1
```

## Architecture

### Internal unit convention

All values are stored internally in **SI base units** (kg, m) and converted
to user-facing units (g/cm³, $/kg, g, cm³) in property getters. The
conversion constants come from `steer_core.Constants.Units`:

| Constant | Value | Meaning |
|---|---|---|
| `KG_TO_G` | 1000 | kg → g |
| `G_TO_KG` | 0.001 | g → kg |
| `M_TO_CM` | 100 | m → cm |
| `CM_TO_M` | 0.01 | cm → m |

### Class hierarchy

- **`_Material`** — Base class providing `name`, `density`, `specific_cost`, `color`, and `last_updated`. Not instantiated directly.
- **`Metal`** / **`Solvent`** — Concrete subclasses of `_Material` for different material categories.
- **`_VolumedMaterialMixin`** — Mixin that adds `volume`, `mass`, and `cost` tracking. Combined with a `_Material` subclass via multiple inheritance.

### Mixins from steer-core

`_Material` inherits from four `steer-core` mixins:

| Mixin | Purpose |
|---|---|
| `ValidationMixin` | Type and range checking (`validate_positive_float`, `validate_string`) |
| `PropagationMixin` | Cascading updates when properties change |
| `DunderMixin` | `__repr__`, `__eq__`, and other dunder methods |
| `SerializerMixin` | JSON serialization and deserialization |

## Making a pull request

1. Fork the repo and create a feature branch.
2. Write tests for any new functionality.
3. Ensure `pytest` and `black --check` both pass.
4. Open a PR against `main` with a clear description.

See [CONTRIBUTING.md](https://github.com/stanford-developers/steer-materials/blob/main/CONTRIBUTING.md) for full guidelines.

## Building documentation locally

```bash
pip install -e ".[docs]"
mkdocs serve
```

Then open <http://127.0.0.1:8000> in your browser.

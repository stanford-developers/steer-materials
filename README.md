# steer-materials

[![Tests](https://github.com/stanford-developers/steer-materials/actions/workflows/tests.yml/badge.svg)](https://github.com/stanford-developers/steer-materials/actions/workflows/tests.yml)
[![Lint](https://github.com/stanford-developers/steer-materials/actions/workflows/lint.yml/badge.svg)](https://github.com/stanford-developers/steer-materials/actions/workflows/lint.yml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

Material definitions for the **STEER** (Storage Technology for Energy and Economic Research) simulation framework. This package provides base classes for representing physical materials — metals, solvents, and other substances — with built-in unit conversion, validation, and cost tracking.

`steer-materials` is a support package within the broader [STEER ecosystem](https://github.com/stanford-developers).

## Installation

```bash
pip install steer-materials
```

For development:

```bash
git clone https://github.com/stanford-developers/steer-materials.git
cd steer-materials
pip install -e ".[dev]"
```

## Quick Start

```python
from steer_materials.Base import Metal, Solvent

# Create a metal material (density in g/cm³, cost in $/kg)
aluminum = Metal(name="Aluminum", density=2.7, specific_cost=2.50, color="silver")
print(aluminum.density)         # 2.7 g/cm³
print(aluminum.specific_cost)   # 2.50 $/kg

# Create a solvent
water = Solvent(name="Water", density=1.0, specific_cost=0.01, color="clear")
```

## Testing

```bash
pip install -e ".[test]"
pytest
```

With coverage:

```bash
pytest --cov=steer_materials
```

## Documentation

Full documentation for the STEER ecosystem is available at the [STEER documentation site](https://github.com/stanford-developers).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is dual-licensed:

1. **Open source** — [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0) (AGPL-3.0)
2. **Commercial** — A separate commercial license is available for use without AGPL-3.0 copyleft requirements. Contact [nsiemons@stanford.edu](mailto:nsiemons@stanford.edu) for details.

See [LICENCE.txt](LICENCE.txt) for full terms.

## Citation

If you use this software in your research, please cite it using the metadata in [CITATION.cff](CITATION.cff).
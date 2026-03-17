# steer-materials

**Material definitions for the STEER simulation framework.**

`steer-materials` provides base classes for representing physical materials — metals, solvents, and other substances — with built-in unit conversion, validation, and cost tracking.

It is a support package within the broader [STEER](https://github.com/stanford-developers) (Storage Technology for Energy and Economic Research) ecosystem.

## Features

- **Validated properties** — density, cost, and names are type-checked on assignment.
- **Automatic unit conversion** — values are stored in SI internally and exposed in common units (g/cm³, $/kg).
- **Cost tracking** — optional volume/mass tracking with automatic cost derivation.
- **Soft & hard ranges** — each physical property carries a plausible range and an absolute bound.
- **Serialization** — built-in JSON serialization via `steer-core` mixins.

## Quick example

```python
from steer_materials.Base import Metal

aluminum = Metal(
    name="Aluminum",
    density=2.7,        # g/cm³
    specific_cost=2.50, # $/kg
    color="silver",
)
print(aluminum.density)        # 2.7
print(aluminum.specific_cost)  # 2.5
```

## Navigation

| Section | Description |
|---|---|
| [Installation](installation.md) | Install from PyPI or source |
| [Quick Start](quickstart.md) | Create your first material in 5 minutes |
| [Examples](examples.md) | Common usage patterns and recipes |
| [API Reference](api.md) | Full class and method documentation |
| [Developer Guide](developer.md) | Contributing, testing, and code style |

# Quick Start

This guide walks you through creating materials with `steer-materials`.

## Creating a Metal

```python
from steer_materials.Base import Metal

steel = Metal(
    name="Steel",
    density=7.87,       # g/cm³
    specific_cost=0.80, # $/kg
    color="grey",
)
```

All inputs are validated on construction — passing a negative density or a non-string name raises immediately:

```python
# This raises ValueError:
Metal(name="Bad", density=-1.0, specific_cost=1.0, color="red")

# This raises TypeError:
Metal(name=123, density=7.87, specific_cost=0.80, color="grey")
```

## Creating a Solvent

```python
from steer_materials.Base import Solvent

water = Solvent(
    name="Water",
    density=1.0,
    specific_cost=0.01,
    color="clear",
)
```

## Reading properties

Properties are returned in user-friendly units:

```python
print(steel.density)         # 7.87  (g/cm³)
print(steel.specific_cost)   # 0.80  ($/kg)
print(steel.name)            # "Steel"
print(steel.last_updated)    # "2026-03-17 10:30:00"
```

## Updating properties

Setters validate input and trigger dependent recalculations:

```python
steel.density = 8.0
print(steel.density)  # 8.0

steel.name = "Stainless Steel"
```

## Inspecting ranges

Each property has a **soft range** (±10 % for density, 0.5×–2× for cost) and a **hard range** (absolute bounds):

```python
print(steel.density_range)       # (7.08, 8.66)
print(steel.density_hard_range)  # (0, 100)
```

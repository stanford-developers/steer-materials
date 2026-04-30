# Examples

## Tracking volume, mass, and cost

The `_VolumedMaterialMixin` adds optional volume/mass tracking with automatic cost derivation. To use it, create a combined class:

```python
from steer_materials.Base import Metal, _VolumedMaterialMixin


class VolumedMetal(_VolumedMaterialMixin, Metal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
```

### Initialize with volume

Provide volume in cm³ — mass and cost are computed automatically:

```python
al = VolumedMetal(
    name="Aluminum",
    density=2.7,
    specific_cost=2.50,
    color="silver",
    volume=100.0,  # cm³
)

print(al.volume)  # 100.0  cm³
print(al.mass)    # 270.0  g
print(al.cost)    # 0.68   $
```

### Initialize with mass

Provide mass in grams instead — volume is back-calculated:

```python
al = VolumedMetal(
    name="Aluminum",
    density=2.7,
    specific_cost=2.50,
    color="silver",
    mass=270.0,  # g
)

print(al.volume)  # 100.0  cm³
```

### Omit both

If neither `volume` nor `mass` is given, all three remain `None` until assigned:

```python
al = VolumedMetal(
    name="Aluminum", density=2.7, specific_cost=2.50, color="silver"
)
print(al.volume)  # None
print(al.mass)    # None
print(al.cost)    # None

al.volume = 50.0
print(al.mass)  # 135.0 g
print(al.cost)  # 0.34  $
```

!!! warning "Mutual exclusivity"
    You **cannot** provide both `volume` and `mass` at the same time:

    ```python
    # Raises ValueError
    VolumedMetal(
        name="Al", density=2.7, specific_cost=2.50, color="silver",
        volume=100.0, mass=270.0,
    )
    ```

## Propagation on property changes

When you update `density` or `specific_cost`, derived values recalculate automatically:

```python
al = VolumedMetal(
    name="Aluminum", density=2.7, specific_cost=2.50,
    color="silver", volume=100.0,
)

# Change density — mass and cost update, volume stays
al.density = 5.0
print(al.volume)  # 100.0
print(al.mass)    # 500.0
print(al.cost)    # 1.25

# Change specific cost — cost updates, mass stays
al.specific_cost = 5.0
print(al.mass)  # 500.0
print(al.cost)  # 2.5
```

## Clearing volume/mass

Set volume or mass to `None` to clear all derived values:

```python
al.volume = None
print(al.volume)  # None
print(al.mass)    # None
print(al.cost)    # None
```

## Comparing materials

Materials provide a human-readable representation via `steer-core` mixins:

```python
copper = Metal(name="Copper", density=8.96, specific_cost=8.00, color="orange")
print(copper)
```

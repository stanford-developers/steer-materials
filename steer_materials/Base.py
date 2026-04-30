# SPDX-FileCopyrightText: 2024-2026 Nicholas Siemons
# SPDX-License-Identifier: AGPL-3.0-or-later

from steer_core.Constants.Units import *
from steer_core.Mixins.TypeChecker import ValidationMixin
from steer_core.Mixins.Serializer import SerializerMixin
from steer_core.Mixins.Dunder import DunderMixin
from steer_core.Mixins.Propagation import PropagationMixin

from datetime import datetime as dt

import numpy as np


class _Material(
    ValidationMixin, 
    PropagationMixin,
    DunderMixin,
    SerializerMixin
    ):
    """Base class for all material types in the STEER framework.

    Provides validated properties for physical and cost characteristics
    with automatic unit conversion between SI internal storage and
    user-facing units (g/cm³ for density, $/kg for cost).

    This class is not intended to be instantiated directly — use
    [`Metal`][steer_materials.Base.Metal] or
    [`Solvent`][steer_materials.Base.Solvent] instead.

    Attributes:
        name: Name of the material.
        density: Density in g/cm³.
        specific_cost: Cost per kilogram in $/kg.
        color: Display color of the material.
        last_updated: Timestamp of the last property change.
    """

    def __init__(self, name: str, density: float, specific_cost: float, color: str):
        """Create a new material.

        Args:
            name: Name of the material.
            density: Density in g/cm³. Must be a non-negative number.
            specific_cost: Cost per kilogram in $/kg. Must be a non-negative number.
            color: Display color string.

        Raises:
            TypeError: If any argument has the wrong type.
            ValueError: If density or specific_cost is negative.
        """
        self.density = density
        self.specific_cost = specific_cost
        self.name = name
        self.color = color

        self._last_updated = dt.now()
        self._update_ranges()

    def _update_ranges(self):
        self._density_range = (self._density * 0.9, self._density * 1.1)
        self._specific_cost_range = (self._specific_cost * 0.5, self._specific_cost * 2)

    @property
    def density(self) -> float:
        """Density of the material in g/cm³."""
        return np.round(self._density * (KG_TO_G / M_TO_CM**3), 2)

    @property
    def density_range(self) -> tuple[float, float]:
        """Soft range for density (±10% of current value) in g/cm³."""
        return (
            np.round(self._density_range[0] * (KG_TO_G / M_TO_CM**3), 2),
            np.round(self._density_range[1] * (KG_TO_G / M_TO_CM**3), 2),
        )

    @property
    def density_hard_range(self):
        """Absolute valid range for density in g/cm³: (0, 100)."""
        return (0, 100)

    @property
    def specific_cost(self):
        """Cost per kilogram in $/kg."""
        return np.round(self._specific_cost, 2)

    @property
    def specific_cost_range(self) -> tuple[float, float]:
        """Soft range for specific cost (0.5x–2x current value) in $/kg."""
        return (
            np.round(self._specific_cost_range[0], 2),
            np.round(self._specific_cost_range[1], 2),
        )

    @property
    def specific_cost_hard_range(self) -> tuple[int, int]:
        """Absolute valid range for specific cost in $/kg: (0, 1000)."""
        return (0, 1000)

    @property
    def name(self):
        """Name of the material."""
        return self._name

    @property
    def color(self) -> str:
        """Display color of the material."""
        return self._color

    @property
    def last_updated(self) -> str:
        """Timestamp of the last modification as `YYYY-MM-DD HH:MM:SS`."""
        return self._last_updated.strftime("%Y-%m-%d %H:%M:%S")

    @color.setter
    def color(self, color: str) -> None:
        self.validate_string(color, "Color")
        self._color = color if color else "Unknown"

    @density.setter
    def density(self, density: float) -> None:

        # validate input 
        self.validate_positive_float(density, "Density")

        # convert and set
        self._density = density * G_TO_KG / CM_TO_M**3

        # If this is a volumed material and volume is set, recalculate mass
        if hasattr(self, '_volume') and self._volume is not None:
            self._mass = self._volume * self._density
            if hasattr(self, '_cost'):
                self._cost = self._mass * self._specific_cost

    @specific_cost.setter
    def specific_cost(self, specific_cost: float) -> None:

        # validate input
        self.validate_positive_float(specific_cost, "Specific Cost")
        
        # set value
        self._specific_cost = specific_cost
        
        # If this is a volumed material with mass, recalculate cost
        if hasattr(self, '_mass') and self._mass is not None:
            if hasattr(self, '_cost'):
                self._cost = self._mass * self._specific_cost

    @name.setter
    def name(self, name: str) -> None:
        self.validate_string(name, "Name")
        self._name = name


class Metal(_Material):
    """A metallic material (e.g. aluminum, steel, copper).

    Inherits all behavior from `_Material`. Use this class for metals
    used in cell enclosures, current collectors, and structural components.

    Examples:
        ```python
        from steer_materials.Base import Metal

        aluminum = Metal(
            name="Aluminum",
            density=2.7,        # g/cm³
            specific_cost=2.50, # $/kg
            color="silver",
        )
        ```
    """

    def __init__(self, name: str, density: float, specific_cost: float, color: str):

        super().__init__(name, density, specific_cost, color)


class Solvent(_Material):
    """A solvent material (e.g. water, electrolyte solvents).

    Inherits all behavior from `_Material`. Use this class for liquid
    solvents used in electrolyte formulations and processing.

    Examples:
        ```python
        from steer_materials.Base import Solvent

        water = Solvent(
            name="Water",
            density=1.0,        # g/cm³
            specific_cost=0.01, # $/kg
            color="clear",
        )
        ```
    """

    def __init__(self, name: str, density: float, specific_cost: float, color: str):

        super().__init__(name, density, specific_cost, color)


class _VolumedMaterialMixin:
    """Mixin that adds volume, mass, and cost tracking to a material.

    When combined with a `_Material` subclass via multiple inheritance,
    this mixin adds optional `volume` (cm³) and `mass` (g) properties.
    Cost ($) is always derived automatically from mass and `specific_cost`.

    You may provide **at most one** of `volume` or `mass` at construction
    time — the other value (and cost) will be computed from the material's
    density. If neither is provided, all three remain `None` until set.

    When `density` or `specific_cost` is changed later, dependent values
    are automatically recalculated.

    Examples:
        ```python
        from steer_materials.Base import Metal, _VolumedMaterialMixin

        class VolumedMetal(_VolumedMaterialMixin, Metal):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        al = VolumedMetal(
            name="Aluminum", density=2.7,
            specific_cost=2.50, color="silver",
            volume=100.0,  # cm³
        )
        print(al.mass)  # 270.0 g
        print(al.cost)   # 0.68 $
        ```
    """

    def __init__(
            self, 
            *, 
            volume: float | None = None, 
            mass: float | None = None, 
            **kwargs
        ):
        """Initialize volume/mass tracking.

        Args:
            volume: Volume in cm³. Mutually exclusive with `mass`.
            mass: Mass in grams. Mutually exclusive with `volume`.
            **kwargs: Forwarded to the next class in the MRO (typically a `_Material` subclass).

        Raises:
            ValueError: If both `volume` and `mass` are provided.
        """

        super().__init__(**kwargs)

        # Check that only one of volume or mass is provided
        provided = sum([volume is not None, mass is not None])
        if provided > 1:
            raise ValueError(
                "Only one of 'volume' or 'mass' can be provided during initialization. "
                f"Received: volume={volume}, mass={mass}"
            )

        self._volume = None
        self._mass = None
        self._cost = None

        if volume is not None:
            self.volume = volume
        elif mass is not None:
            self.mass = mass

    @property
    def volume(self) -> float | None:
        """Volume in cm³, or `None` if not set."""
        if hasattr(self, '_volume') and self._volume is not None:
            return np.round(self._volume * (M_TO_CM**3), 2)
        else:
            return None
        
    @property
    def mass(self) -> float | None:
        """Mass in grams, or `None` if not set."""
        if hasattr(self, '_mass') and self._mass is not None:
            return np.round(self._mass * KG_TO_G, 2)
        else:
            return None
        
    @property
    def cost(self) -> float | None:
        """Cost in dollars, or `None` if not set."""
        if hasattr(self, '_cost') and self._cost is not None:
            return np.round(self._cost, 2)
        else:
            return None

    
    @volume.setter
    def volume(self, value):
        
        if value is not None:
            ValidationMixin.validate_positive_float(value, "Volume")
            self._volume = value * CM_TO_M**3
            self._mass = self._volume * self._density
            self._cost = self._mass * self._specific_cost
        else:
            self._volume = None
            self._mass = None
            self._cost = None

    @mass.setter
    def mass(self, value):

        if value is not None:
            ValidationMixin.validate_positive_float(value, "Mass")
            self._mass = value * G_TO_KG
            self._volume = self._mass / self._density
            self._cost = self._mass * self._specific_cost
        else:
            self._volume = None
            self._mass = None
            self._cost = None



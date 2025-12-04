from steer_core.Constants.Units import *
from steer_core.Mixins.TypeChecker import ValidationMixin
from steer_core.Mixins.Serializer import SerializerMixin
from steer_core.Mixins.Dunder import DunderMixin

from datetime import datetime as dt

import numpy as np


class _Material(
    ValidationMixin, 
    SerializerMixin,
    DunderMixin
    ):

    def __init__(self, name: str, density: float, specific_cost: float, color: str):
        """
        Metal object for encapsulation of the cell

        Parameters
        ----------
        name : str
            Name of the material.
        density : float
            Density of the material in g/cm^3.
        specific_cost : float
            Specific cost of the material in $/kg.
        color : str
            Color of the material.
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
    def density(self):
        return round(self._density * (KG_TO_G / M_TO_CM**3), 2)

    @property
    def density_range(self):
        return (
            round(self._density_range[0] * (KG_TO_G / M_TO_CM**3), 2),
            round(self._density_range[1] * (KG_TO_G / M_TO_CM**3), 2),
        )

    @property
    def density_hard_range(self):
        return (0, 100)

    @property
    def specific_cost(self):
        return round(self._specific_cost, 2)

    @property
    def specific_cost_range(self):
        return (
            round(self._specific_cost_range[0], 2),
            round(self._specific_cost_range[1], 2),
        )

    @property
    def specific_cost_hard_range(self):
        return (0, 1000)

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def last_updated(self):
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

    def __init__(self, name: str, density: float, specific_cost: float, color: str):

        super().__init__(name, density, specific_cost, color)


class Solvent(_Material):

    def __init__(self, name: str, density: float, specific_cost: float, color: str):

        super().__init__(name, density, specific_cost, color)


class _VolumedMaterialMixin:
    """
    Mixin for materials that optionally track volume (cm^3) or mass (kg).
    Cost ($) is always derived from mass and specific_cost.
    """

    def __init__(
            self, 
            *, 
            volume=None, 
            mass=None, 
            **kwargs
        ):

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
    def volume(self):
        if hasattr(self, '_volume') and self._volume is not None:
            return round(self._volume * (M_TO_CM**3), 4)
        else:
            return None
        
    @property
    def mass(self):
        if hasattr(self, '_mass') and self._mass is not None:
            return round(self._mass * KG_TO_G, 2)
        else:
            return None
        
    @property
    def cost(self):
        if hasattr(self, '_cost') and self._cost is not None:
            return round(self._cost, 2)
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



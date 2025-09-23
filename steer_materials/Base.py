from steer_core.Constants.Units import *
from steer_core.Mixins.TypeChecker import ValidationMixin
from steer_core.Mixins.Serializer import SerializerMixin

from datetime import datetime as dt

import numpy as np


class _Material(ValidationMixin, SerializerMixin):

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
        return self._specific_cost

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
        self.validate_positive_float(density, "Density")
        self._density = density * G_TO_KG / CM_TO_M**3

    @specific_cost.setter
    def specific_cost(self, specific_cost: float) -> None:
        self.validate_positive_float(specific_cost, "Specific Cost")
        self._specific_cost = specific_cost

    @name.setter
    def name(self, name: str) -> None:
        self.validate_string(name, "Name")
        self._name = name

    def __str__(self):
        return f"{self.name}, {self.__class__.__name__}, {self.last_updated}"

    def __repr__(self):
        return self.__str__()


class Metal(_Material):

    def __init__(self, name: str, density: float, specific_cost: float, color: str):

        super().__init__(name, density, specific_cost, color)


class Solvent(_Material):

    def __init__(self, name: str, density: float, specific_cost: float, color: str):

        super().__init__(name, density, specific_cost, color)

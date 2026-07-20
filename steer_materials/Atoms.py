# SPDX-FileCopyrightText: 2024-2026 Stanford University
# SPDX-License-Identifier: AGPL-3.0-or-later

from steer_core.Constants.Units import *
from steer_core.Mixins.TypeChecker import ValidationMixin
from steer_core.Mixins.Serializer import SerializerMixin
from steer_core.Mixins.Dunder import DunderMixin
from steer_core.Mixins.Propagation import PropagationMixin


class Atom(
    ValidationMixin, 
    SerializerMixin, 
    DunderMixin, 
    PropagationMixin
):
    
    def __init__(
            self, 
            name: str, 
            symbol: str, 
            atomic_number: int, 
            atomic_mass: float
        ):

        self.name = name
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.atomic_mass = atomic_mass

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def symbol(self) -> str:
        return self._symbol
    
    @property
    def atomic_number(self) -> int:
        return self._atomic_number
    
    @property
    def atomic_mass(self) -> float:
        return self._atomic_mass * KG_TO_AU  

    @name.setter
    def name(self, value: str):
        self.validate_type(value, str, "name")
        self._name = value

    @symbol.setter
    def symbol(self, value: str):
        self.validate_type(value, str, "symbol")
        self._symbol = value

    @atomic_number.setter
    def atomic_number(self, value: int):
        self.validate_type(value, int, "atomic_number")
        self._atomic_number = value

    @atomic_mass.setter
    def atomic_mass(self, value: float):
        self.validate_type(value, float, "atomic_mass")
        self._atomic_mass = value * AU_TO_KG


# SPDX-FileCopyrightText: 2024-2026 Stanford University
# SPDX-License-Identifier: AGPL-3.0-or-later

from steer_core.Constants.Units import *
from steer_core.Mixins.TypeChecker import ValidationMixin
from steer_core.Mixins.Serializer import SerializerMixin
from steer_core.Mixins.Dunder import DunderMixin
from steer_core.Mixins.Propagation import PropagationMixin

from steer_core.Decorators.General import recalculate

from steer_core.Constants.Periodic_table import (
    atomic_numbers_to_symbols,
    atomic_numbers_to_names,
    atomic_numbers_to_masses
)

from steer_core.Constants.Units import AU_TO_KG, KG_TO_AU

class Atom(
    ValidationMixin, 
    SerializerMixin, 
    DunderMixin, 
    PropagationMixin
):
    
    def __init__(
            self, 
            symbol: str, 
            atomic_mass: float = None,
            charge: float = 0.0
        ):

        self._update_properties = False

        self.symbol = symbol
        self.atomic_mass = atomic_mass
        self.charge = charge

        self._calculate_all_properties()
        self._update_properties = True

    def _calculate_all_properties(self):
        """
        Calculate all properties of the atom based on the provided information.
        """
        self._calculate_mass_from_symbol()
        self._calculate_name_from_symbol()
        self._calculate_atomic_number_from_symbol()

    def _calculate_mass_from_name(self):
        """
        Calculate the atomic mass based on the atom's name.
        """
        atomic_number = {v: k for k, v in atomic_numbers_to_names.items()}[self._name]
        self._atomic_mass = atomic_numbers_to_masses[atomic_number] * AU_TO_KG

    def _calculate_symbol_from_name(self):
        """
        Calculate the atomic symbol based on the atom's name.
        """
        atomic_number = {v: k for k, v in atomic_numbers_to_names.items()}[self._name]
        self._symbol = atomic_numbers_to_symbols[atomic_number]

    def _calculate_atomic_number_from_name(self):
        """
        Calculate the atomic number based on the atom's name.
        """
        atomic_number = {v: k for k, v in atomic_numbers_to_names.items()}[self._name]
        self._atomic_number = atomic_number

    def _calculate_mass_from_symbol(self):
        """
        Calculate the atomic mass based on the atom's symbol.
        """
        atomic_number = {v: k for k, v in atomic_numbers_to_symbols.items()}[self._symbol]
        self._atomic_mass = atomic_numbers_to_masses[atomic_number] * AU_TO_KG

    def _calculate_name_from_symbol(self):
        """
        Calculate the atomic name based on the atom's symbol.
        """
        atomic_number = {v: k for k, v in atomic_numbers_to_symbols.items()}[self._symbol]
        self._name = atomic_numbers_to_names[atomic_number]

    def _calculate_atomic_number_from_symbol(self):
        """
        Calculate the atomic number based on the atom's symbol.
        """
        self._atomic_number = {v: k for k, v in atomic_numbers_to_symbols.items()}[self._symbol]

    def _calculate_mass_from_atomic_number(self):
        """
        Calculate the atomic mass based on the atom's atomic number.
        """
        self._atomic_mass = atomic_numbers_to_masses[self._atomic_number] * AU_TO_KG

    def _calculate_name_from_atomic_number(self):
        """
        Calculate the atomic name based on the atom's atomic number.
        """
        self._name = atomic_numbers_to_names[self._atomic_number]

    def _calculate_symbol_from_atomic_number(self):
        """
        Calculate the atomic symbol based on the atom's atomic number.
        """
        self._symbol = atomic_numbers_to_symbols[self._atomic_number]

    def _calculate_name_from_mass(self):
        """
        Calculate the atomic name based on the atom's atomic mass.
        """
        self._name = {v: k for k, v in atomic_numbers_to_masses.items()}[self.atomic_mass]

    def _calculate_symbol_from_mass(self):
        """
        Calculate the atomic symbol based on the atom's atomic mass.
        """
        atomic_number = {v: k for k, v in atomic_numbers_to_masses.items()}[self.atomic_mass]
        self._symbol = atomic_numbers_to_symbols[atomic_number]

    def _calculate_atomic_number_from_mass(self):
        """
        Calculate the atomic number based on the atom's atomic mass.
        """
        self._atomic_number = {v: k for k, v in atomic_numbers_to_masses.items()}[self.atomic_mass]

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
        return round(self._atomic_mass * KG_TO_AU, 3)

    @name.setter
    @recalculate("mass_from_name")
    @recalculate("symbol_from_name")
    @recalculate("atomic_number_from_name")
    def name(self, value: str):
        self.validate_string(value, "name")
        self._name = value

    @symbol.setter
    @recalculate("atomic_number_from_symbol")
    @recalculate("mass_from_symbol")
    @recalculate("name_from_symbol")
    def symbol(self, value: str):
        self.validate_string(value, "symbol")
        self._symbol = value

    @atomic_number.setter
    @recalculate("symbol_from_atomic_number")
    @recalculate("mass_from_atomic_number")
    @recalculate("name_from_atomic_number")
    def atomic_number(self, value: int):
        self.validate_positive_int(value, "atomic_number")
        self._atomic_number = value

    @atomic_mass.setter
    @recalculate("name_from_mass")
    @recalculate("symbol_from_mass")
    @recalculate("atomic_number_from_mass")
    def atomic_mass(self, value: float):
        self.validate_positive_float(value, "atomic_mass")
        self._atomic_mass = value * AU_TO_KG  




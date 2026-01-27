"""
Fuel material classes.

Classes:
    NaturalGas: Natural gas properties for combustion calculations

Volumeless, weightless property classes - just characteristics.
All properties in SI units.
"""
from steer_core.Mixins.TypeChecker import ValidationMixin
from steer_core.Mixins.Serializer import SerializerMixin
from steer_core.Mixins.Dunder import DunderMixin


class NaturalGas(
    ValidationMixin,
    DunderMixin,
    SerializerMixin
):
    """Natural gas properties for boiler calculations.
    
    Values are for typical pipeline-quality natural gas (mainly methane).
    All values in SI units (J/kg).
    """
    
    # Lower Heating Value (net calorific value) [J/kg]
    LHV = 47.0e6
    
    # Higher Heating Value (gross calorific value) [J/kg]
    HHV = 52.2e6

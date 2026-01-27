"""
Liquid material classes with thermodynamic properties.

Classes:
    Water: Pure water properties
    Steam: Steam properties

Volumeless, weightless property classes - just characteristics.
All properties in SI units (Pa, K, J/mol, etc).
"""
from steer_core.Constants.Units import (
    K_TO_C, 
    C_TO_K,
    BAR_TO_PA,
    PA_TO_BAR,
)
from steer_core.Mixins.TypeChecker import ValidationMixin
from steer_core.Mixins.Serializer import SerializerMixin
from steer_core.Mixins.Dunder import DunderMixin
from steer_core.Mixins.Thermodynamics import ThermodynamicsMixin


class Water(
    ThermodynamicsMixin,
    ValidationMixin,
    DunderMixin,
    SerializerMixin
):
    """Water thermodynamic properties.
    
    All values in SI units.
    """
    
    # Molecular weight [kg/mol]
    MW = 0.018015
    
    # Latent heat of vaporization [J/kg] at 100°C
    LAMBDA_VAPORIZATION = 2260000.0
    
    # Heat capacity [J/(kg·K)]
    CP = 4180.0
    
    # Density [kg/m³]
    RHO = 1000.0
    
    # NIST Antoine parameters for water vapor pressure
    # log10(P_bar) = A - B / (T_K + C)
    ANTOINE_A = 5.19621
    ANTOINE_B = 1730.63
    ANTOINE_C = -39.724
    
    @classmethod
    def vapor_pressure(cls, T: float) -> float:
        """Calculate water vapor pressure at given temperature.
        
        Args:
            T: Temperature [K]
            
        Returns:
            Vapor pressure [Pa]
        """
        # T is in Kelvin for this NIST equation
        P_bar = cls.antoine_pressure(T, cls.ANTOINE_A, cls.ANTOINE_B, cls.ANTOINE_C)
        return P_bar * BAR_TO_PA  # bar to Pa


# Alias for Water class
H2O = Water


class Steam(
    ThermodynamicsMixin,
    ValidationMixin,
    DunderMixin,
    SerializerMixin
):
    """Steam thermodynamic properties.
    
    Reference: Steam tables (IAPWS-IF97)
    All values in SI units (J/kg).
    """
    
    # Latent heat of vaporization [J/kg]
    # At different pressures for reboiler calculations
    LAMBDA_LP = 2200000.0    # ~2-3 bar (LP steam, ~120-135°C)
    LAMBDA_MP = 2015000.0    # ~10 bar (MP steam, ~180°C)
    LAMBDA_6BAR = 2086000.0  # 6 bar saturated (~159°C)

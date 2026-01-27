"""
Gas material classes with thermodynamic properties.

Classes:
    CO2: Carbon dioxide
    N2: Nitrogen  
    FlueGas: Combustion flue gas / air properties

All properties in SI units.
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


class CO2(
    ThermodynamicsMixin,
    ValidationMixin,
    DunderMixin,
    SerializerMixin
):
    """Carbon dioxide thermodynamic properties.
    
    Volumeless, weightless property class - just characteristics.
    All values in SI units.
    """
    
    # Molecular weight [kg/mol]
    MW = 0.04401
    
    # Heat capacity [J/(kg·K)] (Gas phase, STP)
    CP = 844.0
    
    # Density [kg/m³] (Gas phase, STP)
    RHO = 1.84
    
    # Antoine equation coefficients for sublimation curve
    # log10(P) = A - B / (T + C)
    # Valid range: approximately -120°C to -60°C
    ANTOINE_A = 9.81
    ANTOINE_B = 1347.79
    ANTOINE_C = 273.0
    
    # Phase change enthalpies [J/kg]
    H_SUBLIMATION = 571000.0  # solid → gas
    H_FUSION = 196000.0  # solid → liquid
    
    # Heat capacities [J/(kg·K)]
    CP_SOLID = 950.0
    CP_LIQUID = 2500.0
    
    # Triple point
    T_TRIPLE = 216.55  # K (-56.6°C)
    P_TRIPLE = 5.18e5  # Pa
    
    # Typical pipeline conditions
    P_PIPELINE = 150e5  # Pa (150 bar)
    RHO_LIQUID = 1100.0  # kg/m³
    
    @classmethod
    def sublimation_pressure(cls, T: float) -> float:
        """Calculate CO2 sublimation pressure at given temperature.
        
        Args:
            T: Temperature [K]
            
        Returns:
            Pressure [Pa]
        """
        # Antoine equation gives mmHg, convert to Pa
        T_celsius = T + K_TO_C  # Convert K to C
        P_mmhg = cls.antoine_pressure(T_celsius, cls.ANTOINE_A, cls.ANTOINE_B, cls.ANTOINE_C)
        return P_mmhg * 133.322  # mmHg to Pa
    
    @classmethod
    def sublimation_temperature(cls, P: float) -> float:
        """Calculate CO2 sublimation temperature at given pressure.
        
        Args:
            P: Pressure [Pa]
            
        Returns:
            Temperature [K]
        """
        P_mmhg = P / 133.322  # Pa to mmHg
        T_celsius = cls.antoine_temperature(P_mmhg, cls.ANTOINE_A, cls.ANTOINE_B, cls.ANTOINE_C)
        return T_celsius + C_TO_K  # Convert C to K


class N2(
    ThermodynamicsMixin,
    ValidationMixin,
    DunderMixin,
    SerializerMixin
):
    """Nitrogen properties.
    
    Volumeless, weightless property class - just characteristics.
    All values in SI units.
    """
    
    # Molecular weight [kg/mol]
    MW = 0.02801
    
    # Heat capacity [J/(kg·K)] (Gas phase, STP)
    CP = 1040.0
    
    # Density [kg/m³] (Gas phase, STP)
    RHO = 1.15


class FlueGas(
    ThermodynamicsMixin,
    ValidationMixin,
    DunderMixin,
    SerializerMixin
):
    """Flue gas and air properties.
    
    Typical values for combustion flue gas.
    Exact values depend on fuel composition.
    
    Volumeless, weightless property class - just characteristics.
    All values in SI units.
    """
    
    # Molecular weight [kg/mol]
    MW = 0.029  # Approximate for air-like mixture
    
    # Heat capacity [J/(kg·K)]
    CP = 1050.0
    
    # Density at ambient conditions (~25°C, 1 atm) [kg/m³]
    RHO = 1.2

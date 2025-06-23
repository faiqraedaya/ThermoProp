"""
Mixture component implementation for ThermoProp application
"""

from typing import Optional
from CoolProp.CoolProp import PropsSI

class MixtureComponent:
    """Class to represent a component in a mixture"""
    
    def __init__(self, name: str, mole_fraction: float = 0.0, mass_fraction: float = 0.0):
        """
        Initialize a mixture component
        
        Args:
            name: Name of the fluid component
            mole_fraction: Mole fraction of the component (0-1)
            mass_fraction: Mass fraction of the component (0-1)
        """
        self.name = name
        self.mole_fraction = mole_fraction
        self.mass_fraction = mass_fraction
        self.molecular_weight: Optional[float] = None
        
        # Get molecular weight if available
        try:
            self.molecular_weight = PropsSI('M', self.name) * 1000  # g/mol
        except:
            self.molecular_weight = 1.0  # Default value
    
    def __str__(self) -> str:
        """String representation of the component"""
        return f"{self.name} (x={self.mole_fraction:.4f}, y={self.mass_fraction:.4f})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the component"""
        return (f"MixtureComponent(name='{self.name}', "
                f"mole_fraction={self.mole_fraction}, "
                f"mass_fraction={self.mass_fraction}, "
                f"molecular_weight={self.molecular_weight})")
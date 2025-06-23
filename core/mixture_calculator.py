"""
Mixture calculator implementation for ThermoProp application
"""

from typing import Dict, List, Tuple, Optional, Union, Any
import numpy as np
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PropsSI, PhaseSI
from CoolProp.HumidAirProp import HAPropsSI

from .mixture_component import MixtureComponent

class MixtureCalculator:
    """Enhanced calculator for pure components and mixtures"""
    
    def __init__(self):
        """Initialize the mixture calculator"""
        self.fluids = self._get_available_fluids()
        self.mixture_models = ['Ideal Gas', 'Humid Air']
        self.property_map = {
            'Molar Mass': ('M', 'kg/mol'),
            'Density': ('D', 'kg/m³'),
            'Enthalpy': ('H', 'J/kg'),
            'Entropy': ('S', 'J/kg/K'),
            'Internal Energy': ('U', 'J/kg'),
            'Isobaric Mass Heat Capacity': ('Cpmass', 'J/kg/K'),
            'Isochoric Mass Heat Capacity': ('Cvmass', 'J/kg/K'),
            'Isobaric Molar Heat Capacity': ('Cpmolar', 'J/mol/K'),
            'Isochoric Molar Heat Capacity': ('Cvmolar', 'J/mol/K'),
            'Viscosity': ('V', 'Pa·s'),
            'Thermal Conductivity': ('L', 'W/m/K'),
            'Speed of Sound': ('A', 'm/s'),
            'Surface Tension': ('I', 'N/m'),
            'Quality': ('Q', '-'),
            'Phase': ('Phase', '-'),
            'Gibbs Free Energy': ('G', 'J/kg'),
            'Compressibility Factor': ('Z', '-'),
            'Joule-Thomson Coefficient': ('isenthalpic_expansion_coefficient', 'K/Pa'),
            'Isothermal Compressibility': ('isothermal_compressibility', '1/Pa'),
            'Isentropic Bulk Modulus': ('isentropic_bulk_modulus', 'Pa'),
        }
        
        # Common mixture systems
        self.predefined_mixtures = {
            'Air': [
                ('Nitrogen', 0.78084),
                ('Oxygen', 0.20946),
                ('Argon', 0.00934),
                ('CO2', 0.00036)
            ],
            'Natural Gas (Typical)': [
                ('Methane', 0.85),
                ('Ethane', 0.10),
                ('Propane', 0.03),
                ('n-Butane', 0.015),
                ('CO2', 0.005)
            ],
            'Flue Gas (Coal)': [
                ('CO2', 0.12),
                ('H2O', 0.08),
                ('Nitrogen', 0.75),
                ('Oxygen', 0.05)
            ]
        }
    
    def _get_available_fluids(self) -> List[str]:
        """
        Get comprehensive list of available fluids
        
        Returns:
            List of available fluid names
        """
        try:
            fluid_list = CP.get_global_param_string("FluidsList").split(',')
            
            # Add common fluids and aliases
            common_fluids = [
                'Water', 'Air', 'Nitrogen', 'Oxygen', 'CO2', 'Methane', 'Ethane',
                'Propane', 'n-Butane', 'i-Butane', 'n-Pentane', 'i-Pentane',
                'Ammonia', 'R134a', 'R410A', 'R22', 'R404A', 'R407C', 'R32',
                'Hydrogen', 'Helium', 'Argon', 'Benzene', 'Toluene', 'Ethanol',
                'Acetone', 'CarbonMonoxide', 'SulfurDioxide', 'HydrogenSulfide'
            ]
            
            all_fluids = list(set(fluid_list + common_fluids))
            all_fluids.sort()
            return all_fluids
        except Exception as e:
            print(f"Warning: Failed to get fluid list: {str(e)}")
            # Fallback list
            return ['Water', 'Air', 'Nitrogen', 'Oxygen', 'CO2', 'Methane', 'Propane']
    
    def calculate_mixture_properties(
        self, 
        components: List[MixtureComponent], 
        T: float, 
        P: float, 
        model: str = 'Ideal Gas'
    ) -> Tuple[Optional[Dict[str, Tuple[float, str]]], Optional[str]]:
        """
        Calculate mixture properties using specified model
        
        Args:
            components: List of mixture components
            T: Temperature in K
            P: Pressure in Pa
            model: Mixture model to use ('Ideal Gas' or 'Humid Air')
            
        Returns:
            Tuple of (results dictionary, error message if any)
        """
        if not components:
            return None, "No components provided"
        
        if model not in self.mixture_models:
            return None, f"Invalid model: {model}"
        
        try:
            if model == 'Humid Air':
                return self._calculate_humid_air(components, T, P)
            else:
                return self._calculate_ideal_gas_mixture(components, T, P)
                
        except Exception as e:
            return None, f"Calculation error: {str(e)}"
    
    def _calculate_ideal_gas_mixture(
        self, 
        components: List[MixtureComponent], 
        T: float, 
        P: float
    ) -> Tuple[Dict[str, Tuple[float, str]], None]:
        """
        Calculate mixture properties using ideal gas mixing rules
        
        Args:
            components: List of mixture components
            T: Temperature in K
            P: Pressure in Pa
            
        Returns:
            Tuple of (results dictionary, None)
            
        Raises:
            ValueError: If total mole fractions is zero
        """
        results = {}
        
        # Normalize mole fractions
        total_moles = sum(comp.mole_fraction for comp in components)
        if total_moles == 0:
            raise ValueError("Total mole fractions cannot be zero")
        
        # Calculate mixture molecular weight
        M_mix = sum(comp.mole_fraction * comp.molecular_weight for comp in components) / total_moles
        results['Molar Mass'] = (M_mix / 1000, 'kg/mol')  # Convert to kg/mol
        
        # Calculate mixture density (ideal gas law)
        R = 8314.462618  # J/kmol/K
        rho_mix = (P * M_mix) / (R * T)
        results['Density'] = (rho_mix, 'kg/m³')
        
        # Calculate mixture properties using mixing rules
        Cp_mix = 0
        Cv_mix = 0
        mu_mix = 0
        k_mix = 0
        
        for comp in components:
            if comp.mole_fraction > 0:
                try:
                    # Get pure component properties
                    Cp_i = PropsSI('Cpmass', 'T', T, 'P', P, comp.name)
                    Cv_i = PropsSI('Cvmass', 'T', T, 'P', P, comp.name)
                    mu_i = PropsSI('V', 'T', T, 'P', P, comp.name)
                    k_i = PropsSI('L', 'T', T, 'P', P, comp.name)
                    
                    # Mass-weighted mixing for heat capacities
                    mass_frac = (comp.mole_fraction * comp.molecular_weight) / M_mix
                    Cp_mix += mass_frac * Cp_i
                    Cv_mix += mass_frac * Cv_i
                    
                    # Mole-weighted mixing for transport properties (approximation)
                    mole_frac = comp.mole_fraction / total_moles
                    mu_mix += mole_frac * mu_i
                    k_mix += mole_frac * k_i
                    
                except Exception as e:
                    print(f"Warning: Failed to calculate properties for {comp.name}: {str(e)}")
                    continue
        
        results['Isobaric Heat Capacity'] = (Cp_mix, 'J/kg/K')
        results['Isochoric Heat Capacity'] = (Cv_mix, 'J/kg/K')
        results['Viscosity'] = (mu_mix, 'Pa·s')
        results['Thermal Conductivity'] = (k_mix, 'W/m/K')
        
        # Calculate other properties
        gamma = Cp_mix / Cv_mix if Cv_mix > 0 else 1.4
        a_mix = np.sqrt(gamma * R * T / M_mix)  # Speed of sound
        results['Speed of Sound'] = (a_mix, 'm/s')
        
        # Compressibility factor (ideal gas = 1)
        results['Compressibility Factor'] = (1.0, '-')
        
        # Enthalpy and entropy (reference state dependent)
        h_mix = Cp_mix * T  # Simplified
        s_mix = Cp_mix * np.log(T) - (R/M_mix) * np.log(P)  # Simplified
        results['Enthalpy'] = (h_mix, 'J/kg')
        results['Entropy'] = (s_mix, 'J/kg/K')
        
        return results, None
    
    def _calculate_humid_air(
        self, 
        components: List[MixtureComponent], 
        T: float, 
        P: float
    ) -> Tuple[Dict[str, Tuple[float, str]], None]:
        """
        Calculate humid air properties
        
        Args:
            components: List of mixture components
            T: Temperature in K
            P: Pressure in Pa
            
        Returns:
            Tuple of (results dictionary, None)
        """
        try:
            # Find water and air components
            water_fraction = 0
            for comp in components:
                if comp.name.lower() in ['water', 'h2o']:
                    water_fraction = comp.mole_fraction
                    break
            
            # Convert to relative humidity (approximation)
            P_sat = PropsSI('P', 'T', T, 'Q', 0, 'Water')
            RH = min(water_fraction * P / P_sat, 1.0)
            
            results = {}
            results['Density'] = (HAPropsSI('Vha', 'T', T, 'P', P, 'R', RH), 'kg/m³')
            results['Enthalpy'] = (HAPropsSI('H', 'T', T, 'P', P, 'R', RH), 'J/kg')
            results['Entropy'] = (HAPropsSI('S', 'T', T, 'P', P, 'R', RH), 'J/kg/K')
            results['Relative Humidity'] = (RH * 100, '%')
            results['Humidity Ratio'] = (HAPropsSI('W', 'T', T, 'P', P, 'R', RH), 'kg/kg')
            
            return results, None
            
        except Exception as e:
            print(f"Warning: Humid air calculation failed: {str(e)}")
            return self._calculate_ideal_gas_mixture(components, T, P)
    
    def calculate_saturation_properties(
        self, 
        fluid: str, 
        sat_type: str, 
        sat_value: float, 
        sat_unit: str
    ) -> Dict[str, Tuple[float, str]]:
        """
        Calculate saturation properties
        
        Args:
            fluid: Fluid name
            sat_type: Saturation type ('T' for temperature or 'P' for pressure)
            sat_value: Saturation value
            sat_unit: Unit of the saturation value
            
        Returns:
            Dictionary of saturation properties
            
        Raises:
            ValueError: If invalid saturation type or unit
        """
        try:
            # Convert to SI
            if sat_type == 'T':
                temp_si = self._convert_to_si(sat_value, sat_unit, 'T')
                psat = PropsSI('P', 'T', temp_si, 'Q', 0, fluid)
                temp_sat = temp_si
            elif sat_type == 'P':
                pres_si = self._convert_to_si(sat_value, sat_unit, 'P')
                temp_sat = PropsSI('T', 'P', pres_si, 'Q', 0, fluid)
                psat = pres_si
            else:
                raise ValueError(f"Invalid saturation type: {sat_type}")
            
            # Calculate liquid and vapor properties
            results = {
                'Saturation Temperature': (temp_sat, 'K'),
                'Saturation Pressure': (psat, 'Pa'),
                'Liquid Density': (PropsSI('D', 'T', temp_sat, 'Q', 0, fluid), 'kg/m³'),
                'Vapor Density': (PropsSI('D', 'T', temp_sat, 'Q', 1, fluid), 'kg/m³'),
                'Liquid Enthalpy': (PropsSI('H', 'T', temp_sat, 'Q', 0, fluid), 'J/kg'),
                'Vapor Enthalpy': (PropsSI('H', 'T', temp_sat, 'Q', 1, fluid), 'J/kg'),
                'Liquid Entropy': (PropsSI('S', 'T', temp_sat, 'Q', 0, fluid), 'J/kg/K'),
                'Vapor Entropy': (PropsSI('S', 'T', temp_sat, 'Q', 1, fluid), 'J/kg/K'),
                'Latent Heat': (PropsSI('H', 'T', temp_sat, 'Q', 1, fluid) - 
                              PropsSI('H', 'T', temp_sat, 'Q', 0, fluid), 'J/kg')
            }
            
            return results
            
        except Exception as e:
            raise ValueError(f"Failed to calculate saturation properties: {str(e)}")
    
    def _convert_to_si(self, value: float, unit: str, prop_type: str) -> float:
        """
        Convert a value to SI units
        
        Args:
            value: Value to convert
            unit: Current unit
            prop_type: Property type ('T' for temperature, 'P' for pressure)
            
        Returns:
            Value in SI units
            
        Raises:
            ValueError: If invalid unit or property type
        """
        if prop_type == 'T':
            if unit == 'K':
                return value
            elif unit in ['°C', 'C']:
                return value + 273.15
            elif unit in ['°F', 'F']:
                return (value - 32) * 5/9 + 273.15
            else:
                raise ValueError(f"Invalid temperature unit: {unit}")
        elif prop_type == 'P':
            if unit == 'Pa':
                return value
            elif unit == 'kPa':
                return value * 1000
            elif unit == 'MPa':
                return value * 1e6
            elif unit == 'bar':
                return value * 1e5
            elif unit == 'bara':
                return value * 1e5
            elif unit == 'barg':
                return (value + 1.01325) * 1e5
            elif unit == 'atm':
                return value * 101325
            elif unit == 'psi':
                return value * 6894.76
            elif unit == 'psia':
                return value * 6894.76
            elif unit == 'psig':
                return (value + 14.696) * 6894.76
            else:
                raise ValueError(f"Invalid pressure unit: {unit}")
        else:
            raise ValueError(f"Invalid property type: {prop_type}")
    
    def calculate_single_point_properties(
        self, 
        fluid: str, 
        prop1: str, 
        prop1_value: float, 
        prop1_unit: str,
        prop2: str, 
        prop2_value: float, 
        prop2_unit: str
    ) -> Dict[str, Tuple[float, str]]:
        """
        Calculate single point properties for a pure fluid
        
        Args:
            fluid: Fluid name
            prop1: First property type ('T', 'P', 'H', 'D', 'S', 'U')
            prop1_value: First property value
            prop1_unit: First property unit
            prop2: Second property type ('T', 'P', 'H', 'D', 'S', 'U')
            prop2_value: Second property value
            prop2_unit: Second property unit
            
        Returns:
            Dictionary of calculated properties
            
        Raises:
            ValueError: If invalid properties or calculation fails
        """
        try:
            # Convert inputs to SI units
            prop1_si = self._convert_to_si(prop1_value, prop1_unit, prop1)
            prop2_si = self._convert_to_si(prop2_value, prop2_unit, prop2)
            
            # Map property names to CoolProp format
            prop_map = {
                'T': 'T', 'P': 'P', 'H': 'H', 'D': 'D', 'S': 'S', 'U': 'U'
            }
            
            prop1_cp = prop_map.get(prop1)
            prop2_cp = prop_map.get(prop2)
            
            if not prop1_cp or not prop2_cp:
                raise ValueError(f"Invalid property types: {prop1}, {prop2}")
            
            # Helper to safely get properties
            def safe_props_si(prop, unit):
                try:
                    val = PropsSI(prop, prop1_cp, prop1_si, prop2_cp, prop2_si, fluid)
                    return (val, unit)
                except Exception:
                    return (np.nan, unit)

            # Calculate all properties using CoolProp
            results = {}
            
            # Basic properties
            results['Temperature'] = safe_props_si('T', 'K')
            results['Pressure'] = safe_props_si('P', 'Pa')
            results['Density'] = safe_props_si('D', 'kg/m³')
            results['Enthalpy'] = safe_props_si('H', 'J/kg')
            results['Entropy'] = safe_props_si('S', 'J/kg/K')
            results['Internal Energy'] = safe_props_si('U', 'J/kg')
            
            # Heat capacities
            results['Isobaric Heat Capacity'] = safe_props_si('Cpmass', 'J/kg/K')
            results['Isochoric Heat Capacity'] = safe_props_si('Cvmass', 'J/kg/K')
            
            # Transport properties
            results['Viscosity'] = safe_props_si('V', 'Pa·s')
            results['Thermal Conductivity'] = safe_props_si('L', 'W/m/K')
            
            # Other properties
            results['Speed of Sound'] = safe_props_si('A', 'm/s')
            results['Surface Tension'] = safe_props_si('I', 'N/m')
            results['Quality'] = safe_props_si('Q', '-')
            
            # Phase information
            try:
                phase = PhaseSI(prop1_cp, prop1_si, prop2_cp, prop2_si, fluid)
                results['Phase'] = (phase, '-')
            except:
                results['Phase'] = ('Unknown', '-')
            
            # Molar properties
            results['Molar Mass'] = safe_props_si('M', 'kg/mol')
            results['Molar Enthalpy'] = safe_props_si('Hmolar', 'J/mol')
            results['Molar Entropy'] = safe_props_si('Smolar', 'J/mol/K')
            
            return results
            
        except Exception as e:
            raise ValueError(f"Failed to calculate properties: {str(e)}")

    def simulate_process_path(
        self,
        fluid: str,
        process_type: str,
        initial_T: float,
        initial_P: float,
        final_value: float,
        num_points: int = 50,
        polytropic_n: float = 1.3  # Only used for polytropic
    ) -> dict:
        """
        Simulate a process path for a pure fluid.
        Args:
            fluid: Fluid name
            process_type: Type of process (Isobaric, Isochoric, Isothermal, Isenthalpic, Isentropic, Polytropic, Custom)
            initial_T: Initial temperature (K)
            initial_P: Initial pressure (Pa)
            final_value: Final value (depends on process)
            num_points: Number of points along the path
            polytropic_n: Polytropic exponent (for polytropic only)
        Returns:
            Dictionary with arrays for each property along the path
        """
        import numpy as np
        from CoolProp.CoolProp import PropsSI

        # Prepare arrays
        T_arr = []
        P_arr = []
        H_arr = []
        S_arr = []
        D_arr = []
        U_arr = []
        Q_arr = []
        phase_arr = []

        def safe_float(val):
            return float('nan') if val is None else val

        # Set up path
        if process_type == 'Isobaric':
            P0 = safe_float(initial_P)
            T0 = safe_float(initial_T)
            T1 = safe_float(final_value)
            T_points = np.linspace(T0, T1, num_points)
            for T in T_points:
                try:
                    P = P0
                    H = PropsSI('H', 'T', T, 'P', P, fluid)
                    S = PropsSI('S', 'T', T, 'P', P, fluid)
                    D = PropsSI('D', 'T', T, 'P', P, fluid)
                    U = PropsSI('U', 'T', T, 'P', P, fluid)
                    Q = PropsSI('Q', 'T', T, 'P', P, fluid)
                    phase = PropsSI('Phase', 'T', T, 'P', P, fluid)
                    for v in [H, S, D, U, Q]:
                        if v is None:
                            v = float('nan')
                except Exception:
                    H = S = D = U = Q = float('nan')
                    phase = 'Unknown'
                T_arr.append(T)
                P_arr.append(P)
                H_arr.append(H if H is not None else float('nan'))
                S_arr.append(S if S is not None else float('nan'))
                D_arr.append(D if D is not None else float('nan'))
                U_arr.append(U if U is not None else float('nan'))
                Q_arr.append(Q if Q is not None else float('nan'))
                phase_arr.append(phase)
        elif process_type == 'Isothermal':
            T = safe_float(initial_T)
            P0 = safe_float(initial_P)
            P1 = safe_float(final_value)
            P_points = np.linspace(P0, P1, num_points)
            for P in P_points:
                try:
                    H = PropsSI('H', 'T', T, 'P', P, fluid)
                    S = PropsSI('S', 'T', T, 'P', P, fluid)
                    D = PropsSI('D', 'T', T, 'P', P, fluid)
                    U = PropsSI('U', 'T', T, 'P', P, fluid)
                    Q = PropsSI('Q', 'T', T, 'P', P, fluid)
                    phase = PropsSI('Phase', 'T', T, 'P', P, fluid)
                    for v in [H, S, D, U, Q]:
                        if v is None:
                            v = float('nan')
                except Exception:
                    H = S = D = U = Q = float('nan')
                    phase = 'Unknown'
                T_arr.append(T)
                P_arr.append(P)
                H_arr.append(H if H is not None else float('nan'))
                S_arr.append(S if S is not None else float('nan'))
                D_arr.append(D if D is not None else float('nan'))
                U_arr.append(U if U is not None else float('nan'))
                Q_arr.append(Q if Q is not None else float('nan'))
                phase_arr.append(phase)
        elif process_type == 'Isochoric':
            try:
                D0 = PropsSI('D', 'T', safe_float(initial_T), 'P', safe_float(initial_P), fluid)
                D0 = safe_float(D0)
            except Exception:
                D0 = float('nan')
            T0 = safe_float(initial_T)
            T1 = safe_float(final_value)
            T_points = np.linspace(T0, T1, num_points)
            for T in T_points:
                try:
                    P = PropsSI('P', 'T', T, 'D', D0, fluid)
                    H = PropsSI('H', 'T', T, 'D', D0, fluid)
                    S = PropsSI('S', 'T', T, 'D', D0, fluid)
                    U = PropsSI('U', 'T', T, 'D', D0, fluid)
                    Q = PropsSI('Q', 'T', T, 'D', D0, fluid)
                    phase = PropsSI('Phase', 'T', T, 'D', D0, fluid)
                    for v in [P, H, S, U, Q]:
                        if v is None:
                            v = float('nan')
                except Exception:
                    P = H = S = U = Q = float('nan')
                    phase = 'Unknown'
                T_arr.append(T)
                P_arr.append(P if P is not None else float('nan'))
                H_arr.append(H if H is not None else float('nan'))
                S_arr.append(S if S is not None else float('nan'))
                D_arr.append(D0)
                U_arr.append(U if U is not None else float('nan'))
                Q_arr.append(Q if Q is not None else float('nan'))
                phase_arr.append(phase)
        elif process_type == 'Isenthalpic':
            try:
                H0 = PropsSI('H', 'T', safe_float(initial_T), 'P', safe_float(initial_P), fluid)
                H0 = safe_float(H0)
            except Exception:
                H0 = float('nan')
            P0 = safe_float(initial_P)
            P1 = safe_float(final_value)
            P_points = np.linspace(P0, P1, num_points)
            for P in P_points:
                try:
                    T = PropsSI('T', 'P', P, 'H', H0, fluid)
                    S = PropsSI('S', 'P', P, 'H', H0, fluid)
                    D = PropsSI('D', 'P', P, 'H', H0, fluid)
                    U = PropsSI('U', 'P', P, 'H', H0, fluid)
                    Q = PropsSI('Q', 'P', P, 'H', H0, fluid)
                    phase = PropsSI('Phase', 'P', P, 'H', H0, fluid)
                    for v in [T, S, D, U, Q]:
                        if v is None:
                            v = float('nan')
                except Exception:
                    T = S = D = U = Q = float('nan')
                    phase = 'Unknown'
                T_arr.append(T if T is not None else float('nan'))
                P_arr.append(P)
                H_arr.append(H0)
                S_arr.append(S if S is not None else float('nan'))
                D_arr.append(D if D is not None else float('nan'))
                U_arr.append(U if U is not None else float('nan'))
                Q_arr.append(Q if Q is not None else float('nan'))
                phase_arr.append(phase)
        elif process_type == 'Isentropic':
            try:
                S0 = PropsSI('S', 'T', safe_float(initial_T), 'P', safe_float(initial_P), fluid)
                S0 = safe_float(S0)
            except Exception:
                S0 = float('nan')
            P0 = safe_float(initial_P)
            P1 = safe_float(final_value)
            P_points = np.linspace(P0, P1, num_points)
            for P in P_points:
                try:
                    T = PropsSI('T', 'P', P, 'S', S0, fluid)
                    H = PropsSI('H', 'P', P, 'S', S0, fluid)
                    D = PropsSI('D', 'P', P, 'S', S0, fluid)
                    U = PropsSI('U', 'P', P, 'S', S0, fluid)
                    Q = PropsSI('Q', 'P', P, 'S', S0, fluid)
                    phase = PropsSI('Phase', 'P', P, 'S', S0, fluid)
                    for v in [T, H, D, U, Q]:
                        if v is None:
                            v = float('nan')
                except Exception:
                    T = H = D = U = Q = float('nan')
                    phase = 'Unknown'
                T_arr.append(T if T is not None else float('nan'))
                P_arr.append(P)
                H_arr.append(H if H is not None else float('nan'))
                S_arr.append(S0)
                D_arr.append(D if D is not None else float('nan'))
                U_arr.append(U if U is not None else float('nan'))
                Q_arr.append(Q if Q is not None else float('nan'))
                phase_arr.append(phase)
        elif process_type == 'Polytropic':
            P0 = safe_float(initial_P)
            T0 = safe_float(initial_T)
            P1 = safe_float(final_value)
            P_points = np.linspace(P0, P1, num_points)
            for P in P_points:
                try:
                    if P0 == 0 or np.isnan(P0) or np.isnan(T0):
                        T = float('nan')
                    else:
                        T = T0 * (P / P0) ** ((polytropic_n - 1) / polytropic_n)
                    T = safe_float(T)
                    H = safe_float(PropsSI('H', 'T', T, 'P', P, fluid))
                    S = safe_float(PropsSI('S', 'T', T, 'P', P, fluid))
                    D = safe_float(PropsSI('D', 'T', T, 'P', P, fluid))
                    U = safe_float(PropsSI('U', 'T', T, 'P', P, fluid))
                    Q = safe_float(PropsSI('Q', 'T', T, 'P', P, fluid))
                    try:
                        phase = PropsSI('Phase', 'T', T, 'P', P, fluid)
                    except Exception:
                        phase = 'Unknown'
                except Exception:
                    T = H = S = D = U = Q = float('nan')
                    phase = 'Unknown'
                T_arr.append(T)
                P_arr.append(P)
                H_arr.append(H)
                S_arr.append(S)
                D_arr.append(D)
                U_arr.append(U)
                Q_arr.append(Q)
                phase_arr.append(phase)
        else:
            # Custom or unsupported process
            raise NotImplementedError(f"Process type '{process_type}' not implemented.")

        return {
            'Temperature': np.array(T_arr),
            'Pressure': np.array(P_arr),
            'Enthalpy': np.array(H_arr),
            'Entropy': np.array(S_arr),
            'Density': np.array(D_arr),
            'Internal Energy': np.array(U_arr),
            'Quality': np.array(Q_arr),
            'Phase': np.array(phase_arr)
        }
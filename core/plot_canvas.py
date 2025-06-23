import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from CoolProp.CoolProp import PropsSI

class PlotCanvas(FigureCanvas):
    """Enhanced matplotlib canvas with more plotting capabilities"""
    
    def __init__(self, parent=None, width=12, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
    def plot_diagram(self, fluid, plot_type, show_grid=True, show_legend=True, 
                    x_axis='Auto', y_axis='Auto'):
        """Enhanced plot generation with customization options"""
        self.fig.clear()
        
        try:
            if plot_type == 'T-S Diagram':
                self._plot_ts_diagram(fluid, show_grid, show_legend)
            elif plot_type == 'P-H Diagram':
                self._plot_ph_diagram(fluid, show_grid, show_legend)
            elif plot_type == 'P-V Diagram':
                self._plot_pv_diagram(fluid, show_grid, show_legend)
            elif plot_type == 'H-S Diagram':
                self._plot_hs_diagram(fluid, show_grid, show_legend)
            elif plot_type == 'Property vs Temperature':
                self._plot_property_vs_temp(fluid, show_grid, show_legend)
            elif plot_type == 'Property vs Pressure':
                self._plot_property_vs_pressure(fluid, show_grid, show_legend)
            elif plot_type == 'Saturation Curves':
                self._plot_saturation_curve(fluid, show_grid, show_legend)
            elif plot_type == 'Phase Envelope':
                self._plot_phase_envelope(fluid, show_grid, show_legend)
            elif plot_type == 'Custom Plot':
                self._plot_custom(fluid, x_axis, y_axis, show_grid, show_legend)
            
            self.fig.tight_layout()
            self.draw()
            
        except Exception as e:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Plot generation failed:\n{str(e)}', 
                   transform=ax.transAxes, ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            self.draw()
    
    def _plot_ts_diagram(self, fluid, show_grid=True, show_legend=True):
        """Plot Temperature-Entropy diagram"""
        ax = self.fig.add_subplot(111)
        try:
            # Get critical properties
            Tc = PropsSI('Tcrit', fluid)
            # Generate saturation curve
            T_sat = np.linspace(273.16, Tc * 0.99, 100)
            S_liq, S_vap = [], []
            for T in T_sat:
                try:
                    S_liq.append(PropsSI('S', 'T', T, 'Q', 0, fluid))
                    S_vap.append(PropsSI('S', 'T', T, 'Q', 1, fluid))
                except:
                    S_liq.append(np.nan)
                    S_vap.append(np.nan)
            # Plot saturation curves
            ax.plot(np.array(S_liq)/1000, T_sat - 273.15, 'b-', linewidth=2, label='Saturated Liquid')
            ax.plot(np.array(S_vap)/1000, T_sat - 273.15, 'r-', linewidth=2, label='Saturated Vapor')
            ax.set_xlabel('Entropy (kJ/kg·K)')
            ax.set_ylabel('Temperature (°C)')
            ax.set_title(f'T-S Diagram for {fluid}')
            if show_grid:
                ax.grid(True, alpha=0.3)
            if show_legend:
                ax.legend()
        except Exception as e:
            raise Exception(f"T-S diagram error: {str(e)}")

    def _plot_hs_diagram(self, fluid, show_grid=True, show_legend=True):
        """Plot Enthalpy-Entropy diagram"""
        ax = self.fig.add_subplot(111)
        
        try:
            # Get critical properties
            Tc = PropsSI('Tcrit', fluid)
            Pc = PropsSI('Pcrit', fluid)
            
            # Generate saturation curve
            T_sat = np.linspace(273.16, Tc * 0.99, 100)
            H_liq, H_vap, S_liq, S_vap = [], [], [], []
            
            for T in T_sat:
                try:
                    H_liq.append(PropsSI('H', 'T', T, 'Q', 0, fluid))
                    H_vap.append(PropsSI('H', 'T', T, 'Q', 1, fluid))
                    S_liq.append(PropsSI('S', 'T', T, 'Q', 0, fluid))
                    S_vap.append(PropsSI('S', 'T', T, 'Q', 1, fluid))
                except:
                    H_liq.append(np.nan)
                    H_vap.append(np.nan)
                    S_liq.append(np.nan)
                    S_vap.append(np.nan)
            
            # Plot saturation curves
            ax.plot(np.array(S_liq)/1000, np.array(H_liq)/1000, 'b-', 
                   linewidth=2, label='Saturated Liquid')
            ax.plot(np.array(S_vap)/1000, np.array(H_vap)/1000, 'r-', 
                   linewidth=2, label='Saturated Vapor')
            
            # Add isobars
            pressures = [0.1, 0.5, 1.0, 5.0, 10.0]  # bar
            for P in pressures:
                if P * 100000 < Pc:
                    T_range = np.linspace(273.16, min(Tc * 1.2, 500), 50)
                    H_isobar, S_isobar = [], []
                    
                    for T in T_range:
                        try:
                            H = PropsSI('H', 'T', T, 'P', P * 100000, fluid)
                            S = PropsSI('S', 'T', T, 'P', P * 100000, fluid)
                            H_isobar.append(H)
                            S_isobar.append(S)
                        except:
                            continue
                    
                    if len(H_isobar) > 5:
                        ax.plot(np.array(S_isobar)/1000, np.array(H_isobar)/1000, 
                               '--', alpha=0.7, label=f'{P} bar')
            
            ax.set_xlabel('Entropy (kJ/kg·K)')
            ax.set_ylabel('Enthalpy (kJ/kg)')
            ax.set_title(f'H-S Diagram for {fluid}')
            
            if show_grid:
                ax.grid(True, alpha=0.3)
            if show_legend:
                ax.legend()
                
        except Exception as e:
            raise Exception(f"H-S diagram error: {str(e)}")

    def _plot_property_vs_temp(self, fluid, show_grid=True, show_legend=True):
        """Plot various properties vs temperature at constant pressure"""
        try:
            T_range = np.linspace(273.16, 373.15, 100)  # 0-100°C
            P_const = 101325  # 1 atm
            
            properties = {
                'Density': [],
                'Viscosity': [],
                'Thermal Conductivity': [],
                'Specific Heat (Cp)': []
            }
            
            for T in T_range:
                try:
                    properties['Density'].append(PropsSI('D', 'T', T, 'P', P_const, fluid))
                    properties['Viscosity'].append(PropsSI('V', 'T', T, 'P', P_const, fluid) * 1000)
                    properties['Thermal Conductivity'].append(PropsSI('L', 'T', T, 'P', P_const, fluid))
                    properties['Specific Heat (Cp)'].append(PropsSI('Cpmass', 'T', T, 'P', P_const, fluid) / 1000)
                except:
                    for prop in properties:
                        properties[prop].append(np.nan)
            
            # Clear the figure and create subplots
            self.fig.clear()
            ax1 = self.fig.add_subplot(221)
            ax2 = self.fig.add_subplot(222)
            ax3 = self.fig.add_subplot(223)
            ax4 = self.fig.add_subplot(224)
            
            # Plot each property
            ax1.plot(T_range - 273.15, properties['Density'], 'b-', linewidth=2)
            ax1.set_ylabel('Density (kg/m³)')
            ax1.set_xlabel('Temperature (°C)')
            ax1.grid(True, alpha=0.3)
            ax1.set_title('Density vs Temperature')
            
            ax2.plot(T_range - 273.15, properties['Viscosity'], 'r-', linewidth=2)
            ax2.set_ylabel('Viscosity (mPa·s)')
            ax2.set_xlabel('Temperature (°C)')
            ax2.grid(True, alpha=0.3)
            ax2.set_title('Viscosity vs Temperature')
            
            ax3.plot(T_range - 273.15, properties['Thermal Conductivity'], 'g-', linewidth=2)
            ax3.set_ylabel('Thermal Conductivity (W/m·K)')
            ax3.set_xlabel('Temperature (°C)')
            ax3.grid(True, alpha=0.3)
            ax3.set_title('Thermal Conductivity vs Temperature')
            
            ax4.plot(T_range - 273.15, properties['Specific Heat (Cp)'], 'm-', linewidth=2)
            ax4.set_ylabel('Specific Heat Cp (kJ/kg·K)')
            ax4.set_xlabel('Temperature (°C)')
            ax4.grid(True, alpha=0.3)
            ax4.set_title('Specific Heat vs Temperature')
            
            self.fig.suptitle(f'Property Variations for {fluid} at 1 atm')
            self.fig.tight_layout()
            self.draw()
            
        except Exception as e:
            raise Exception(f"Property vs Temperature plot error: {str(e)}")

    def _plot_property_vs_pressure(self, fluid, show_grid=True, show_legend=True):
        """Plot properties vs pressure at constant temperature"""
        try:
            P_range = np.logspace(3, 7, 100)  # 1 kPa to 10 MPa
            T_const = 298.15  # 25°C
            
            properties = {
                'Density': [],
                'Viscosity': [],
                'Thermal Conductivity': [],
                'Compressibility Factor': []
            }
            
            P_valid = []
            
            for P in P_range:
                try:
                    rho = PropsSI('D', 'T', T_const, 'P', P, fluid)
                    mu = PropsSI('V', 'T', T_const, 'P', P, fluid) * 1000  # mPa·s
                    k = PropsSI('L', 'T', T_const, 'P', P, fluid)
                    
                    # Calculate compressibility factor
                    M = PropsSI('M', fluid)
                    R = 8314.462618  # J/kmol/K
                    Z = P / (rho * R * T_const / M)
                    
                    properties['Density'].append(rho)
                    properties['Viscosity'].append(mu)
                    properties['Thermal Conductivity'].append(k)
                    properties['Compressibility Factor'].append(Z)
                    P_valid.append(P)
                    
                except:
                    continue
            
            # Clear the figure and create subplots
            self.fig.clear()
            ax1 = self.fig.add_subplot(221)
            ax2 = self.fig.add_subplot(222)
            ax3 = self.fig.add_subplot(223)
            ax4 = self.fig.add_subplot(224)
            
            P_bar = np.array(P_valid) / 100000  # Convert to bar
            
            ax1.semilogx(P_bar, properties['Density'], 'b-', linewidth=2)
            ax1.set_ylabel('Density (kg/m³)')
            ax1.set_xlabel('Pressure (bar)')
            ax1.set_title('Density vs Pressure')
            if show_grid:
                ax1.grid(True, alpha=0.3)
            
            ax2.semilogx(P_bar, properties['Viscosity'], 'r-', linewidth=2)
            ax2.set_ylabel('Viscosity (mPa·s)')
            ax2.set_xlabel('Pressure (bar)')
            ax2.set_title('Viscosity vs Pressure')
            if show_grid:
                ax2.grid(True, alpha=0.3)
            
            ax3.semilogx(P_bar, properties['Thermal Conductivity'], 'g-', linewidth=2)
            ax3.set_ylabel('Thermal Conductivity (W/m·K)')
            ax3.set_xlabel('Pressure (bar)')
            ax3.set_title('Thermal Conductivity vs Pressure')
            if show_grid:
                ax3.grid(True, alpha=0.3)
            
            ax4.semilogx(P_bar, properties['Compressibility Factor'], 'm-', linewidth=2)
            ax4.set_ylabel('Compressibility Factor (-)')
            ax4.set_xlabel('Pressure (bar)')
            ax4.set_title('Compressibility Factor vs Pressure')
            ax4.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='Ideal Gas')
            if show_grid:
                ax4.grid(True, alpha=0.3)
            if show_legend:
                ax4.legend()
            
            self.fig.suptitle(f'Property Variations for {fluid} at 25°C')
            self.fig.tight_layout()
            self.draw()
            
        except Exception as e:
            raise Exception(f"Property vs Pressure plot error: {str(e)}")
    
    def plot_saturation_curve(self, T_sat, P_sat, rho_liq, rho_vap, fluid, show_grid=True, show_legend=True):
        """Plot saturation curve data"""
        self.fig.clear()
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        T_celsius = np.array(T_sat) - 273.15
        P_bar = np.array(P_sat) / 100000
        
        # Temperature vs Pressure
        ax1.semilogy(T_celsius, P_bar, 'b-', linewidth=2)
        ax1.set_xlabel('Temperature (°C)')
        ax1.set_ylabel('Pressure (bar)')
        ax1.set_title('Saturation Pressure vs Temperature')
        ax1.grid(True, alpha=0.3)
        
        # Density vs Temperature
        ax2.plot(T_celsius, rho_liq, 'b-', linewidth=2, label='Liquid')
        ax2.plot(T_celsius, rho_vap, 'r-', linewidth=2, label='Vapor')
        ax2.set_xlabel('Temperature (°C)')
        ax2.set_ylabel('Density (kg/m³)')
        ax2.set_title('Saturation Density vs Temperature')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # P-V diagram
        V_liq = 1.0 / np.array(rho_liq)
        V_vap = 1.0 / np.array(rho_vap)
        ax3.loglog(V_liq, P_bar, 'b-', linewidth=2, label='Liquid')
        ax3.loglog(V_vap, P_bar, 'r-', linewidth=2, label='Vapor')
        ax3.set_xlabel('Specific Volume (m³/kg)')
        ax3.set_ylabel('Pressure (bar)')
        ax3.set_title('P-V Saturation Curve')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Density ratio
        density_ratio = np.array(rho_liq) / np.array(rho_vap)
        ax4.semilogy(T_celsius, density_ratio, 'g-', linewidth=2)
        ax4.set_xlabel('Temperature (°C)')
        ax4.set_ylabel('Density Ratio (ρ_liq/ρ_vap)')
        ax4.set_title('Liquid/Vapor Density Ratio')
        ax4.grid(True, alpha=0.3)
        
        fig.suptitle(f'Saturation Properties for {fluid}')
        fig.tight_layout()
        
        # Replace the original figure
        self.fig = fig
        self.draw()
    
    def plot_process_path(self, results, process_type, fluid, show_grid=True, show_legend=True):
        """Plot process path results"""
        self.fig.clear()
        
        try:
            # Create subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            
            T_data = np.array(results['Temperature']) - 273.15  # Convert to °C
            P_data = np.array(results['Pressure']) / 100000     # Convert to bar
            
            # Remove NaN values
            valid_idx = ~(np.isnan(T_data) | np.isnan(P_data))
            T_valid = T_data[valid_idx]
            P_valid = P_data[valid_idx]
            
            # T-P diagram
            ax1.plot(T_valid, P_valid, 'b-', linewidth=2, marker='o', markersize=3)
            ax1.set_xlabel('Temperature (°C)')
            ax1.set_ylabel('Pressure (bar)')
            ax1.set_title(f'{process_type} Process - T-P Path')
            ax1.grid(True, alpha=0.3)
            
            # Property evolution
            if 'Enthalpy' in results:
                H_data = np.array(results['Enthalpy'])[valid_idx] / 1000  # kJ/kg
                ax2.plot(T_valid, H_data, 'r-', linewidth=2, marker='s', markersize=3)
                ax2.set_xlabel('Temperature (°C)')
                ax2.set_ylabel('Enthalpy (kJ/kg)')
                ax2.set_title('Enthalpy vs Temperature')
                ax2.grid(True, alpha=0.3)
            
            if 'Density' in results:
                rho_data = np.array(results['Density'])[valid_idx]
                ax3.plot(T_valid, rho_data, 'g-', linewidth=2, marker='^', markersize=3)
                ax3.set_xlabel('Temperature (°C)')
                ax3.set_ylabel('Density (kg/m³)')
                ax3.set_title('Density vs Temperature')
                ax3.grid(True, alpha=0.3)
            
            if 'Entropy' in results:
                S_data = np.array(results['Entropy'])[valid_idx] / 1000  # kJ/kg/K
                ax4.plot(T_valid, S_data, 'm-', linewidth=2, marker='d', markersize=3)
                ax4.set_xlabel('Temperature (°C)')
                ax4.set_ylabel('Entropy (kJ/kg·K)')
                ax4.set_title('Entropy vs Temperature')
                ax4.grid(True, alpha=0.3)
            
            fig.suptitle(f'{process_type} Process for {fluid}')
            fig.tight_layout()
            
            # Replace the original figure
            self.fig = fig
            self.draw()
            
        except Exception as e:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Process plot failed:\n{str(e)}', 
                   transform=ax.transAxes, ha='center', va='center')
            self.draw()
    
    def _plot_ph_diagram(self, fluid, show_grid=True, show_legend=True):
        """Plot Pressure-Enthalpy diagram"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        try:
            # Get critical properties
            Tc = PropsSI('Tcrit', fluid)
            
            # Generate saturation curve
            T_sat = np.linspace(273.16, Tc * 0.99, 100)
            H_liq, H_vap, P_sat = [], [], []
            
            for T in T_sat:
                try:
                    P = PropsSI('P', 'T', T, 'Q', 0, fluid)
                    H_liq.append(PropsSI('H', 'T', T, 'Q', 0, fluid))
                    H_vap.append(PropsSI('H', 'T', T, 'Q', 1, fluid))
                    P_sat.append(P)
                except:
                    continue
                    
            # Plot saturation curves
            ax.plot(np.array(H_liq)/1000, np.array(P_sat)/100000, 'b-', 
                   linewidth=2, label='Saturated Liquid')
            ax.plot(np.array(H_vap)/1000, np.array(P_sat)/100000, 'r-', 
                   linewidth=2, label='Saturated Vapor')
            
            ax.set_xlabel('Enthalpy (kJ/kg)')
            ax.set_ylabel('Pressure (bar)')
            ax.set_title(f'P-H Diagram for {fluid}')
            ax.set_yscale('log')
            if show_legend:
                ax.legend()
            if show_grid:
                ax.grid(True, alpha=0.3)
            
        except Exception as e:
            raise Exception(f"P-H diagram error: {str(e)}")
    
    def _plot_pv_diagram(self, fluid, show_grid=True, show_legend=True):
        """Plot Pressure-Volume diagram"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        try:
            # Get critical properties
            Tc = PropsSI('Tcrit', fluid)
            
            # Generate saturation curve
            T_sat = np.linspace(273.16, Tc * 0.99, 50)
            V_liq, V_vap, P_sat = [], [], []
            
            for T in T_sat:
                try:
                    P = PropsSI('P', 'T', T, 'Q', 0, fluid)
                    rho_liq = PropsSI('D', 'T', T, 'Q', 0, fluid)
                    rho_vap = PropsSI('D', 'T', T, 'Q', 1, fluid)
                    V_liq.append(1.0 / rho_liq)
                    V_vap.append(1.0 / rho_vap)
                    P_sat.append(P)
                except:
                    continue
                    
            # Plot saturation curves
            ax.plot(V_liq, np.array(P_sat)/100000, 'b-', linewidth=2, label='Saturated Liquid')
            ax.plot(V_vap, np.array(P_sat)/100000, 'r-', linewidth=2, label='Saturated Vapor')
            
            ax.set_xlabel('Specific Volume (m³/kg)')
            ax.set_ylabel('Pressure (bar)')
            ax.set_title(f'P-V Diagram for {fluid}')
            ax.set_xscale('log')
            ax.set_yscale('log')
            if show_legend:
                ax.legend()
            if show_grid:
                ax.grid(True, alpha=0.3)
            
        except Exception as e:
            raise Exception(f"P-V diagram error: {str(e)}")

    def _plot_saturation_curve(self, fluid, show_grid=True, show_legend=True):
        """Plot the saturation curve (P-T, density, etc.) for a pure fluid"""
        self.fig.clear()
        try:
            Tc = PropsSI('Tcrit', fluid)
            Ttriple = 273.16
            try:
                Ttriple = PropsSI('Ttriple', fluid)
            except:
                pass
            T_sat = np.linspace(Ttriple, Tc * 0.999, 100)
            P_sat, rho_liq, rho_vap = [], [], []
            for T in T_sat:
                try:
                    P_sat.append(PropsSI('P', 'T', T, 'Q', 0, fluid))
                    rho_liq.append(PropsSI('D', 'T', T, 'Q', 0, fluid))
                    rho_vap.append(PropsSI('D', 'T', T, 'Q', 1, fluid))
                except:
                    P_sat.append(np.nan)
                    rho_liq.append(np.nan)
                    rho_vap.append(np.nan)
            # Create subplots
            ax1 = self.fig.add_subplot(221)
            ax2 = self.fig.add_subplot(222)
            ax3 = self.fig.add_subplot(223)
            ax4 = self.fig.add_subplot(224)
            T_celsius = np.array(T_sat) - 273.15
            P_bar = np.array(P_sat) / 100000
            # T vs P
            ax1.semilogy(T_celsius, P_bar, 'b-', linewidth=2)
            ax1.set_xlabel('Temperature (°C)')
            ax1.set_ylabel('Pressure (bar)')
            ax1.set_title('Saturation Pressure vs Temperature')
            if show_grid:
                ax1.grid(True, alpha=0.3)
            # Density vs T
            ax2.plot(T_celsius, rho_liq, 'b-', linewidth=2, label='Liquid')
            ax2.plot(T_celsius, rho_vap, 'r-', linewidth=2, label='Vapor')
            ax2.set_xlabel('Temperature (°C)')
            ax2.set_ylabel('Density (kg/m³)')
            ax2.set_title('Saturation Density vs Temperature')
            if show_legend:
                ax2.legend()
            if show_grid:
                ax2.grid(True, alpha=0.3)
            # P-V diagram
            V_liq = 1.0 / np.array(rho_liq)
            V_vap = 1.0 / np.array(rho_vap)
            ax3.loglog(V_liq, P_bar, 'b-', linewidth=2, label='Liquid')
            ax3.loglog(V_vap, P_bar, 'r-', linewidth=2, label='Vapor')
            ax3.set_xlabel('Specific Volume (m³/kg)')
            ax3.set_ylabel('Pressure (bar)')
            ax3.set_title('P-V Saturation Curve')
            if show_legend:
                ax3.legend()
            if show_grid:
                ax3.grid(True, alpha=0.3)
            # Density ratio
            density_ratio = np.array(rho_liq) / np.array(rho_vap)
            ax4.semilogy(T_celsius, density_ratio, 'g-', linewidth=2)
            ax4.set_xlabel('Temperature (°C)')
            ax4.set_ylabel('Density Ratio (ρ_liq/ρ_vap)')
            ax4.set_title('Liquid/Vapor Density Ratio')
            if show_grid:
                ax4.grid(True, alpha=0.3)
            self.fig.suptitle(f'Saturation Properties for {fluid}')
            self.fig.tight_layout()
            self.draw()
        except Exception as e:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Saturation curve plot failed:\n{str(e)}',
                    transform=ax.transAxes, ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            self.draw()

    def _plot_phase_envelope(self, fluid, show_grid=True, show_legend=True):
        """Plot the phase envelope for a fluid or mixture with phase zones"""
        self.fig.clear()
        try:
            # Get critical and triple point properties
            Tc = PropsSI('Tcrit', fluid)
            Pc = PropsSI('Pcrit', fluid)
            Ttriple = 273.16
            try:
                Ttriple = PropsSI('Ttriple', fluid)
                Ptriple = PropsSI('Ptriple', fluid)
            except:
                Ptriple = 611.657  # Default for water if triple point not available
            
            # Generate saturation curve data with more points for smoother curves
            T_sat = np.linspace(Ttriple, Tc * 0.999, 200)
            P_sat = []
            for T in T_sat:
                try:
                    P_sat.append(PropsSI('P', 'T', T, 'Q', 0, fluid))
                except:
                    P_sat.append(np.nan)
            
            # Create plot
            ax = self.fig.add_subplot(111)
            
            # Convert to plotting units
            T_plot = T_sat - 273.15
            P_plot = np.array(P_sat) / 100000
            
            # Create upper and lower bounds for phase zones
            T_upper = np.linspace(Ttriple-273.15, Tc*1.5-273.15, 200)
            P_upper = np.full_like(T_upper, Pc*10/100000)
            
            # Plot phase zones with smooth boundaries
            # Liquid zone
            ax.fill_between(T_plot, P_plot, P_upper,
                          color='lightblue', alpha=0.3, label='Liquid')
            
            # Vapor zone
            ax.fill_between(T_plot, P_plot, 
                          np.full_like(T_plot, Ptriple/100000),
                          color='lightgreen', alpha=0.3, label='Vapor')
            
            # Supercritical zone
            ax.fill_between(T_upper, P_upper,
                          np.full_like(T_upper, Pc/100000),
                          color='lightyellow', alpha=0.3, label='Supercritical')
            
            # Plot saturation curve
            ax.semilogy(T_plot, P_plot, 'b-', linewidth=2, label='Phase Envelope')
            
            # Add critical point marker
            ax.plot(Tc-273.15, Pc/100000, 'ro', label='Critical Point')
            
            # Add labels and formatting
            ax.set_xlabel('Temperature (°C)')
            ax.set_ylabel('Pressure (bar)')
            ax.set_title(f'Phase Envelope for {fluid}')
            if show_grid:
                ax.grid(True, alpha=0.3)
            if show_legend:
                ax.legend()
            
            # Set reasonable axis limits
            ax.set_xlim(Ttriple-273.15, Tc*1.5-273.15)
            ax.set_ylim(Ptriple/100000, Pc*10/100000)
            
            self.fig.tight_layout()
            self.draw()
            
        except Exception as e:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Phase envelope plot failed:\n{str(e)}',
                    transform=ax.transAxes, ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            self.draw()

    def _plot_custom(self, fluid, x_axis, y_axis, show_grid=True, show_legend=True):
        """Plot a user-selected property on the x and y axes"""
        self.fig.clear()
        try:
            # Map axis names to CoolProp keys and labels
            axis_map = {
                'T': ('T', 'Temperature (°C)', lambda v: v - 273.15),
                'P': ('P', 'Pressure (bar)', lambda v: v / 100000),
                'H': ('H', 'Enthalpy (kJ/kg)', lambda v: v / 1000),
                'S': ('S', 'Entropy (kJ/kg·K)', lambda v: v / 1000),
                'D': ('D', 'Density (kg/m³)', lambda v: v),
                'V': ('V', 'Specific Volume (m³/kg)', lambda v: v),
            }
            # Default axes
            if x_axis == 'Auto':
                x_axis = 'T'
            if y_axis == 'Auto':
                y_axis = 'P'
            if x_axis not in axis_map or y_axis not in axis_map:
                raise ValueError('Invalid axis selection')
            x_key, x_label, x_conv = axis_map[x_axis]
            y_key, y_label, y_conv = axis_map[y_axis]
            # Choose a reasonable range for x
            if x_key == 'T':
                Tc = PropsSI('Tcrit', fluid)
                Tmin = 273.16
                try:
                    Tmin = PropsSI('Ttriple', fluid)
                except:
                    pass
                x_vals = np.linspace(Tmin, Tc * 0.99, 100)
                y_vals = []
                for x in x_vals:
                    try:
                        if y_key == 'V':
                            rho = PropsSI('D', 'T', x, 'P', 101325, fluid)
                            y = 1.0 / rho if rho > 0 else np.nan
                        else:
                            y = PropsSI(y_key, 'T', x, 'P', 101325, fluid)
                        y_vals.append(y)
                    except:
                        y_vals.append(np.nan)
                x_plot = x_conv(x_vals)
                y_plot = [y_conv(y) if y is not None and not np.isnan(y) else np.nan for y in y_vals]
            elif x_key == 'P':
                Pc = PropsSI('Pcrit', fluid)
                x_vals = np.logspace(4, np.log10(Pc * 0.99), 100)  # 0.1 bar to near critical
                y_vals = []
                for x in x_vals:
                    try:
                        if y_key == 'V':
                            rho = PropsSI('D', 'T', 298.15, 'P', x, fluid)
                            y = 1.0 / rho if rho > 0 else np.nan
                        else:
                            y = PropsSI(y_key, 'T', 298.15, 'P', x, fluid)
                        y_vals.append(y)
                    except:
                        y_vals.append(np.nan)
                x_plot = x_conv(x_vals)
                y_plot = [y_conv(y) if y is not None and not np.isnan(y) else np.nan for y in y_vals]
            else:
                # For other axes, use T as the sweep variable
                Tc = PropsSI('Tcrit', fluid)
                Tmin = 273.16
                try:
                    Tmin = PropsSI('Ttriple', fluid)
                except:
                    pass
                x_vals = np.linspace(Tmin, Tc * 0.99, 100)
                y_vals = []
                for x in x_vals:
                    try:
                        if x_key == 'V':
                            rho = PropsSI('D', 'T', x, 'P', 101325, fluid)
                            x_val = 1.0 / rho if rho > 0 else np.nan
                        else:
                            x_val = PropsSI(x_key, 'T', x, 'P', 101325, fluid)
                        if y_key == 'V':
                            rho = PropsSI('D', 'T', x, 'P', 101325, fluid)
                            y_val = 1.0 / rho if rho > 0 else np.nan
                        else:
                            y_val = PropsSI(y_key, 'T', x, 'P', 101325, fluid)
                        y_vals.append((x_val, y_val))
                    except:
                        y_vals.append((np.nan, np.nan))
                x_plot = [x_conv(x) if x is not None and not np.isnan(x) else np.nan for x, y in y_vals]
                y_plot = [y_conv(y) if y is not None and not np.isnan(y) else np.nan for x, y in y_vals]
            ax = self.fig.add_subplot(111)
            ax.plot(x_plot, y_plot, 'b-', linewidth=2, label=f'{y_label} vs {x_label}')
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title(f'{y_label} vs {x_label} for {fluid}')
            if show_grid:
                ax.grid(True, alpha=0.3)
            if show_legend:
                ax.legend()
            self.fig.tight_layout()
            self.draw()
        except Exception as e:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Custom plot failed:\n{str(e)}',
                    transform=ax.transAxes, ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            self.draw()

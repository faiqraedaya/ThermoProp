from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox, 
                             QComboBox, QLabel, QDoubleSpinBox, QPushButton, 
                             QTableWidget, QSplitter, QTableWidgetItem)
from PyQt5.QtCore import Qt
from core.plot_canvas import PlotCanvas
import numpy as np

class SaturationTab(QWidget):
    def __init__(self, calc, parent=None):
        super().__init__(parent)
        self.calc = calc
        self.init_ui()

    def init_ui(self):
        """Create enhanced saturation properties tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input section with multiple options
        input_group = QGroupBox("Saturation Calculation")
        input_layout = QGridLayout(input_group)
        
        # Fluid selection
        input_layout.addWidget(QLabel("Fluid:"), 0, 0)
        self.sat_fluid_combo = QComboBox()
        self.sat_fluid_combo.addItems(self.calc.fluids)
        self.sat_fluid_combo.setCurrentText('Water')
        input_layout.addWidget(self.sat_fluid_combo, 0, 1)
        
        # Input parameter
        input_layout.addWidget(QLabel("Given:"), 2, 0)
        self.sat_type_combo = QComboBox()
        self.sat_type_combo.addItems(['Temperature', 'Pressure'])
        input_layout.addWidget(self.sat_type_combo, 2, 1)
        
        # Value and unit
        self.sat_value = QDoubleSpinBox()
        self.sat_value.setRange(-273, 1000)
        self.sat_value.setValue(100)
        input_layout.addWidget(self.sat_value, 2, 2)
        
        self.sat_unit = QComboBox()
        self.sat_unit.addItems(['°C', 'K', '°F'])
        input_layout.addWidget(self.sat_unit, 2, 3)
        
        # Update units when type changes
        self.sat_type_combo.currentTextChanged.connect(self.update_sat_units)
        
        layout.addWidget(input_group)
        
        # Calculate button
        sat_calc_btn = QPushButton("Calculate")
        sat_calc_btn.clicked.connect(self.calculate_saturation)
        layout.addWidget(sat_calc_btn)
        
        # Results in splitter
        results_splitter = QSplitter(Qt.Horizontal)
        
        # Table results
        self.sat_results_table = QTableWidget()
        self.sat_results_table.setColumnCount(3)
        self.sat_results_table.setHorizontalHeaderLabels(['Property', 'Value', 'Unit'])
        results_splitter.addWidget(self.sat_results_table)
        
        # Plot canvas for saturation curve
        self.sat_plot_canvas = PlotCanvas(self, width=8, height=6)
        results_splitter.addWidget(self.sat_plot_canvas)
        
        layout.addWidget(results_splitter)
        
        self.setLayout(layout)

    def update_sat_units(self):
        """Update saturation units based on input type"""
        sat_type = self.sat_type_combo.currentText()
        self.sat_unit.clear()
        
        if sat_type == 'Temperature':
            self.sat_unit.addItems(['°C', 'K', '°F'])
            self.sat_value.setRange(-273, 1000)
            self.sat_value.setValue(100)
        else:  # Pressure
            self.sat_unit.addItems(['bar', 'kPa', 'MPa', 'atm', 'psi'])
            self.sat_value.setRange(0.001, 1000)
            self.sat_value.setValue(1.01325)

    def calculate_saturation(self):
        """Calculate saturation properties"""
        try:
            # Get input values
            fluid = self.sat_fluid_combo.currentText()
            sat_type = self.sat_type_combo.currentText()
            sat_value = self.sat_value.value()
            sat_unit = self.sat_unit.currentText()
            
            # Convert sat_type to single character
            if sat_type == 'Temperature':
                sat_type_char = 'T'
            else:
                sat_type_char = 'P'
            
            # Perform calculation
            results = self.calc.calculate_saturation_properties(
                fluid, sat_type_char, sat_value, sat_unit
            )
            
            # Display results
            self.display_saturation_results(results)
            
            # Update plot
            self.update_saturation_plot(fluid, sat_type_char, sat_value, sat_unit)
            
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Calculation Error", f"Failed to calculate saturation properties: {str(e)}")

    def display_saturation_results(self, results):
        """Display saturation calculation results"""
        self.sat_results_table.setRowCount(len(results))
        
        for i, (property_name, (value, unit)) in enumerate(results.items()):
            # Property name
            self.sat_results_table.setItem(i, 0, QTableWidgetItem(property_name))
            
            # Value (formatted)
            if isinstance(value, float) and (abs(value) < 1e-6 or abs(value) > 1e6):
                formatted_value = f"{value:.4e}"
            elif isinstance(value, float):
                formatted_value = f"{value:.6g}"
            else:
                formatted_value = str(value)
            self.sat_results_table.setItem(i, 1, QTableWidgetItem(formatted_value))
            
            # Unit
            self.sat_results_table.setItem(i, 2, QTableWidgetItem(unit))
        
        # Resize columns to content
        self.sat_results_table.resizeColumnsToContents()

    def update_saturation_plot(self, fluid, sat_type, sat_value, sat_unit):
        """Update saturation curve plot"""
        try:
            self.sat_plot_canvas.axes.clear()
            import CoolProp.CoolProp as CP
            import CoolProp
            # Generate saturation curve data
            if sat_type == 'T':
                # Temperature-based saturation curve
                # Convert input to SI (K)
                T_center = self.calc._convert_to_si(sat_value, sat_unit, 'T')
                # Get fluid critical and triple point
                try:
                    Tc = CP.PropsSI('Tcrit', fluid)
                except Exception:
                    Tc = T_center * 1.5
                try:
                    Ttriple = CP.PropsSI('Ttriple', fluid)
                except Exception:
                    Ttriple = 273.16
                T_min = max(Ttriple, T_center * 0.8)
                T_max = min(Tc * 0.99, T_center * 1.2)
                T_range = np.linspace(T_min, T_max, 50)
                P_sat = []
                for T in T_range:
                    try:
                        P = CP.PropsSI('P', 'T', T, 'Q', 0, fluid)
                        P_sat.append(P)
                    except Exception:
                        P_sat.append(np.nan)
                self.sat_plot_canvas.axes.semilogy(T_range, P_sat, 'b-', label=f'{fluid} Saturation')
                self.sat_plot_canvas.axes.set_xlabel('Temperature (K)')
                self.sat_plot_canvas.axes.set_ylabel('Saturation Pressure (Pa)')
                self.sat_plot_canvas.axes.set_title(f'{fluid} Saturation Curve (P vs T)')
            else:
                # Pressure-based saturation curve
                # Convert input to SI (Pa)
                P_center = self.calc._convert_to_si(sat_value, sat_unit, 'P')
                # Get fluid critical and triple point
                try:
                    Pc = CP.PropsSI('Pcrit', fluid)
                except Exception:
                    Pc = P_center * 1.5
                try:
                    Ptriple = CP.PropsSI('Ptriple', fluid)
                except Exception:
                    Ptriple = 611.657
                P_min = max(Ptriple, P_center * 0.8)
                P_max = min(Pc * 0.99, P_center * 1.2)
                P_range = np.linspace(P_min, P_max, 50)
                T_sat = []
                for P in P_range:
                    try:
                        T = CP.PropsSI('T', 'P', P, 'Q', 0, fluid)
                        T_sat.append(T)
                    except Exception:
                        T_sat.append(np.nan)
                self.sat_plot_canvas.axes.plot(P_range, T_sat, 'r-', label=f'{fluid} Saturation')
                self.sat_plot_canvas.axes.set_xlabel('Saturation Pressure (Pa)')
                self.sat_plot_canvas.axes.set_ylabel('Temperature (K)')
                self.sat_plot_canvas.axes.set_title(f'{fluid} Saturation Curve (T vs P)')
            self.sat_plot_canvas.axes.legend()
            self.sat_plot_canvas.axes.grid(True)
            self.sat_plot_canvas.draw()
        except Exception as e:
            print(f"Warning: Failed to update saturation plot: {str(e)}")
            # Continue without plot update
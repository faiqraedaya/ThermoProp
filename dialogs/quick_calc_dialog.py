from CoolProp.CoolProp import PropsSI
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, 
    QComboBox, QTextEdit, QGroupBox, QDoubleSpinBox, QRadioButton, 
    QButtonGroup, QDialog, QDialogButtonBox,
)

from core.mixture_calculator import MixtureCalculator

class QuickCalcDialog(QDialog):
    """Quick calculation dialog for simple property lookups"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calc = MixtureCalculator()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Quick Property Calculator')
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout(self)
        
        # Fluid selection
        fluid_layout = QHBoxLayout()
        fluid_layout.addWidget(QLabel("Fluid:"))
        self.fluid_combo = QComboBox()
        self.fluid_combo.addItems(['Water', 'Air', 'Nitrogen', 'CO2', 'Methane'])
        fluid_layout.addWidget(self.fluid_combo)
        layout.addLayout(fluid_layout)
        
        # Quick presets
        preset_group = QGroupBox("Quick Presets")
        preset_layout = QVBoxLayout(preset_group)
        
        self.preset_buttons = QButtonGroup()
        
        stp_btn = QRadioButton("STP (0°C, 1 atm)")
        stp_btn.setChecked(True)
        self.preset_buttons.addButton(stp_btn, 0)
        preset_layout.addWidget(stp_btn)
        
        ntp_btn = QRadioButton("NTP (20°C, 1 atm)")
        self.preset_buttons.addButton(ntp_btn, 1)
        preset_layout.addWidget(ntp_btn)
        
        custom_btn = QRadioButton("Custom conditions")
        self.preset_buttons.addButton(custom_btn, 2)
        preset_layout.addWidget(custom_btn)
        
        layout.addWidget(preset_group)
        
        # Custom conditions
        self.custom_group = QGroupBox("Custom Conditions")
        custom_layout = QGridLayout(self.custom_group)
        
        custom_layout.addWidget(QLabel("Temperature:"), 0, 0)
        self.temp_input = QDoubleSpinBox()
        self.temp_input.setRange(-273, 1000)
        self.temp_input.setValue(25)
        self.temp_input.setSuffix(" °C")
        custom_layout.addWidget(self.temp_input, 0, 1)
        
        custom_layout.addWidget(QLabel("Pressure:"), 1, 0)
        self.pres_input = QDoubleSpinBox()
        self.pres_input.setRange(0.001, 1000)
        self.pres_input.setValue(1.01325)
        self.pres_input.setSuffix(" bar")
        custom_layout.addWidget(self.pres_input, 1, 1)
        
        self.custom_group.setEnabled(False)
        layout.addWidget(self.custom_group)
        
        # Connect preset buttons
        self.preset_buttons.buttonClicked.connect(self.preset_changed)
        
        # Calculate button
        calc_btn = QPushButton("Calculate")
        calc_btn.clicked.connect(self.calculate)
        layout.addWidget(calc_btn)
        
        # Results
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        layout.addWidget(self.results_text)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def preset_changed(self):
        """Handle preset selection change"""
        preset_id = self.preset_buttons.checkedId()
        
        if preset_id == 0:  # STP
            self.temp_input.setValue(0)
            self.pres_input.setValue(1.01325)
            self.custom_group.setEnabled(False)
        elif preset_id == 1:  # NTP
            self.temp_input.setValue(20)
            self.pres_input.setValue(1.01325)
            self.custom_group.setEnabled(False)
        else:  # Custom
            self.custom_group.setEnabled(True)
    
    def calculate(self):
        """Perform quick calculation"""
        try:
            fluid = self.fluid_combo.currentText()
            T = self.temp_input.value() + 273.15
            P = self.pres_input.value() * 100000
            
            # Calculate key properties
            results = {}
            results['Density'] = PropsSI('D', 'T', T, 'P', P, fluid)
            results['Viscosity'] = PropsSI('V', 'T', T, 'P', P, fluid) * 1000  # mPa·s
            results['Thermal Conductivity'] = PropsSI('L', 'T', T, 'P', P, fluid)
            results['Heat Capacity Mass'] = PropsSI('Cpmass', 'T', T, 'P', P, fluid) / 1000  # kJ/kg·K
            results['Speed of Sound'] = PropsSI('A', 'T', T, 'P', P, fluid)
            
            # Format results
            output = f"Quick Properties for {fluid}\n"
            output += f"T = {T-273.15:.1f}°C, P = {P/100000:.3f} bar\n"
            output += "-" * 40 + "\n"
            output += f"Density: {results['Density']:.3f} kg/m³\n"
            output += f"Viscosity: {results['Viscosity']:.4f} mPa·s\n"
            output += f"Thermal Conductivity: {results['Thermal Conductivity']:.4f} W/m·K\n"
            output += f"Heat Capacity Mass: {results['Heat Capacity Mass']:.3f} kJ/kg·K\n"
            output += f"Speed of Sound: {results['Speed of Sound']:.1f} m/s\n"
            
            self.results_text.setText(output)
            
        except Exception as e:
            self.results_text.setText(f"Calculation failed: {str(e)}")



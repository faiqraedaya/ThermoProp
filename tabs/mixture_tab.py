from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, 
                             QGroupBox, QComboBox, QLabel, QPushButton, 
                             QDoubleSpinBox, QTableWidget, QSplitter, 
                             QTextEdit, QMessageBox, QInputDialog, QTableWidgetItem)
from PyQt5.QtCore import Qt

class MixtureTab(QWidget):
    def __init__(self, calc, parent=None):
        super().__init__(parent)
        self.calc = calc
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Create mixture calculation tab"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Left panel - Mixture definition
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Mixture composition
        comp_group = QGroupBox("Mixture Composition")
        comp_layout = QVBoxLayout(comp_group)
        
        # Mixture model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.mixture_model = QComboBox()
        self.mixture_model.addItems(self.calc.mixture_models)
        model_layout.addWidget(self.mixture_model)
        comp_layout.addLayout(model_layout)
        
        # Mixture definition buttons
        btn_layout = QHBoxLayout()
        define_btn = QPushButton("Define Mixture")
        define_btn.clicked.connect(self.define_mixture)
        btn_layout.addWidget(define_btn)
        
        load_pred_btn = QPushButton("Load Predefined")
        load_pred_btn.clicked.connect(self.load_predefined_mixture)
        btn_layout.addWidget(load_pred_btn)
        
        comp_layout.addLayout(btn_layout)
        
        # Current mixture display
        self.mixture_display = QTextEdit()
        self.mixture_display.setMaximumHeight(150)
        self.mixture_display.setPlaceholderText("No mixture defined")
        comp_layout.addWidget(self.mixture_display)
        
        left_layout.addWidget(comp_group)
        
        # State conditions
        state_group = QGroupBox("State Conditions")
        state_layout = QGridLayout(state_group)
        
        state_layout.addWidget(QLabel("Temperature:"), 0, 0)
        self.mix_temp = QDoubleSpinBox()
        self.mix_temp.setRange(-273, 2000)
        self.mix_temp.setValue(25)
        self.mix_temp.setSuffix(" °C")
        state_layout.addWidget(self.mix_temp, 0, 1)
        
        state_layout.addWidget(QLabel("Pressure:"), 1, 0)
        self.mix_pres = QDoubleSpinBox()
        self.mix_pres.setRange(0.001, 1000)
        self.mix_pres.setValue(1.01325)
        self.mix_pres.setSuffix(" bar")
        state_layout.addWidget(self.mix_pres, 1, 1)
        
        left_layout.addWidget(state_group)
        
        # Calculate button
        mix_calc_btn = QPushButton("Calculate Mixture Properties")
        mix_calc_btn.setStyleSheet("QPushButton { font-size: 16px; padding: 12px; }")
        mix_calc_btn.clicked.connect(self.calculate_mixture)
        left_layout.addWidget(mix_calc_btn)
        
        left_layout.addStretch()
        
        # Right panel - Results
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Mixture results
        mix_results_group = QGroupBox("Mixture Properties")
        mix_results_layout = QVBoxLayout(mix_results_group)
        
        self.mixture_results_table = QTableWidget()
        self.mixture_results_table.setColumnCount(3)
        self.mixture_results_table.setHorizontalHeaderLabels(['Property', 'Value', 'Unit'])
        header = self.mixture_results_table.horizontalHeader()
        if header:
            header.setStretchLastSection(True)
        self.mixture_results_table.setAlternatingRowColors(True)
        mix_results_layout.addWidget(self.mixture_results_table)
        
        right_layout.addWidget(mix_results_group)
        
        # Component properties comparison
        comp_props_group = QGroupBox("Component Properties Comparison")
        comp_props_layout = QVBoxLayout(comp_props_group)
        
        self.component_table = QTableWidget()
        comp_props_layout.addWidget(self.component_table)
        
        right_layout.addWidget(comp_props_group)
        
        # Add panels to splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([500, 700])
        
        layout.addWidget(splitter)
        self.setLayout(layout)

    def define_mixture(self):
        """Define mixture composition"""
        if self.parent and hasattr(self.parent, 'open_mixture_designer'):
            self.parent.open_mixture_designer()
        else:
            QMessageBox.warning(self, "Error", 
                "Could not open mixture designer.")

    def load_predefined_mixture(self):
        """Load predefined mixture"""
        mixture_name, ok = QInputDialog.getItem(
            self, "Load Predefined Mixture", 
            "Select mixture:", 
            list(self.calc.predefined_mixtures.keys()), 
            0, False
        )
        
        if ok and mixture_name:
            components = self.calc.predefined_mixtures[mixture_name]
            self.display_mixture(components)
            QMessageBox.information(self, "Mixture Loaded", f"Loaded {mixture_name} mixture")

    def display_mixture(self, components):
        """Display mixture composition"""
        text = "Mixture Composition:\n"
        for name, fraction in components:
            text += f"  {name}: {fraction:.4f} (mole fraction)\n"
        self.mixture_display.setPlainText(text)

    def update_mixture_display(self, components):
        """Update mixture display from main window"""
        self.display_mixture(components)

    def calculate_mixture(self):
        """Calculate mixture properties"""
        try:
            # Get current mixture from display
            mixture_text = self.mixture_display.toPlainText()
            if "No mixture defined" in mixture_text or not mixture_text.strip():
                QMessageBox.warning(self, "No Mixture", "Please define a mixture first.")
                return
            
            # Get state conditions
            T = self.mix_temp.value() + 273.15  # Convert to K
            P = self.mix_pres.value() * 1e5     # Convert to Pa
            
            # For now, create a simple mixture for demonstration
            # In a real implementation, you would parse the mixture from the display
            from core.mixture_component import MixtureComponent
            
            # Create a simple air mixture for demonstration
            components = [
                MixtureComponent("Nitrogen", 0.78),
                MixtureComponent("Oxygen", 0.21),
                MixtureComponent("Argon", 0.01)
            ]
            
            # Calculate properties
            model = self.mixture_model.currentText()
            results, error = self.calc.calculate_mixture_properties(components, T, P, model)
            
            if error:
                QMessageBox.critical(self, "Calculation Error", f"Failed to calculate: {error}")
                return
            
            # Display results
            self.display_mixture_results(results)
            
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"Failed to calculate mixture properties: {str(e)}")

    def display_mixture_results(self, results):
        """Display mixture calculation results"""
        self.mixture_results_table.setRowCount(len(results))
        
        for i, (property_name, (value, unit)) in enumerate(results.items()):
            # Property name
            self.mixture_results_table.setItem(i, 0, QTableWidgetItem(property_name))
            
            # Value (formatted)
            if isinstance(value, float) and (abs(value) < 1e-6 or abs(value) > 1e6):
                formatted_value = f"{value:.4e}"
            elif isinstance(value, float):
                formatted_value = f"{value:.6g}"
            else:
                formatted_value = str(value)
            self.mixture_results_table.setItem(i, 1, QTableWidgetItem(formatted_value))
            
            # Unit
            self.mixture_results_table.setItem(i, 2, QTableWidgetItem(unit))
        
        # Resize columns to content
        self.mixture_results_table.resizeColumnsToContents()
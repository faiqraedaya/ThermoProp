from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, 
                             QGroupBox, QLineEdit, QComboBox, QLabel, 
                             QDoubleSpinBox, QPushButton, QTableWidget, 
                             QSplitter, QHeaderView, QTableWidgetItem)
from PyQt5.QtCore import Qt
import pandas as pd

class SinglePointTab(QWidget):
    def __init__(self, calc, parent=None):
        super().__init__(parent)
        self.calc = calc
        self.init_ui()

    def init_ui(self):
        """Create enhanced single point calculation tab"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Left panel - Input
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Fluid selection with search
        fluid_group = QGroupBox("Fluid Selection")
        fluid_layout = QVBoxLayout(fluid_group)
        
        self.fluid_search = QLineEdit()
        self.fluid_search.setPlaceholderText("Search fluids...")
        self.fluid_search.textChanged.connect(self.filter_fluids)
        fluid_layout.addWidget(self.fluid_search)
        
        self.fluid_combo = QComboBox()
        self._all_fluids = list(self.calc.fluids)  # Store full list for filtering
        self.fluid_combo.addItems(self._all_fluids)
        self.fluid_combo.setCurrentText('Water')
        self.fluid_combo.setEditable(True)
        fluid_layout.addWidget(self.fluid_combo)
        
        left_layout.addWidget(fluid_group)
        
        # Enhanced input section
        input_group = QGroupBox("State Point Definition")
        input_layout = QGridLayout(input_group)
        
        # Property 1
        input_layout.addWidget(QLabel("Property 1:"), 0, 0)
        self.prop1_combo = QComboBox()
        self.prop1_combo.addItems(['T', 'P', 'H', 'D', 'S', 'U'])
        input_layout.addWidget(self.prop1_combo, 0, 1)
        
        self.prop1_value = QDoubleSpinBox()
        self.prop1_value.setRange(-1000, 10000)
        self.prop1_value.setDecimals(6)
        self.prop1_value.setValue(25)
        input_layout.addWidget(self.prop1_value, 0, 2)
        
        self.prop1_unit = QComboBox()
        self.prop1_unit.addItems(['°C', 'K', '°F'])
        input_layout.addWidget(self.prop1_unit, 0, 3)
        
        # Property 2
        input_layout.addWidget(QLabel("Property 2:"), 1, 0)
        self.prop2_combo = QComboBox()
        self.prop2_combo.addItems(['T', 'P', 'H', 'D', 'S', 'U'])
        self.prop2_combo.setCurrentText('P')
        input_layout.addWidget(self.prop2_combo, 1, 1)
        
        self.prop2_value = QDoubleSpinBox()
        self.prop2_value.setRange(0.001, 1000)
        self.prop2_value.setDecimals(6)
        self.prop2_value.setValue(1.01325)
        input_layout.addWidget(self.prop2_value, 1, 2)
        
        self.prop2_unit = QComboBox()
        self.prop2_unit.addItems(['bara', 'barg', 'Pa', 'psia', 'psig', 'MPa'])
        input_layout.addWidget(self.prop2_unit, 1, 3)
        
        # Update unit combos when property type changes
        self.prop1_combo.currentTextChanged.connect(self.update_units)
        self.prop2_combo.currentTextChanged.connect(self.update_units)
        
        # Initialize units
        self.update_units(is_init=True)
        
        left_layout.addWidget(input_group)
        
        # Calculate button
        calc_btn = QPushButton("Calculate Properties")
        calc_btn.setStyleSheet("QPushButton { font-size: 16px; padding: 12px; }")
        calc_btn.clicked.connect(self.calculate_single_point)
        left_layout.addWidget(calc_btn)
        
        left_layout.addStretch()
        
        # Right panel - Results
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Results table with enhanced features
        results_group = QGroupBox("Calculation Results")
        results_layout = QVBoxLayout(results_group)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(['Property', 'Value', 'Unit'])
        header = self.results_table.horizontalHeader()
        if header:
            header.setStretchLastSection(True)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSortingEnabled(True)
        results_layout.addWidget(self.results_table)
        
        # Export options
        export_layout = QHBoxLayout()
        export_csv_btn = QPushButton("Export CSV")
        export_csv_btn.clicked.connect(self.export_results)
        export_layout.addWidget(export_csv_btn)
        
        export_excel_btn = QPushButton("Export Excel")
        export_excel_btn.clicked.connect(self.export_excel)
        export_layout.addWidget(export_excel_btn)
        
        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.clicked.connect(self.copy_results)
        export_layout.addWidget(copy_btn)
        
        results_layout.addLayout(export_layout)
        right_layout.addWidget(results_group)
        
        # Add panels to splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 800])
        
        layout.addWidget(splitter)
        self.setLayout(layout)

    def filter_fluids(self, text):
        """Filter fluids based on search text"""
        current_text = self.fluid_combo.currentText()
        filtered = [f for f in self._all_fluids if text.lower() in f.lower()]
        self.fluid_combo.blockSignals(True)
        self.fluid_combo.clear()
        self.fluid_combo.addItems(filtered)
        # Try to restore the current selection if possible
        if current_text in filtered:
            self.fluid_combo.setCurrentText(current_text)
        elif filtered:
            self.fluid_combo.setCurrentIndex(0)
        self.fluid_combo.blockSignals(False)

    def update_units(self, is_init=False):
        """Update unit options based on selected property type"""
        self.prop_to_unit_map = {
            'T': ['°C', 'K', '°F', '°R'],
            'P': ['Pa', 'kPa', 'MPa', 'bar', 'bara', 'barg', 'psi', 'psia', 'psig', 'atm'],
            'H': ['J/kg', 'kJ/kg', 'MJ/kg', 'J/mol', 'kJ/mol', 'BTU/lb'],
            'D': ['kg/m³', 'g/cm³', 'lb/ft³', 'kg/L'],
            'S': ['J/kg/K', 'kJ/kg/K', 'J/mol/K', 'kJ/mol/K'],
            'U': ['J/kg', 'kJ/kg', 'MJ/kg', 'J/mol', 'kJ/mol', 'BTU/lb']
        }
        
        if is_init:
            # Initial setup for both
            self._update_combo(self.prop1_combo, self.prop1_unit)
            self._update_combo(self.prop2_combo, self.prop2_unit)
        else:
            sender = self.sender()
            if sender == self.prop1_combo:
                self._update_combo(self.prop1_combo, self.prop1_unit)
            elif sender == self.prop2_combo:
                self._update_combo(self.prop2_combo, self.prop2_unit)

    def _update_combo(self, prop_combo, unit_combo):
        """Helper to update a single unit combo box"""
        prop = prop_combo.currentText()
        units = self.prop_to_unit_map.get(prop, [])
        
        current_unit = unit_combo.currentText()
        unit_combo.clear()
        if units:
            unit_combo.addItems(units)
            if current_unit in units:
                unit_combo.setCurrentText(current_unit)
            else:
                unit_combo.setCurrentIndex(0)

    def calculate_single_point(self):
        """Calculate properties for single point"""
        try:
            # Get input values
            fluid = self.fluid_combo.currentText()
            prop1 = self.prop1_combo.currentText()
            prop1_value = self.prop1_value.value()
            prop1_unit = self.prop1_unit.currentText()
            prop2 = self.prop2_combo.currentText()
            prop2_value = self.prop2_value.value()
            prop2_unit = self.prop2_unit.currentText()
            
            # Validate inputs
            if prop1 == prop2:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Input Error", "Property 1 and Property 2 must be different.")
                return
            
            # Perform calculation
            results = self.calc.calculate_single_point_properties(
                fluid, prop1, prop1_value, prop1_unit, prop2, prop2_value, prop2_unit
            )
            
            # Display results
            self.display_results(results)
            
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Calculation Error", f"Failed to calculate properties: {str(e)}")

    def display_results(self, results):
        """Display calculation results in the table"""
        self.results_table.setRowCount(len(results))
        
        for i, (property_name, (value, unit)) in enumerate(results.items()):
            # Property name
            self.results_table.setItem(i, 0, QTableWidgetItem(property_name))
            
            # Value (formatted)
            val_str = ""
            if isinstance(value, float) and (abs(value) < 1e-6 or abs(value) > 1e6):
                val_str = f"{value:.4e}"
            elif isinstance(value, float):
                val_str = f"{value:.6g}"
            else:
                val_str = str(value)
            
            self.results_table.setItem(i, 1, QTableWidgetItem(val_str))
            
            # Unit
            self.results_table.setItem(i, 2, QTableWidgetItem(unit))
        
        # Resize columns to content
        self.results_table.resizeColumnsToContents()

    def export_results(self):
        """Export results to CSV"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export Results", "", "CSV Files (*.csv)"
            )
            if filename:
                import pandas as pd
                
                # Get data from table
                data = []
                for row in range(self.results_table.rowCount()):
                    property_item = self.results_table.item(row, 0)
                    value_item = self.results_table.item(row, 1)
                    unit_item = self.results_table.item(row, 2)
                    
                    if property_item and value_item and unit_item:
                        property_name = property_item.text()
                        value = value_item.text()
                        unit = unit_item.text()
                        data.append([property_name, value, unit])
                
                if data:
                    df = pd.DataFrame(data, columns=['Property', 'Value', 'Unit'])
                    df.to_csv(filename, index=False)
                    
                    from PyQt5.QtWidgets import QMessageBox
                    QMessageBox.information(self, "Export Success", f"Results exported to {filename}")
                
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Export Error", f"Failed to export results: {str(e)}")

    def export_excel(self):
        """Export results to Excel"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export Results", "", "Excel Files (*.xlsx)"
            )
            if filename:
                import pandas as pd
                
                # Get data from table
                data = []
                for row in range(self.results_table.rowCount()):
                    property_item = self.results_table.item(row, 0)
                    value_item = self.results_table.item(row, 1)
                    unit_item = self.results_table.item(row, 2)
                    
                    if property_item and value_item and unit_item:
                        property_name = property_item.text()
                        value = value_item.text()
                        unit = unit_item.text()
                        data.append([property_name, value, unit])
                
                if data:
                    df = pd.DataFrame(data, columns=['Property', 'Value', 'Unit'])
                    df.to_excel(filename, index=False)
                    
                    from PyQt5.QtWidgets import QMessageBox
                    QMessageBox.information(self, "Export Success", f"Results exported to {filename}")
                
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Export Error", f"Failed to export results: {str(e)}")

    def copy_results(self):
        """Copy results to clipboard"""
        try:
            from PyQt5.QtWidgets import QApplication
            
            # Build text representation
            text = "Property\tValue\tUnit\n"
            for row in range(self.results_table.rowCount()):
                property_item = self.results_table.item(row, 0)
                value_item = self.results_table.item(row, 1)
                unit_item = self.results_table.item(row, 2)
                
                if property_item and value_item and unit_item:
                    property_name = property_item.text()
                    value = value_item.text()
                    unit = unit_item.text()
                    text += f"{property_name}\t{value}\t{unit}\n"
            
            # Copy to clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Copy Success", "Results copied to clipboard")
            
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Copy Error", f"Failed to copy results: {str(e)}")
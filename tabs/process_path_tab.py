from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QGroupBox, 
                             QComboBox, QLabel, QDoubleSpinBox, QPushButton, 
                             QTableWidget, QTabWidget, QTextEdit, QSpinBox, QMessageBox, QTableWidgetItem)
from PyQt5.QtCore import Qt
from core.plot_canvas import PlotCanvas
import numpy as np

class ProcessPathTab(QWidget):
    def __init__(self, calc, parent=None):
        super().__init__(parent)
        self.calc = calc
        self.init_ui()

    def init_ui(self):
        """Create process path simulation tab"""
        layout = QVBoxLayout(self)
        
        # Input section
        input_group = QGroupBox("Process Path Definition")
        input_layout = QGridLayout(input_group)
        
        # Fluid
        input_layout.addWidget(QLabel("Fluid:"), 0, 0)
        self.proc_fluid_combo = QComboBox()
        self.proc_fluid_combo.addItems(self.calc.fluids)
        self.proc_fluid_combo.setCurrentText('Water')
        input_layout.addWidget(self.proc_fluid_combo, 0, 1)
        
        # Initial state
        input_layout.addWidget(QLabel("Initial T (°C):"), 1, 0)
        self.init_temp = QDoubleSpinBox()
        self.init_temp.setRange(-273, 1000)
        self.init_temp.setValue(25)
        input_layout.addWidget(self.init_temp, 1, 1)
        
        input_layout.addWidget(QLabel("Initial P (bar):"), 1, 2)
        self.init_pres = QDoubleSpinBox()
        self.init_pres.setRange(0.001, 1000)
        self.init_pres.setValue(1.01325)
        input_layout.addWidget(self.init_pres, 1, 3)
        
        # Process type
        input_layout.addWidget(QLabel("Process:"), 2, 0)
        self.process_type = QComboBox()
        self.process_type.addItems([
            'Isobaric', 'Isochoric', 'Isothermal', 'Isenthalpic', 
            'Isentropic', 'Polytropic', 'Custom'
        ])
        input_layout.addWidget(self.process_type, 2, 1)
        
        # Final condition
        input_layout.addWidget(QLabel("Final Value:"), 2, 2)
        self.final_condition = QDoubleSpinBox()
        self.final_condition.setRange(-1000, 1000)
        self.final_condition.setValue(100)
        input_layout.addWidget(self.final_condition, 2, 3)
        
        # Number of points
        input_layout.addWidget(QLabel("Points:"), 3, 0)
        self.num_points = QSpinBox()
        self.num_points.setRange(10, 1000)
        self.num_points.setValue(50)
        input_layout.addWidget(self.num_points, 3, 1)
        
        layout.addWidget(input_group)
        
        # Calculate button
        proc_calc_btn = QPushButton("Simulate Process")
        proc_calc_btn.clicked.connect(self.simulate_process)
        layout.addWidget(proc_calc_btn)
        
        # Results in tabs
        results_tabs = QTabWidget()
        
        # Text results
        self.process_results = QTextEdit()
        results_tabs.addTab(self.process_results, "Summary")
        
        # Data table
        self.process_table = QTableWidget()
        results_tabs.addTab(self.process_table, "Data Table")
        
        # Process plot
        self.process_plot_canvas = PlotCanvas(self, width=10, height=6)
        results_tabs.addTab(self.process_plot_canvas, "Process Plot")
        
        layout.addWidget(results_tabs)
        
        self.setLayout(layout)

    def simulate_process(self):
        """Simulate process path"""
        try:
            # Gather user input
            fluid = self.proc_fluid_combo.currentText()
            initial_T = self.init_temp.value() + 273.15  # K
            initial_P = self.init_pres.value() * 1e5     # Pa
            process_type = self.process_type.currentText()
            final_value = self.final_condition.value()
            num_points = self.num_points.value()
            polytropic_n = 1.3
            if process_type == 'Polytropic':
                # Optionally, you could add a UI field for n
                pass

            # For isothermal, final_value is final P (bar), convert to Pa
            # For isobaric, final_value is final T (C), convert to K
            # For isochoric, final_value is final T (C), convert to K
            # For isenthalpic/isentropic/polytropic, final_value is final P (bar), convert to Pa
            if process_type in ['Isothermal', 'Isenthalpic', 'Isentropic', 'Polytropic']:
                final_value_si = final_value * 1e5  # bar to Pa
            else:
                final_value_si = final_value + 273.15  # C to K

            # Simulate process path
            results = self.calc.simulate_process_path(
                fluid=fluid,
                process_type=process_type,
                initial_T=initial_T,
                initial_P=initial_P,
                final_value=final_value_si,
                num_points=num_points,
                polytropic_n=polytropic_n
            )

            # Display summary
            summary = f"Process Path Simulation\n"
            summary += f"Fluid: {fluid}\n"
            summary += f"Process: {process_type}\n"
            summary += f"Initial T: {self.init_temp.value():.2f} °C\n"
            summary += f"Initial P: {self.init_pres.value():.4g} bar\n"
            summary += f"Final Value: {final_value}"
            if process_type in ['Isothermal', 'Isenthalpic', 'Isentropic', 'Polytropic']:
                summary += " bar\n"
            else:
                summary += " °C\n"
            summary += f"Points: {num_points}\n\n"
            summary += f"First State:\n"
            for key in results:
                if isinstance(results[key], np.ndarray):
                    val = results[key][0]
                    summary += f"  {key}: {val:.6g}\n"
            summary += f"\nLast State:\n"
            for key in results:
                if isinstance(results[key], np.ndarray):
                    val = results[key][-1]
                    summary += f"  {key}: {val:.6g}\n"
            self.process_results.setPlainText(summary)

            # Display data table
            props = list(results.keys())
            nrow = len(results[props[0]])
            ncol = len(props)
            self.process_table.setRowCount(nrow)
            self.process_table.setColumnCount(ncol)
            self.process_table.setHorizontalHeaderLabels(props)
            for i in range(nrow):
                for j, key in enumerate(props):
                    val = results[key][i]
                    if isinstance(val, float) and (np.isnan(val) or abs(val) > 1e8 or abs(val) < 1e-8):
                        val_str = f"{val:.4e}"
                    elif isinstance(val, float):
                        val_str = f"{val:.6g}"
                    else:
                        val_str = str(val)
                    self.process_table.setItem(i, j, QTableWidgetItem(val_str))
            self.process_table.resizeColumnsToContents()

            # Display process plot
            self.process_plot_canvas.plot_process_path(results, process_type, fluid)

        except Exception as e:
            QMessageBox.critical(self, "Simulation Error", f"Failed to simulate process: {str(e)}")
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, 
                             QGroupBox, QComboBox, QLabel, QPushButton, 
                             QCheckBox, QSplitter)
from PyQt5.QtCore import Qt
from core.plot_canvas import PlotCanvas

class PlottingTab(QWidget):
    def __init__(self, calc, parent=None):
        super().__init__(parent)
        self.calc = calc
        self.init_ui()

    def init_ui(self):
        """Create enhanced plotting tab"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Left panel - Plot controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Plot configuration
        plot_config_group = QGroupBox("Plot Configuration")
        plot_config_layout = QGridLayout(plot_config_group)
        
        # Fluid selection
        plot_config_layout.addWidget(QLabel("Fluid:"), 0, 0)
        self.plot_fluid_combo = QComboBox()
        self.plot_fluid_combo.addItems(self.calc.fluids)
        self.plot_fluid_combo.setCurrentText('Water')
        plot_config_layout.addWidget(self.plot_fluid_combo, 0, 1)
        
        # Plot type
        plot_config_layout.addWidget(QLabel("Plot Type:"), 1, 0)
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems([
            'T-S Diagram', 'P-H Diagram', 'P-V Diagram', 'H-S Diagram',
            'Property vs Temperature', 'Property vs Pressure', 
            'Saturation Curve', 'Phase Envelope', 'Custom Plot'
        ])
        plot_config_layout.addWidget(self.plot_type_combo, 1, 1)
        
        # Plot options
        self.show_grid = QCheckBox("Show Grid")
        self.show_grid.setChecked(True)
        plot_config_layout.addWidget(self.show_grid, 2, 0)
        
        self.show_legend = QCheckBox("Show Legend")
        self.show_legend.setChecked(True)
        plot_config_layout.addWidget(self.show_legend, 2, 1)
        
        left_layout.addWidget(plot_config_group)
        
        # Plot customization
        custom_group = QGroupBox("Customization")
        custom_layout = QGridLayout(custom_group)
        
        custom_layout.addWidget(QLabel("X-axis:"), 0, 0)
        self.x_axis_combo = QComboBox()
        self.x_axis_combo.addItems(['Auto', 'T', 'P', 'H', 'S', 'D', 'V'])
        custom_layout.addWidget(self.x_axis_combo, 0, 1)
        
        custom_layout.addWidget(QLabel("Y-axis:"), 1, 0)
        self.y_axis_combo = QComboBox()
        self.y_axis_combo.addItems(['Auto', 'T', 'P', 'H', 'S', 'D', 'V'])
        custom_layout.addWidget(self.y_axis_combo, 1, 1)
        
        left_layout.addWidget(custom_group)
        
        # Generate plot button
        plot_btn = QPushButton("Generate Plot")
        plot_btn.setStyleSheet("QPushButton { font-size: 16px; padding: 12px; }")
        plot_btn.clicked.connect(self.generate_plot)
        left_layout.addWidget(plot_btn)
        
        # Export plot options
        export_group = QGroupBox("Export Options")
        export_layout = QVBoxLayout(export_group)
        
        save_plot_btn = QPushButton("Save Plot")
        save_plot_btn.clicked.connect(self.save_plot)
        export_layout.addWidget(save_plot_btn)
        
        copy_plot_btn = QPushButton("Copy to Clipboard")
        copy_plot_btn.clicked.connect(self.copy_plot)
        export_layout.addWidget(copy_plot_btn)
        
        left_layout.addWidget(export_group)
        left_layout.addStretch()
        
        # Right panel - Plot display
        self.plot_canvas = PlotCanvas(self, width=12, height=8)
        
        # Add panels to splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.plot_canvas)
        splitter.setSizes([300, 900])
        
        layout.addWidget(splitter)
        
        self.setLayout(layout)

    def generate_plot(self):
        """Generate plot based on configuration"""
        fluid = self.plot_fluid_combo.currentText()
        plot_type = self.plot_type_combo.currentText()
        show_grid = self.show_grid.isChecked()
        show_legend = self.show_legend.isChecked()
        x_axis = self.x_axis_combo.currentText()
        y_axis = self.y_axis_combo.currentText()

        self.plot_canvas.plot_diagram(
            fluid,
            plot_type,
            show_grid=show_grid,
            show_legend=show_legend,
            x_axis=x_axis,
            y_axis=y_axis
        )

    def save_plot(self):
        """Save plot to file"""
        # This is a placeholder implementation
        pass

    def copy_plot(self):
        """Copy plot to clipboard"""
        # This is a placeholder implementation
        pass
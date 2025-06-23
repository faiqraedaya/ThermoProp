"""
Main window implementation for ThermoProp application
"""

import sys
import json
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QAction, QMessageBox,
    QProgressBar, QApplication, QFileDialog
)
from PyQt5.QtCore import QSettings

from core.mixture_calculator import MixtureCalculator
from core.plot_canvas import PlotCanvas
from dialogs.mixture_dialog import MixtureDialog
from dialogs.unit_converter_dialog import UnitConverterDialog
from dialogs.quick_calc_dialog import QuickCalcDialog
from utils.file_io import FileIO
from tabs.tab_manager import TabManager

class MainWindow(QMainWindow):
    """Enhanced main application window with mixture support"""
    
    def __init__(self):
        super().__init__()
        self.calc = MixtureCalculator()
        self.settings = QSettings('ThermoProp', 'Calculator')
        self.current_mixture = []
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """Initialize enhanced user interface"""
        self.setWindowTitle('ThermoProp')
        self.setGeometry(100, 100, 1400, 1000)
        
        # Set application style
        self.setStyleSheet(self._get_style_sheet())
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget_layout = QVBoxLayout(central_widget)
        
        # Initialize tab manager
        self.tab_manager = TabManager(self, self.calc)
        central_widget_layout.addWidget(self.tab_manager.get_tab_widget())
        
        # Enhanced status bar
        self.statusBar().showMessage('Ready')
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.statusBar().addPermanentWidget(self.progress_bar)
    
    def _get_style_sheet(self):
        """Return the application style sheet"""
        return """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #4CAF50;
            }
        """
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New Calculation', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_calculation)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open Project', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save Project', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction('Export Results', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_all_results)
        file_menu.addAction(export_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('Tools')

        calc_action = QAction('Quick Calculation', self)
        calc_action.triggered.connect(self.quick_calculation)
        tools_menu.addAction(calc_action)
        
        unit_conv_action = QAction('Unit Converter', self)
        unit_conv_action.triggered.connect(self.open_unit_converter)
        tools_menu.addAction(unit_conv_action)
        
        mixture_action = QAction('Mixture Designer', self)
        mixture_action.triggered.connect(self.open_mixture_designer)
        tools_menu.addAction(mixture_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def new_calculation(self):
        """Start a new calculation"""
        self.tab_manager.clear_all_tabs()
        self.current_mixture = []
        self.statusBar().showMessage('New calculation started')
    
    def open_project(self):
        """Open a saved project"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Open Project", "", "JSON Files (*.json)"
            )
            if filename:
                with open(filename, 'r') as f:
                    data = json.load(f)
                self.load_project_data(data)
                self.statusBar().showMessage(f'Project loaded: {filename}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open project: {str(e)}")
    
    def save_project(self):
        """Save current project"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Project", "", "JSON Files (*.json)"
            )
            if filename:
                data = self.get_project_data()
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
                self.statusBar().showMessage(f'Project saved: {filename}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")
    
    def export_all_results(self):
        """Export all calculation results"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export Results", "", "Excel Files (*.xlsx)"
            )
            if filename:
                FileIO.export_results(filename, self.get_all_results())
                self.statusBar().showMessage(f'Results exported: {filename}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export results: {str(e)}")
    
    def quick_calculation(self):
        """Open quick calculation dialog"""
        dialog = QuickCalcDialog(self)
        dialog.exec_()
    
    def open_unit_converter(self):
        """Open unit converter dialog"""
        dialog = UnitConverterDialog(self)
        dialog.exec_()
    
    def open_mixture_designer(self):
        """Open mixture designer dialog"""
        dialog = MixtureDialog(self)
        if dialog.exec_():
            self.current_mixture = dialog.get_mixture()
            self.update_mixture_display()
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About ThermoProp",
            "ThermoProp v2.1.0\n\n"
            "Enhanced Thermophysical Properties Calculator\n"
            "For Risk and Safety Engineering Applications\n"
            "with Mixture Support\n\n"
            "Author: Faiq Raedaya\n"
            "© 2025 MES")
    
    def save_settings(self):
        """Save application settings"""
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())
    
    def load_settings(self):
        """Load application settings"""
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        state = self.settings.value('windowState')
        if state:
            self.restoreState(state)
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.save_settings()
        event.accept()
    
    def load_project_data(self, data):
        """Load project data into the application"""
        try:
            # Load mixture data if present
            if 'mixture' in data:
                self.current_mixture = data['mixture']
                self.update_mixture_display()
            
            # Load tab data if present
            if 'tabs' in data and hasattr(self.tab_manager, 'load_tab_data'):
                self.tab_manager.load_tab_data(data['tabs'])
                
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Some project data could not be loaded: {str(e)}")
    
    def get_project_data(self):
        """Get current project data for saving"""
        data = {}
        
        # Save mixture data if present
        if self.current_mixture:
            data['mixture'] = self.current_mixture
        
        # Save tab data if available
        if hasattr(self.tab_manager, 'get_tab_data'):
            data['tabs'] = self.tab_manager.get_tab_data()
        
        return data
    
    def get_all_results(self):
        """Get all calculation results from all tabs"""
        results = {}
        
        # Get results from each tab
        for tab_name, tab in self.tab_manager.tabs.items():
            if hasattr(tab, 'get_results'):
                try:
                    tab_results = tab.get_results()
                    if tab_results:
                        results[tab_name] = tab_results
                except:
                    pass
        
        return results
    
    def update_mixture_display(self):
        """Update mixture display in relevant tabs"""
        # Update mixture tab if it has a display method
        mixture_tab = self.tab_manager.get_tab('mixture')
        if mixture_tab and hasattr(mixture_tab, 'update_mixture_display'):
            mixture_tab.update_mixture_display(self.current_mixture)
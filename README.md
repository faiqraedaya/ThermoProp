# ThermoProp
*Thermophysical Properties Calculator*

## Overview
ThermoProp is an enhanced thermophysical properties calculator designed for risk and safety engineering applications, with robust support for pure fluids and mixtures. It provides a modern, user-friendly graphical interface for calculating, simulating, and visualizing a wide range of thermodynamic and transport properties.

## Features
- **Single Point Calculations:** Compute properties for pure fluids at specified conditions.
- **Mixture Designer:** Define custom or use predefined mixtures (e.g., air, natural gas, flue gas) and calculate their properties.
- **Saturation Properties:** Calculate and display saturation curves and properties.
- **Process Path Simulation:** Simulate thermodynamic processes (isobaric, isochoric, isothermal, isenthalpic, isentropic, polytropic, custom) and visualize results.
- **Plotting Tools:** Generate T-S, P-H, P-V, H-S diagrams, property vs. temperature/pressure plots, and more.
- **Quick Calculation:** Instantly look up key properties for common fluids at standard or custom conditions.
- **Unit Converter:** Convert between a wide range of engineering units.
- **Export Results:** Save results to Excel or CSV for further analysis.

## Requirements
- Python 3.7+
- [CoolProp](http://www.coolprop.org/)
- PyQt5
- matplotlib
- pandas
- numpy
- scipy
- pint (for unit conversion)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd "ThermoProp"
   ```
2. **Install dependencies:**
   You can use pip to install the required packages:
   ```bash
   pip install CoolProp PyQt5 matplotlib pandas numpy scipy pint
   ```

## Usage
To launch the application, run:
```bash
python main.py
```

- The main window provides access to all features via tabs and menus.
- Use the **Mixture Designer** to define or load mixtures.
- Use the **Process Path** tab to simulate thermodynamic processes.
- Use the **Plotting** tab for advanced visualization.
- Export results using the menu or export buttons in each tab.

## Project Structure
- `main.py` — Application entry point
- `main_window.py` — Main GUI window
- `core/` — Core calculation logic (mixtures, components, plotting)
- `tabs/` — GUI tabs for different calculation and visualization tasks
- `dialogs/` — Dialogs for quick calculations, unit conversion, about, etc.
- `utils/` — Utility functions (file I/O, table utilities)
- `test_app.py` — Test script for verifying installation and UI

## License
This project is provided under the MIT License.

## Acknowledgments
- [CoolProp](http://www.coolprop.org/) for thermophysical property calculations.
- PyQt5 for the GUI framework.
- matplotlib for plotting and visualization.

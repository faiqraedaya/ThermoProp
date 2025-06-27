# ThermoProp
*Thermophysical Properties Calculator*

## Overview
ThermoProp is a versatile thermophysical properties calculator using CoolProp, with robust support for pure fluids and user-defined mixtures. It provides a modern, user-friendly GUI for calculating, simulating, and visualizing a wide range of thermodynamic and transport properties.

*Basically a CoolProp GUI Wrapper...*

## Features
- **Single Point Calculations:** Compute properties for pure fluids at specified conditions.
- **Mixture Designer:** Define custom or use predefined mixtures (e.g., air, natural gas, flue gas) and calculate their properties.
- **Saturation Properties:** Calculate and display saturation curves and properties.
- **Process Path Simulation:** Simulate thermodynamic processes (isobaric, isochoric, isothermal, isenthalpic, isentropic, polytropic, custom) and visualize results.
- **Plotting Tools:** Generate T-S, P-H, P-V, H-S diagrams, property vs. temperature/pressure plots, and more.
- **Quick Calculation:** Instantly look up key properties for common fluids at standard or custom conditions.
- **Unit Converter:** Convert between a wide range of engineering units.

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
   git clone https://github.com/faiqraedaya/thermoprop
   cd "ThermoProp"
   ```
2. **Install dependencies:**
   ```bash
   pip install CoolProp PyQt5 matplotlib pandas numpy scipy pint
   ```

## Usage
1. To launch the application, run:
   ```bash
   python main.py
   ```

## License
This project is provided under the MIT License.

## Acknowledgments
- [CoolProp](http://www.coolprop.org/) for an incredible thermophysical property calculation package.

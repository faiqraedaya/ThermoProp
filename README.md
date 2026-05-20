# ThermoProp

Thermophysical properties calculator for pure fluids and mixtures, built for risk and safety engineering workflows.

## Features

- Calculate 15+ thermodynamic and transport properties for pure fluids at any state point
- Mixture properties using ideal-gas or humid-air mixing rules with user-defined compositions
- Saturation properties (liquid/vapor) at a specified temperature or pressure
- Process path simulation: isobaric, isochoric, isothermal, isenthalpic, isentropic, and polytropic
- Interactive thermodynamic diagrams: T-S, P-H, P-V, H-S, saturation curves, phase envelopes
- Unit conversion across 10 property categories (temperature, pressure, density, energy, and more)
- Export results to CSV, Excel, or clipboard from any calculation tab

## Requirements

- Python ≥ 3.14
- [CoolProp](http://www.coolprop.org/) ≥ 7.2.0
- PySide6 ≥ 6.11.1
- matplotlib ≥ 3.10.9
- numpy ≥ 2.4.6
- pandas ≥ 3.0.3
- pint ≥ 0.25.3

## Installation

Clone the repository and install with [uv](https://github.com/astral-sh/uv) (recommended — `uv.lock` is provided):

```bash
git clone https://github.com/faiqraedaya/ThermoProp
cd ThermoProp
uv sync
```

Or with pip into an existing environment:

```bash
git clone https://github.com/faiqraedaya/ThermoProp
cd ThermoProp
pip install -e .
```

## Quick Start

```bash
uv run python main.py
# or, with pip install:
python main.py
```

The application opens with five tabs: **Single Point**, **Mixture**, **Saturation**, **Process Path**, and **Plotting**.

## Usage

### Single Point tab

Select a fluid, choose any two known properties (T, P, H, S, D, or U) and their values, then click **Calculate Properties**. Results include density, enthalpy, entropy, heat capacities, viscosity, thermal conductivity, speed of sound, and phase.

### Mixture tab

Open the **Mixture Designer** (Tools menu) to define a mixture by fluid name and mole fraction, or load a predefined mixture (Air, Natural Gas, Flue Gas). Set temperature and pressure, choose a mixing model (Ideal Gas or Humid Air), and click **Calculate Mixture Properties**.

### Saturation tab

Select a fluid and specify either a saturation temperature or saturation pressure. Results include saturation temperature, pressure, liquid/vapor density, enthalpy, entropy, and latent heat. A saturation curve plot is generated automatically.

### Process Path tab

Define the fluid, initial state (T and P), process type, and final condition, then click **Simulate Process**. Results are shown in a summary, a data table, and a four-panel plot of T-P, enthalpy, density, and entropy along the path.

### Plotting tab

Select a fluid and diagram type (T-S, P-H, P-V, H-S, Property vs Temperature, Property vs Pressure, Saturation Curve, Phase Envelope, or Custom). Generated plots can be saved to PNG/PDF/SVG or copied to the clipboard.

### Unit Converter

Available under **Tools → Unit Converter**. Converts between units for temperature, pressure, density, energy, power, length, area, volume, mass, and force using [pint](https://pint.readthedocs.io/).

## Development

```bash
git clone https://github.com/faiqraedaya/ThermoProp
cd ThermoProp
uv sync
```

Run the import and component smoke tests:

```bash
uv run python test_app.py
```

`test_app.py` verifies that all dependencies import cleanly, the `MixtureCalculator` instantiates correctly, and all five GUI tabs construct without error.

## Project Structure

```
ThermoProp/
├── main.py                  # Application entry point
├── pyproject.toml           # Project metadata and pinned dependency versions
├── uv.lock                  # Locked dependency tree
├── test_app.py              # Import and component smoke tests
└── src/
    └── thermoprop/
        ├── main_window.py   # Main window, menu bar, project save/load
        ├── core/
        │   ├── mixture_calculator.py  # CoolProp wrapper, unit conversion, process simulation
        │   ├── mixture_component.py   # Per-component data class
        │   └── plot_canvas.py         # Matplotlib canvas and diagram renderers
        ├── tabs/
        │   ├── single_point_tab.py
        │   ├── mixture_tab.py
        │   ├── saturation_tab.py
        │   ├── process_path_tab.py
        │   ├── plotting_tab.py
        │   └── tab_manager.py
        ├── dialogs/
        │   ├── mixture_dialog.py
        │   ├── unit_converter_dialog.py
        │   └── about_dialog.py
        └── utils/
            ├── file_io.py
            └── table_utils.py
```

## License

MIT License — see [LICENSE](LICENSE). Copyright (c) 2026 Faiq Raedaya.

<!-- Unverified: GitHub repository URL (assumed from existing README; not confirmed from repo config) -->

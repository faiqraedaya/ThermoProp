# ThermoProp

## Overview
*ThermoProp is a desktop calculator for the thermophysical properties of pure fluids and mixtures. It brings state-point, saturation, process-path and diagram calculations from CoolProp together in one interface.*

## Features
- Single-point properties of any CoolProp fluid from a pair of T, P, H, D, S or U
- Mixture properties with ideal-gas (Gibbs-Dalton) or humid-air models, including predefined mixtures such as air
- Saturation properties at a given temperature or pressure
- Isobaric, isochoric, isothermal, isenthalpic, isentropic and polytropic process paths
- T-S, P-H, P-V and H-S diagrams, saturation curves, phase envelopes and custom plots
- Unit converter
- Export of results to CSV or Excel, and projects saved as JSON

## Install
```bash
git clone https://github.com/faiqraedaya/ThermoProp
cd ThermoProp
uv sync
```

## Usage
```bash
uv run thermoprop
```
On the Single point page, Water at 25 °C and 1.01325 bara is preselected. Click Calculate properties to see the results table, then use Export CSV or Export Excel to save it. `uv run python main.py` starts the same application from a source checkout.

## Technical details
Inputs are entered in the GUI: a fluid or mixture, and two state properties in a choice of units. Values are converted to SI before calling CoolProp PropsSI. Supported input pairs are those CoolProp can flash on a mass basis; T-H, T-U, H-U and S-U are rejected. Results include density, enthalpy, entropy, internal energy, heat capacities, speed of sound, viscosity, thermal conductivity, surface tension, compressibility factor, phase and quality.

Ideal-gas mixtures evaluate each component in the gas phase at its partial pressure, so enthalpy and entropy include the ideal entropy of mixing. The calculation stops if any component is below its dew point at its partial pressure. Mixture viscosity uses Wilke's rule, and thermal conductivity uses the Wassiljewa equation with the Mason-Saxena approximation. Humid-air mixtures use CoolProp HAPropsSI on a per-kilogram-of-humid-air basis. Process paths use real-fluid properties, with two-phase segments inserted on isobaric and isothermal paths. Polytropic paths enforce p·v^n = constant with real-fluid density.

Results appear in tables and Matplotlib plots. They can be exported to .xlsx, .csv or .json, and a project is saved to and loaded from JSON.

## License
MIT — see [LICENSE](LICENSE).

# Architecture

## Overview

Project Aphelion separates concerns along responsibility boundaries. Each directory has a single clear purpose.

## Package Structure

### `aphelion/`: the Python package

The simulation engine.

```
aphelion/
├── __init__.py          # Package version
├── __main__.py          # CLI: loads scenarios, runs simulations, prints results
├── core/
│   ├── __init__.py
│   └── constants.py     # Physical constants (SI units, documented references)
└── dynamics/
    ├── __init__.py
    ├── integrators.py   # Generic numerical ODE solvers (RK4)
    └── suborbital.py    # 3DOF suborbital propagator
```

**Dependency direction:** `__main__` → `dynamics` → `core`. No circular dependencies.

### `scenarios/`: simulation configurations

YAML files defining vehicle parameters, initial conditions, and simulation settings. Loaded by the CLI. Reproducible.

### `tests/`: the test suite

```
tests/
├── unit/                # Component-level tests (mass model, atmosphere, etc.)
└── validation/          # Physics validation against analytical solutions
```

### `firmware/`: ESP32 embedded code

```
firmware/
├── flight-computer/
│   └── mpu6050-driver/  # Working MPU6050 I2C driver prototype
└── archive/             # Historical learning exercises (blink, PWM, DHT11, radar)
```

The firmware directory is separate from the Python package. They communicate through a future telemetry protocol (Level 5+).

### `docs/`: documentation

- `architecture.md`: this file
- `hardware.md`: hardware inventory and capability matrix
- `adr/`: architecture decision records
- `dev-logs/`: engineering development journal

### `media/`: generated assets

Plots and demo images. The `plots/` subdirectory contains reference outputs from the baseline scenario.

## Design Principles

1. **No module-level side effects.** Importing a module never runs simulation code.
2. **Constants in one place.** `aphelion/core/constants.py` is the single source for physical constants.
3. **Scenarios are data.** Simulation parameters live in YAML, not in Python code.
4. **Tests prove correctness.** Every physics module must have validation tests against analytical solutions.
5. **Firmware is separate.** The ESP32 code has its own build system (ESP-IDF/CMake). It is not part of the Python package.

## Data Flow

```
Scenario YAML
    ↓
CLI (loads config)
    ↓
Propagator (physics engine)
    ↓
States + Times (numpy arrays)
    ↓
Statistics / Plots / CSV
```

In future levels:

```
Simulation → Telemetry Protocol → MQTT → Ground Station → Visualization
     ↓
Simulated Sensors → ESP32 Flight Computer → State Estimation
```

## Physical Constants

All constants are in `aphelion/core/constants.py`. Values use CODATA 2018 and IERS Conventions 2010. Units are SI unless noted.

## Numerical Methods

- **Integrator:** Fixed-step RK4 in `aphelion/dynamics/integrators.py`
- **Convergence:** 4th-order (error ∝ dt⁴)
- **Current step size:** dt = 0.01s (configurable via scenario)

# Project Aphelion

A flight dynamics testbed for trajectory simulation, numerical methods, and embedded flight hardware.

Project Aphelion is an evolving engineering project. It currently combines a Python suborbital trajectory simulator with an ESP32 flight computer prototype. The long-term plan runs from suborbital propagation through orbital mechanics, telemetry, and hardware-in-the-loop testing, but the near-term work is about getting the numerical core solid and validated.

## Current Status

**Level 0: Foundations** (September 2026)

What exists now:

- A 3DOF suborbital trajectory propagator using RK4 integration
- Atmospheric drag and propellant mass depletion modelling
- YAML scenario configuration
- A Python package (`aphelion`) with a CLI
- A unit and validation test suite
- CI on GitHub Actions (Python 3.10 through 3.13)
- An ESP32 MPU6050 IMU driver, working on physical hardware

The propagator has validation tests against analytical solutions, but treat those as a work in progress. Full propagator validation is the Level 1 milestone.

### Baseline Scenario Statistics

| Metric | Value |
|---|---|
| Apogee altitude | ~655 m |
| Flight time | ~25 s |
| Downrange distance | ~476 m |

These come from `scenarios/suborbital-baseline.yaml`, which describes a small suborbital flight.

## Quick Start

```bash
pip install -e ".[dev]"

# Run the baseline simulation
aphelion --scenario scenarios/suborbital-baseline.yaml

# Or equivalently
python -m aphelion --scenario scenarios/suborbital-baseline.yaml

# Run tests
pytest

# Run linting
ruff check .
```

## Architecture

```
aphelion/                  # Python package
├── core/                  # Physical constants (constants.py)
├── dynamics/              # Numerical + propagator code
│   ├── integrators.py     # RK4 integrator
│   └── suborbital.py      # 3DOF suborbital propagator
└── __main__.py            # CLI entry point

scenarios/                 # YAML simulation configs
tests/                     # Unit + validation tests
firmware/                  # ESP32 embedded code
  ├── flight-computer/
  │   └── mpu6050-driver/  # Working MPU6050 I2C driver
  └── archive/             # Historical learning exercises
docs/                      # Docs, ADRs, dev logs
media/                     # Plots and demo assets
```

See [docs/architecture.md](docs/architecture.md) for details.

## Propagator

The propagator is a 3DOF trajectory model for suborbital launch vehicles:

- **Integration:** fixed-step 4th-order Runge-Kutta
- **Gravity:** constant g0, flat-Earth approximation
- **Atmosphere:** exponential density model
- **Drag:** quadratic aerodynamic drag with configurable Cd and area
- **Thrust:** constant thrust during the powered phase, aligned with velocity
- **Mass:** linear propellant depletion during the burn

### Limitations

These are intentional for the current level:

- Flat-Earth geometry (valid below ~100 km altitude)
- Constant gravitational field (no 1/r² variation)
- No wind model
- Thrust aligned with the velocity vector, not the body frame
- 3DOF, no rotational dynamics
- No orbital mechanics yet

## Hardware Prototype

An ESP32-WROOM board with an MPU6050 IMU:

- I2C at 100 kHz (SDA: GPIO 21, SCL: GPIO 22)
- Reads 6-axis accelerometer + gyroscope + temperature
- Verified on physical hardware

This is a learning prototype, not flight software. It is the first piece of the flight computer, far from the eventual telemetry and ground-station system. See `firmware/flight-computer/mpu6050-driver/` and [docs/hardware.md](docs/hardware.md).

## Validation

The physics tests check the propagator against analytical results:

- Vertical free-fall: velocity and altitude match v(t) = v₀ - gt and h(t) = v₀t - ½gt²
- RK4 convergence: error drops at the expected 4th-order rate
- Energy conservation: specific mechanical energy is conserved in ballistic flight

All tests pass with relative tolerance ≤ 0.1%.

## Roadmap

| Level | Description | Status |
|---|---|---|
| 0 | Foundations: package, tests, CI | **Current** |
| 1 | Validated suborbital propagator | Planned |
| 2 | Two-body orbital propagator | Planned |
| 3 | Perturbation models (J2, drag, SRP) | Planned |
| 4 | Maneuver and mission modelling | Planned |
| 5 | Telemetry protocol and ground station | Planned |
| 6 | Mission control visualization | Planned |
| 7 | Attitude dynamics | Planned |
| 8 | Extended Kalman filter | Planned |
| 9 | Monte Carlo dispersion analysis | Planned |
| 10 | Hardware-in-the-loop | Planned |

## Tech Stack

- **Simulation:** Python 3.10+, NumPy, SciPy, Matplotlib, PyYAML
- **Testing:** pytest, ruff
- **Firmware:** C++, ESP-IDF v5.2, FreeRTOS
- **Hardware:** ESP32-WROOM-32D, MPU6050 IMU

## License

MIT

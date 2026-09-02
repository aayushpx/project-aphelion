# Project Aphelion

A flight-dynamics and spacecraft mission simulation/testbed platform.

Project Aphelion is a suborbital-to-orbital flight dynamics testbed combining a Python numerical simulation engine with ESP32 embedded hardware. It is designed to demonstrate software engineering, aerospace engineering, numerical methods, and hardware integration as a continuously evolving engineering project.

## Current Status

**Level 0 — Foundations** (September 2026)

The project currently provides:

- A validated 3DOF suborbital trajectory propagator (RK4 integration)
- Atmospheric drag and mass depletion modelling
- YAML-based scenario configuration
- A clean Python package (`aphelion`) with CLI
- 31 unit and validation tests
- An ESP32 MPU6050 IMU driver (working hardware prototype)

### Trajectory Statistics (Baseline Scenario)

| Metric | Value |
|---|---|
| Apogee altitude | ~655 m |
| Flight time | ~25 s |
| Downrange distance | ~476 m |

## Quick Start

```bash
# Install the package
pip install -e ".[dev]"

# Run the baseline simulation
aphelion run --scenario scenarios/suborbital-baseline.yaml

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
├── core/                  # Physical constants, types
│   └── constants.py       # G, mu, R_Earth, etc.
├── dynamics/              # Physics engines
│   ├── integrators.py     # RK4 numerical integrator
│   └── suborbital.py      # 3DOF suborbital propagator
└── __main__.py            # CLI entry point

scenarios/                 # YAML simulation configs
tests/                     # Unit + validation tests
firmware/                  # ESP32 embedded code
  ├── flight-computer/
  │   └── mpu6050-driver/  # Working MPU6050 I2C driver
  └── archive/             # Historical learning exercises
docs/                      # Documentation
  ├── adr/                 # Architecture Decision Records
  └── dev-logs/            # Engineering development journal
media/                     # Plots and demo assets
```

See [docs/architecture.md](docs/architecture.md) for details.

## Propagator

The core propagator is a 3DOF (three-degrees-of-freedom) trajectory model for suborbital launch vehicles:

- **Integration:** 4th-order Runge-Kutta (RK4), fixed step
- **Gravity:** Constant g0 (flat-Earth approximation)
- **Atmosphere:** Exponential density model (scale height)
- **Drag:** Quadratic aerodynamic drag with configurable Cd and area
- **Thrust:** Constant thrust during powered phase, aligned along velocity
- **Mass:** Linear propellant depletion during burn

### Limitations

These are known and intentional for the current development level:

- Flat-Earth geometry (valid for < 100 km altitude)
- Constant gravitational field (no 1/r² variation)
- No wind model
- Thrust aligned along velocity vector (not body frame)
- No rotational dynamics (3DOF, not 6DOF)
- No orbital mechanics yet

## Hardware Prototype

An ESP32-WROOM development board with MPU6050 IMU:

- I2C bus at 100 kHz (SDA: GPIO 21, SCL: GPIO 22)
- Reads 6-axis accelerometer + gyroscope + temperature
- Verified on physical hardware (soldered connections)

This is a **learning prototype**, not flight software. See `firmware/flight-computer/mpu6050-driver/`.

See [docs/hardware.md](docs/hardware.md) for hardware interfaces and integration targets.

## Validation

Physics validation tests verify numerical accuracy against analytical solutions:

- Vertical free-fall: velocity and altitude match v(t) = v₀ - gt and h(t) = v₀t - ½gt²
- RK4 convergence: error reduces at 4th-order rate
- Energy conservation: specific mechanical energy conserved in ballistic flight

All tests pass with relative tolerance ≤ 0.1%.

## Roadmap

| Level | Description | Status |
|---|---|---|
| 0 | Project foundations, package, tests, CI | **Current** |
| 1 | Validated suborbital propagator | Planned |
| 2 | Two-body orbital propagator | Planned |
| 3 | Perturbation models (J2, drag, SRP) | Planned |
| 4 | Maneuver & mission modeling | Planned |
| 5 | Telemetry protocol & ground station | Planned |
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

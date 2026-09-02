# ADR 001: Python for Numerical Core

## Context

Project Aphelion needs a language for the simulation engine (orbital mechanics, numerical integration, state estimation, Monte Carlo). Options considered: Python, Rust, C++, MATLAB.

## Decision

Use **Python** with NumPy/SciPy for the numerical core.

## Consequences

**Positive:**
- Mature scientific computing ecosystem (NumPy, SciPy, Matplotlib)
- Rapid prototyping and iteration
- Easy validation with analytical solutions
- Low barrier to entry for a solo developer
- pytest for testing

**Negative:**
- Slower than Rust/C++ for compute-heavy paths
- Not suitable for embedded firmware

**Mitigation:**
- Future performance-critical kernels can be rewritten in Rust and called via Python bindings
- The firmware layer is C++ (ESP-IDF) — this decision only affects the simulation side
- For current scales (suborbital trajectories), Python performance is adequate

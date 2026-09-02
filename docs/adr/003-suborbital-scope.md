# ADR 003: Flat-Earth Scope for Suborbital Propagation

## Context

The initial propagator models suborbital flights (altitudes < 10 km, ranges < 1 km). Options: full spherical Earth with 1/r² gravity, flat-Earth with constant g0.

## Decision

Use **flat-Earth with constant g0** for the current suborbital scope.

## Consequences

**Positive:**
- Simple analytical validation (v = v₀ - gt, h = v₀t - ½gt²)
- Correct for the current altitude/range regime
- Clear documentation of limitations

**Negative:**
- Will need replacement for orbital mechanics (Level 2+)
- Not suitable for altitudes > 100 km

**Mitigation:**
- The `SuborbitalPropagator` class is explicitly scoped to suborbital flight
- A separate `OrbitalPropagator` will be created in Level 2 with full spherical geometry
- The flat-Earth propagator remains valid for sounding rocket simulations

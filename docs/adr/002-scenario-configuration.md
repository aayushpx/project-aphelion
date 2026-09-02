# ADR 002: YAML for Scenario Configuration

## Context

The propagator needs configurable parameters (vehicle mass, thrust, drag coefficient, launch angle, etc.). Options: hardcoded constants, Python dataclasses, YAML files, JSON files, TOML files.

## Decision

Use **YAML** for scenario configuration files.

## Consequences

**Positive:**
- Human-readable and editable
- Supports comments (useful for documenting parameter choices)
- Well-supported by PyYAML
- Version-controllable
- Separates data from code

**Negative:**
- Requires PyYAML dependency
- No schema validation built in (mitigated by loading code that validates)

**Mitigation:**
- The scenario loader in `__main__.py` validates required keys
- Future: add JSON Schema validation if scenarios become complex

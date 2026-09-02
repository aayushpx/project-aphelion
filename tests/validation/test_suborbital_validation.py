"""Validation tests for the suborbital propagator.

These tests verify that the numerical propagator produces physically
correct results by comparing against analytical solutions.

Tolerance rationale:
    - RK4 with dt=0.01s on a 5-second simulation gives ~500 steps.
    - Local truncation error is O(dt^5) ≈ 1e-10 per step.
    - Global error accumulates linearly: ~5e-8 over 500 steps.
    - For position (integrated from velocity), error is O(dt^4) ≈ 1e-8.
    - Using rtol=1e-3 (0.1%) provides generous margin while still
      catching gross errors. This is appropriate for engineering validation
      where the goal is to confirm the integrator and force models are
      implemented correctly, not to achieve production precision.
"""

import numpy as np
import pytest

from aphelion.core.constants import G0
from aphelion.dynamics.suborbital import SuborbitalPropagator


class TestFreeFallValidation:
    """Validate against analytical free-fall (no drag, no thrust).

    Analytical solution for vertical motion under constant gravity:
        v(t) = v0 - g*t
        h(t) = h0 + v0*t - 0.5*g*t^2
    """

    def test_vertical_velocity_matches_analytical(self):
        """Velocity should match v(t) = v0 - g*t."""
        prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.0, area=0.008,
            cd=0.0, thrust_nominal=0.0, burn_time=0.0,
        )

        v0 = 50.0  # m/s upward
        states, times = prop.propagate(
            [0, 0, 0, 0, 0, v0], dt=0.001, max_duration=5.0,
        )

        # Check velocity at multiple times during ascent
        for t_check in [0.5, 1.0, 2.0, 3.0]:
            idx = np.argmin(np.abs(times - t_check))
            t_actual = times[idx]
            v_analytical = v0 - G0 * t_actual
            v_numerical = states[idx, 5]
            assert v_numerical == pytest.approx(v_analytical, rel=1e-3), (
                f"Velocity mismatch at t={t_actual:.3f}: "
                f"numerical={v_numerical:.6f}, analytical={v_analytical:.6f}"
            )

    def test_altitude_matches_analytical(self):
        """Altitude should match h(t) = h0 + v0*t - 0.5*g*t^2."""
        prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.0, area=0.008,
            cd=0.0, thrust_nominal=0.0, burn_time=0.0,
        )

        v0 = 50.0
        states, times = prop.propagate(
            [0, 0, 0, 0, 0, v0], dt=0.001, max_duration=5.0,
        )

        for t_check in [0.5, 1.0, 2.0, 3.0]:
            idx = np.argmin(np.abs(times - t_check))
            t_actual = times[idx]
            h_analytical = v0 * t_actual - 0.5 * G0 * t_actual**2
            h_numerical = states[idx, 2]
            assert h_numerical == pytest.approx(h_analytical, rel=1e-3), (
                f"Altitude mismatch at t={t_actual:.3f}: "
                f"numerical={h_numerical:.6f}, analytical={h_analytical:.6f}"
            )

    def test_apogee_time_matches_analytical(self):
        """Apogee should occur at t = v0/g."""
        prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.0, area=0.008,
            cd=0.0, thrust_nominal=0.0, burn_time=0.0,
        )

        v0 = 100.0
        states, times = prop.propagate(
            [0, 0, 0, 0, 0, v0], dt=0.001, max_duration=15.0,
        )

        t_apogee_analytical = v0 / G0
        t_apogee_numerical = times[np.argmax(states[:, 2])]
        assert t_apogee_numerical == pytest.approx(
            t_apogee_analytical, rel=1e-3
        ), (
            f"Apogee time mismatch: numerical={t_apogee_numerical:.4f}, "
            f"analytical={t_apogee_analytical:.4f}"
        )

    def test_apogee_altitude_matches_analytical(self):
        """Maximum altitude should be v0^2 / (2*g)."""
        prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.0, area=0.008,
            cd=0.0, thrust_nominal=0.0, burn_time=0.0,
        )

        v0 = 100.0
        states, times = prop.propagate(
            [0, 0, 0, 0, 0, v0], dt=0.001, max_duration=15.0,
        )

        h_max_analytical = v0**2 / (2 * G0)
        h_max_numerical = np.max(states[:, 2])
        assert h_max_numerical == pytest.approx(
            h_max_analytical, rel=1e-3
        ), (
            f"Apogee mismatch: numerical={h_max_numerical:.4f}, "
            f"analytical={h_max_analytical:.4f}"
        )

    def test_impact_time_matches_analytical(self):
        """Total flight time should be 2*v0/g."""
        prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.0, area=0.008,
            cd=0.0, thrust_nominal=0.0, burn_time=0.0,
        )

        v0 = 50.0
        states, times = prop.propagate(
            [0, 0, 0, 0, 0, v0], dt=0.001, max_duration=15.0,
        )

        t_flight_analytical = 2 * v0 / G0
        t_flight_numerical = times[-1]
        assert t_flight_numerical == pytest.approx(
            t_flight_analytical, rel=1e-3
        ), (
            f"Flight time mismatch: numerical={t_flight_numerical:.4f}, "
            f"analytical={t_flight_analytical:.4f}"
        )


class TestRK4Convergence:
    """Verify RK4 convergence rate using a nonlinear ODE.

    The ODE dx/dt = x has analytical solution x(t) = e^t.
    This is nonlinear and NOT exactly integrated by RK4, so truncation
    error is measurable. Halving dt should reduce error by ~16x (2^4).
    """

    def test_convergence_rate(self):
        from aphelion.dynamics.integrators import rk4

        def exponential_derivs(state, t):
            return state  # dx/dt = x

        x0 = np.array([1.0])
        t_check = 1.0
        x_analytical = np.exp(t_check)

        dt_fine = 0.05
        dt_coarse = 0.1

        states_fine, times_fine = rk4(
            exponential_derivs, x0, (0.0, t_check + 0.01), dt_fine,
        )
        states_coarse, times_coarse = rk4(
            exponential_derivs, x0, (0.0, t_check + 0.01), dt_coarse,
        )

        idx_fine = np.argmin(np.abs(times_fine - t_check))
        idx_coarse = np.argmin(np.abs(times_coarse - t_check))

        err_fine = abs(states_fine[idx_fine, 0] - x_analytical)
        err_coarse = abs(states_coarse[idx_coarse, 0] - x_analytical)

        # Error ratio should be approximately 16x (2^4) for RK4
        assert err_coarse > 1e-10, (
            f"Coarse error too small ({err_coarse:.2e}) to test convergence"
        )
        ratio = err_coarse / err_fine
        assert ratio > 8, (
            f"Expected error ratio > 8 (RK4 convergence), got {ratio:.2f}. "
            f"Coarse error: {err_coarse:.2e}, fine error: {err_fine:.2e}"
        )


class TestEnergyConservation:
    """Verify energy conservation in ballistic (no-drag, no-thrust) flight.

    In a constant gravitational field with no drag, specific mechanical
    energy (KE + PE per unit mass) should be conserved.
    """

    def test_specific_energy_conserved(self):
        prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.0, area=0.008,
            cd=0.0, thrust_nominal=0.0, burn_time=0.0,
        )

        v0 = 80.0
        states, times = prop.propagate(
            [0, 0, 0, 0, 0, v0], dt=0.001, max_duration=10.0,
        )

        # Specific energy = 0.5*v^2 + g*h (per unit mass)
        speeds = np.linalg.norm(states[:, 3:6], axis=1)
        heights = states[:, 2]
        energy = 0.5 * speeds**2 + G0 * heights

        # Energy should be conserved to within numerical tolerance
        # Use only the portion before ground impact
        valid = heights >= -0.01
        energy_valid = energy[valid]
        energy_variation = np.max(energy_valid) - np.min(energy_valid)
        energy_mean = np.mean(energy_valid)

        assert energy_variation / energy_mean < 1e-4, (
            f"Energy variation {energy_variation:.6e} exceeds tolerance "
            f"relative to mean {energy_mean:.6e}"
        )

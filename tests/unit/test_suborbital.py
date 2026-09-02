"""Unit tests for the suborbital propagator module."""

import numpy as np
import pytest

from aphelion.dynamics.suborbital import SuborbitalPropagator


class TestSuborbitalPropagatorInit:
    """Tests for constructor validation."""

    def test_valid_construction(self):
        p = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.3, area=0.008,
            cd=0.45, thrust_nominal=80.0, burn_time=3.5,
        )
        assert p.dry_mass == 1.0
        assert p.total_mass == 1.3

    def test_zero_propellant(self):
        p = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.0, area=0.008,
            cd=0.45, thrust_nominal=80.0, burn_time=0.0,
        )
        assert p.total_mass == 1.0

    def test_negative_dry_mass_raises(self):
        with pytest.raises(ValueError, match="dry_mass must be > 0"):
            SuborbitalPropagator(
                dry_mass=-1.0, propellant_mass=0.3, area=0.008,
                cd=0.45, thrust_nominal=80.0, burn_time=3.5,
            )

    def test_negative_propellant_raises(self):
        with pytest.raises(ValueError, match="propellant_mass must be >= 0"):
            SuborbitalPropagator(
                dry_mass=1.0, propellant_mass=-0.3, area=0.008,
                cd=0.45, thrust_nominal=80.0, burn_time=3.5,
            )

    def test_zero_area_raises(self):
        with pytest.raises(ValueError, match="area must be > 0"):
            SuborbitalPropagator(
                dry_mass=1.0, propellant_mass=0.3, area=0.0,
                cd=0.45, thrust_nominal=80.0, burn_time=3.5,
            )

    def test_negative_cd_raises(self):
        with pytest.raises(ValueError, match="cd must be >= 0"):
            SuborbitalPropagator(
                dry_mass=1.0, propellant_mass=0.3, area=0.008,
                cd=-0.45, thrust_nominal=80.0, burn_time=3.5,
            )


class TestMassModel:
    """Tests for mass depletion model."""

    def setup_method(self):
        self.prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.3, area=0.008,
            cd=0.45, thrust_nominal=80.0, burn_time=3.5,
        )

    def test_initial_mass(self):
        assert self.prop.get_mass(0.0) == pytest.approx(1.3)

    def test_midburn_mass(self):
        # At t = 1.75s (half of burn_time), mass should be halfway
        mass = self.prop.get_mass(1.75)
        expected = 1.3 - (0.3 / 3.5) * 1.75
        assert mass == pytest.approx(expected)

    def test_burnout_mass(self):
        # At t = burn_time, mass should be dry_mass
        assert self.prop.get_mass(3.5) == pytest.approx(1.0)

    def test_post_burn_mass(self):
        # After burnout, mass should be constant
        assert self.prop.get_mass(10.0) == pytest.approx(1.0)
        assert self.prop.get_mass(100.0) == pytest.approx(1.0)

    def test_mass_decreases_during_burn(self):
        masses = [self.prop.get_mass(t) for t in np.linspace(0, 3.5, 10)]
        for i in range(len(masses) - 1):
            assert masses[i + 1] < masses[i]

    def test_mdot_calculation(self):
        assert self.prop.mdot == pytest.approx(0.3 / 3.5)


class TestAtmosphereModel:
    """Tests for exponential atmospheric density model."""

    def setup_method(self):
        self.prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.3, area=0.008,
            cd=0.45, thrust_nominal=80.0, burn_time=3.5,
        )

    def test_sea_level_density(self):
        rho = self.prop.get_density(0.0)
        assert rho == pytest.approx(1.225)

    def test_density_decreases_with_altitude(self):
        rho_0 = self.prop.get_density(0.0)
        rho_10k = self.prop.get_density(10000.0)
        rho_100k = self.prop.get_density(100000.0)
        assert rho_0 > rho_10k > rho_100k

    def test_negative_altitude_clamps_to_sea_level(self):
        assert self.prop.get_density(-100.0) == pytest.approx(1.225)

    def test_exponential_decay_at_scale_height(self):
        # At altitude = scale height, density should be rho0 / e
        rho = self.prop.get_density(8500.0)
        expected = 1.225 / np.e
        assert rho == pytest.approx(expected, rel=1e-10)

    def test_density_always_positive(self):
        for alt in [0, 5000, 20000, 100000, 500000]:
            assert self.prop.get_density(alt) > 0


class TestPropagation:
    """Tests for the propagation method."""

    def setup_method(self):
        self.prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.3, area=0.008,
            cd=0.45, thrust_nominal=80.0, burn_time=3.5,
        )

    def test_vertical_launch_altitude_positive(self):
        states, times = self.prop.propagate(
            [0, 0, 0, 0, 0, 10.0],  # 10 m/s straight up
            dt=0.01,
            max_duration=5.0,
        )
        # Vehicle should reach positive altitude
        assert np.max(states[:, 2]) > 0

    def test_impact_at_zero_altitude(self):
        # Use a no-thrust, no-drag propagator for clean ballistic flight
        prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.0, area=0.008,
            cd=0.0, thrust_nominal=0.0, burn_time=0.0,
        )
        states, times = prop.propagate(
            [0, 0, 0, 0, 0, 10.0],
            dt=0.001,
            max_duration=5.0,
        )
        # Final altitude should be approximately 0 (interpolated impact)
        assert states[-1, 2] == pytest.approx(0.0, abs=0.01)

    def test_returns_arrays(self):
        states, times = self.prop.propagate(
            [0, 0, 0, 0, 0, 5.0], dt=0.1, max_duration=2.0,
        )
        assert isinstance(states, np.ndarray)
        assert isinstance(times, np.ndarray)
        assert states.shape[1] == 6
        assert len(times) == len(states)

    def test_time_monotonically_increasing(self):
        _, times = self.prop.propagate(
            [0, 0, 0, 0, 0, 5.0], dt=0.01, max_duration=2.0,
        )
        diffs = np.diff(times)
        assert np.all(diffs > 0)

    def test_trajectory_stats_exist(self):
        states, times = self.prop.propagate(
            [0, 0, 0, 0, 0, 10.0], dt=0.01, max_duration=5.0,
        )
        stats = self.prop.get_trajectory_stats(states, times)
        assert "apogee_altitude_m" in stats
        assert "flight_time_s" in stats
        assert stats["apogee_altitude_m"] > 0
        assert stats["flight_time_s"] > 0


class TestDerivatives:
    """Tests for the derivatives function."""

    def setup_method(self):
        self.prop = SuborbitalPropagator(
            dry_mass=1.0, propellant_mass=0.3, area=0.008,
            cd=0.45, thrust_nominal=80.0, burn_time=3.5,
        )

    def test_stationary_vehicle_has_gravitational_acceleration(self):
        state = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        derivs = self.prop._derivatives(state, 5.0)  # After burnout
        # Should have zero velocity derivative and -g0 acceleration
        assert derivs[3] == pytest.approx(0.0)  # ax
        assert derivs[4] == pytest.approx(0.0)  # ay
        assert derivs[5] == pytest.approx(-9.80665)  # az (gravity)

    def test_thrust_direction_during_burn(self):
        # Vehicle moving upward during burn
        state = np.array([0.0, 0.0, 100.0, 0.0, 0.0, 50.0])
        derivs = self.prop._derivatives(state, 1.0)  # During burn
        # Vertical acceleration should be positive (thrust > gravity)
        assert derivs[5] > 0

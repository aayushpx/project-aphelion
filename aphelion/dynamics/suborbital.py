"""3DOF suborbital trajectory propagator.

Implements a flat-Earth, constant-gravity 3DOF trajectory model for
suborbital launch vehicles. Uses 4th-order Runge-Kutta integration with
altitude-dependent atmospheric density and time-varying mass profiles.

Limitations (by design at this level):
    - Flat-Earth assumption (valid for < 100 km altitude, < 100 km range)
    - Constant gravitational field (g0)
    - Exponential atmosphere model
    - Thrust aligned along velocity vector (not body frame)
    - No wind model
    - No rotational dynamics (3DOF only)
"""

import numpy as np

from aphelion.core.constants import G0, H_SCALE, RHO_SEA_LEVEL


class SuborbitalPropagator:
    """3DOF trajectory propagator for suborbital launch vehicles.

    Parameters
    ----------
    dry_mass : float
        Structural mass of the vehicle (kg). Must be > 0.
    propellant_mass : float
        Usable propellant mass (kg). Must be >= 0.
    area : float
        Cross-sectional area for drag (m^2). Must be > 0.
    cd : float
        Drag coefficient (dimensionless). Must be >= 0.
    thrust_nominal : float
        Nominal thrust during powered phase (N). Must be >= 0.
    burn_time : float
        Duration of powered phase (s). Must be >= 0.
    rho0 : float, optional
        Sea-level atmospheric density (kg/m^3). Default: 1.225.
    h_scale : float, optional
        Atmospheric scale height (m). Default: 8500.0.
    g0 : float, optional
        Gravitational acceleration (m/s^2). Default: 9.80665.
    """

    def __init__(
        self,
        dry_mass: float,
        propellant_mass: float,
        area: float,
        cd: float,
        thrust_nominal: float,
        burn_time: float,
        rho0: float = RHO_SEA_LEVEL,
        h_scale: float = H_SCALE,
        g0: float = G0,
    ):
        if dry_mass <= 0:
            raise ValueError(f"dry_mass must be > 0, got {dry_mass}")
        if propellant_mass < 0:
            raise ValueError(f"propellant_mass must be >= 0, got {propellant_mass}")
        if area <= 0:
            raise ValueError(f"area must be > 0, got {area}")
        if cd < 0:
            raise ValueError(f"cd must be >= 0, got {cd}")
        if thrust_nominal < 0:
            raise ValueError(f"thrust_nominal must be >= 0, got {thrust_nominal}")
        if burn_time < 0:
            raise ValueError(f"burn_time must be >= 0, got {burn_time}")

        self.dry_mass = dry_mass
        self.propellant_mass = propellant_mass
        self.area = area
        self.cd = cd
        self.thrust_nominal = thrust_nominal
        self.burn_time = burn_time
        self.rho0 = rho0
        self.h_scale = h_scale
        self.g0 = g0

        self.total_mass = dry_mass + propellant_mass
        self.mdot = propellant_mass / burn_time if burn_time > 0 else 0.0

    def get_mass(self, t: float) -> float:
        """Instantaneous vehicle mass due to propellant depletion.

        During powered flight (t < burn_time), mass decreases linearly.
        After burnout, mass equals dry_mass.
        """
        if t < self.burn_time:
            return self.total_mass - self.mdot * t
        return self.dry_mass

    def get_density(self, altitude: float) -> float:
        """Exponential atmospheric density model.

        Parameters
        ----------
        altitude : float
            Altitude above sea level (m). Values below 0 are clamped to sea level.
        """
        if altitude < 0:
            return self.rho0
        return self.rho0 * np.exp(-altitude / self.h_scale)

    def _derivatives(self, state: np.ndarray, t: float) -> np.ndarray:
        """State derivative: [velocity, acceleration].

        State vector layout:
            state[0] = x (downrange, m)
            state[1] = y (cross-range, m); unused in 2D
            state[2] = z (altitude, m)
            state[3] = vx (downrange velocity, m/s)
            state[4] = vy (cross-range velocity, m/s)
            state[5] = vz (vertical velocity, m/s)

        Forces modelled:
            - Gravity: constant g0, downward
            - Aerodynamic drag: opposite to velocity
            - Thrust: along velocity vector during powered phase
        """
        x, y, z, vx, vy, vz = state
        vel = np.array([vx, vy, vz])
        speed = np.linalg.norm(vel)
        mass = self.get_mass(t)

        # Gravity
        f_gravity = np.array([0.0, 0.0, -mass * self.g0])

        # Aerodynamic drag
        if speed > 1e-6:
            rho = self.get_density(z)
            drag_mag = 0.5 * rho * speed**2 * self.cd * self.area
            f_drag = -drag_mag * (vel / speed)
        else:
            f_drag = np.zeros(3)

        # Thrust (along velocity vector during powered phase)
        if t < self.burn_time:
            if speed > 1e-6:
                f_thrust = self.thrust_nominal * (vel / speed)
            else:
                f_thrust = np.array([0.0, 0.0, self.thrust_nominal])
        else:
            f_thrust = np.zeros(3)

        # Equations of motion: a = F_total / m
        total_force = f_gravity + f_drag + f_thrust
        accel = total_force / mass

        return np.concatenate([vel, accel])

    def propagate(
        self,
        initial_state: list | np.ndarray,
        dt: float = 0.01,
        max_duration: float = 100.0,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Run trajectory propagation.

        Parameters
        ----------
        initial_state : array_like
            Initial state vector [x, y, z, vx, vy, vz] in meters and m/s.
        dt : float
            Integration time step (s). Default: 0.01.
        max_duration : float
            Maximum simulation duration (s). Default: 100.0.

        Returns
        -------
        states : ndarray, shape (N, 6)
            State history. Each row is [x, y, z, vx, vy, vz].
        times : ndarray, shape (N,)
            Corresponding time values (s).
        """
        initial_state = np.asarray(initial_state, dtype=float)

        # Integrate with RK4, checking for ground impact
        all_states = [initial_state.copy()]
        all_times = [0.0]

        t = 0.0
        state = initial_state.copy()

        while t < max_duration:
            # Single RK4 step
            k1 = self._derivatives(state, t)
            k2 = self._derivatives(state + 0.5 * dt * k1, t + 0.5 * dt)
            k3 = self._derivatives(state + 0.5 * dt * k2, t + 0.5 * dt)
            k4 = self._derivatives(state + dt * k3, t + dt)

            state = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            t += dt

            all_states.append(state.copy())
            all_times.append(t)

            # Ground impact termination
            if state[2] < -1e-3:
                break

        states = np.array(all_states)
        times = np.array(all_times)

        # Interpolate impact point if vehicle went below ground
        if states[-1, 2] < 0.0 and len(states) > 1:
            z_prev = states[-2, 2]
            z_curr = states[-1, 2]
            fraction = (0.0 - z_prev) / (z_curr - z_prev)

            t_impact = times[-2] + fraction * dt
            state_impact = states[-2] + fraction * (states[-1] - states[-2])
            state_impact[2] = 0.0  # Snap to ground

            states[-1] = state_impact
            times[-1] = t_impact

        return states, times

    def get_trajectory_stats(self, states: np.ndarray, times: np.ndarray) -> dict:
        """Compute basic trajectory statistics from a propagated result.

        Parameters
        ----------
        states : ndarray, shape (N, 6)
            State history from propagate().
        times : ndarray, shape (N,)
            Time history from propagate().

        Returns
        -------
        dict
            Dictionary with keys: apogee_altitude, apogee_time, flight_time,
            downrange_distance, impact_velocity.
        """
        altitudes = states[:, 2]
        apogee_idx = np.argmax(altitudes)

        return {
            "apogee_altitude_m": float(altitudes[apogee_idx]),
            "apogee_time_s": float(times[apogee_idx]),
            "flight_time_s": float(times[-1]),
            "downrange_distance_m": float(states[-1, 0]),
            "impact_velocity_mps": float(
                np.linalg.norm(states[-1, 3:6])
            ),
        }

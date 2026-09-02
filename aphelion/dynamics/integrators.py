"""Numerical integration methods for ordinary differential equations."""

import numpy as np


def rk4(derivs, state0, t_span, dt, args=()):
    """Fixed-step 4th-order Runge-Kutta integrator.

    Parameters
    ----------
    derivs : callable
        Derivative function with signature derivs(state, t, *args) -> dstate/dt.
    state0 : array_like
        Initial state vector.
    t_span : tuple[float, float]
        Integration interval (t_start, t_end).
    dt : float
        Fixed time step. Must be positive.
    args : tuple, optional
        Extra arguments passed to derivs.

    Returns
    -------
    states : ndarray, shape (N, len(state0))
        State at each time step (including initial state).
    times : ndarray, shape (N,)
        Corresponding time values.

    Raises
    ------
    ValueError
        If dt is not positive or t_span is invalid.
    """
    if dt <= 0:
        raise ValueError(f"dt must be positive, got {dt}")
    if t_span[1] < t_span[0]:
        raise ValueError(f"t_span end ({t_span[1]}) < start ({t_span[0]})")

    state0 = np.asarray(state0, dtype=float)
    t_start, t_end = t_span

    n_steps = int(np.ceil((t_end - t_start) / dt))
    if n_steps == 0:
        return state0.reshape(1, -1), np.array([t_start])

    # Pre-allocate arrays
    states = np.empty((n_steps + 1, len(state0)))
    times = np.empty(n_steps + 1)

    states[0] = state0
    times[0] = t_start

    state = state0.copy()
    t = t_start

    for i in range(n_steps):
        k1 = derivs(state, t, *args)
        k2 = derivs(state + 0.5 * dt * k1, t + 0.5 * dt, *args)
        k3 = derivs(state + 0.5 * dt * k2, t + 0.5 * dt, *args)
        k4 = derivs(state + dt * k3, t + dt, *args)

        state = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t_start + (i + 1) * dt

        states[i + 1] = state
        times[i + 1] = t

    return states, times

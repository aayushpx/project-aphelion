# Weekly Log -2026-06-22 12:03

## Tasks Completed
- [x] Refactored `FlightPropagator` class to support mass depletion during powered flight phases
- [x] Upgraded force vector models to include active propulsive thrust alongside gravity and atmospheric drag
- [x] Implemented a 4th order Runge-Kutta integration loop handling multi-dimensional state vector derivatives
- [x] Successfully generated a 2D spatial trajectory profile displaying a realistic suborbital flight path

## Challenges / Roadblocks
- Initial attempts to introduce a horizontal velocity component caused the thrust unit vector to collapse entirely along the horizontal axis, causing the rocket to drop below ground level. Resolved by enforcing a strict altitude termination constraint ($z < 0$) in the propagation loop.

## Learnings / Notes
- Storing state as `[x, y, z, vx, vy, vx]` allows standard NumPy vector operations to compute forces across all dimensions simultaneously without manual component looping.
- RK4 is superior to Euler integration because it samples derivatives at step midpoints, capturing rapid changes in acceleration during high-dynamic phases like powered ascent and atmospheric re-entry.
- Using linear interpolation at the end of the simulation ensures the final impact coordinate snaps precisely to the ground boundary, removing discrete timestep rounding errors.

## Code Snippets / Commands
```python
# Resolving initial state vector orientation via launch rail angle
launch_angle_rad = np.radians(85.0)
rail_speed = 0.1 

init_vx = rail_speed * np.cos(launch_angle_rad)
init_vz = rail_speed * np.sin(launch_angle_rad)
initial_flight_vector = [0.0, 0.0, 0.0, init_vx, 0.0, init_vz]
```


## Performance Metrics:
- **Trajectory Apogee**: ~700 meters achieved at approximately 11-12 seconds using a simulated 80 N, 3.5s burn profile.
- **Downrange Impact Coordinate**: ~460 meters from launch pad location.

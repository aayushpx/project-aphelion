import numpy as np
import matplotlib.pyplot as plt
import os
import csv

output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(output_dir, exist_ok=True)
csv_filename = os.path.join(output_dir, "nominal_trajectory.csv")

script_dir = os.path.dirname(__file__)
media_plots_dir = os.path.join(script_dir, "..", "..", "..", "media", "plots")
os.makedirs(media_plots_dir, exist_ok=True)

class FlightPropagator:
    """
    3DOF Trajectory Propagator for suborbital launch vehicles.
    Implements 4th-order Runge-Kutta numerical integration with
    altitude-dependent atmospheric density and time-varying mass profiles.
    """
    def __init__(self, dry_mass, propellant_mass, area,
                 cd, thrust_nominal, burn_time):
        self.dry_mass = dry_mass  # kg (structural mass)
        self.prop_mass_init = propellant_mass  # kg (usable fuel)
        self.area = area  # m^2 (cross-sectional area)
        self.cd = cd      # Drag coefficient (dimensionless)
        self.thrust_nominal = thrust_nominal  # N
        self.burn_time = burn_time  # s

        # Physical constants
        self.g0 = 9.80665  # standard gravity (m/s^2)

        # Mass flow rate (assuming constant thrust and burn time)
        self.mdot = self.prop_mass_init / self.burn_time if self.burn_time > 0 else 0.0


    def get_mass(self, t):
        """Calculates instantaneous vehicle mass due to propellant depletion."""
        if t < self.burn_time:
            return self.dry_mass + self.prop_mass_init - (self.mdot * t)
        return self.dry_mass

    def get_density(self, altitude):
        """Barometric density model using a standard scale height."""
        rho0 = 1.255 # Standard sea-level density (kg/m^3)
        h_scale = 8500.0 # Scale height (m)
        if altitude < 0: 
            return rho0
        return rho0 * np.exp(-altitude / h_scale)  

    def derivatives(self, state, t):
        """
        Computes the state derivative vector [velocity, acceleration].

        State vector map:
            state[0:3] = position (x, y, z) in meters
            state[3:6] = velocity (vx, vy, vz) in m/s
        """
        x, y, z, vx, vy, vz = state
        vel = np.array([vx, vy, vz])
        speed = np.linalg.norm(vel) # total speed magnitude
        current_mass = self.get_mass(t)

        # Gravitational force vector
        f_gravity = np.array([0.0, 0.0, -current_mass * self.g0])

        # Aerodynamic drag force vector
        if speed > 1e-6:
            rho = self.get_density(z)
            drag_mag = 0.5 * rho * (speed**2) * self.cd * self.area
            f_drag = -drag_mag * (vel / speed)

        else:
            f_drag = np.zeros(3)


        # Propulsive thrust force vector
        if t < self.burn_time:
            if speed > 1e-6:
                f_thrust = self.thrust_nominal * (vel / speed)
            else: 
                f_thrust = np.array([0.0, 0.0, self.thrust_nominal])
        else:
            f_thrust = np.zeros(3)

        # Equations of motion: Sum(F) = m * a
        total_force = f_gravity + f_drag + f_thrust
        accel = total_force / current_mass

        return np.concatenate([vel, accel])


    def propagate(self, initial_state, dt, max_duration = 100.0):
        """Executes RK4 integration across the flight envelope"""
        t_arr = [0.0]
        history = [np.array(initial_state, dtype = float)]
        current_state = np.array(initial_state, dtype = float)
        t = 0.0

        while t < max_duration:
            k1 = self.derivatives(current_state, t)
            k2 = self.derivatives(current_state + (dt/2) * k1, t + dt/2)
            k3 = self.derivatives(current_state + (dt/2) * k2, t + dt/2)
            k4 = self.derivatives(current_state + dt * k3, t + dt)
            
            current_state += (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
            t += dt

            # Record state
            history.append(current_state.copy())
            t_arr.append(t)

            # Terminate propagation is vehicle impacts surface
            if current_state[2] < -1e-3:
                break

        # --- Post-Flight Data Clean-Up ---
        history_arr = np.array(history)
        time_arr = np.array(t_arr)

        # If the last recorded point dipped below the ground, 
        # interpolate the impact state
        if history_arr[-1, 2] < 0.0 and len(history_arr) > 1:
            last_state = history_arr[-2]
            overshoot_state = history_arr[-1]

            # Find the fraction of the timestep where z crossed exactly 0.0
            # fraction = (0 - z_prev) / (z_curr - z_prev)
            z_prev = last_state[2]
            z_curr = overshoot_state[2]
            fraction = (0.0 - z_prev) / (z_curr - z_prev)

            # Linearly interpolate time and the state vector
            t_impact = time_arr[-2] + fraction * dt
            state_impact = last_state + fraction * (overshoot_state - last_state)
            state_impact[2] = 0.0  # Explicitly snap altitude to exactly 0

            # Replace the overshoot point with the precise impact point
            history_arr[-1] = state_impact
            time_arr[-1] = t_impact

        return history_arr, time_arr

sim = FlightPropagator(
    dry_mass = 1.0,
    propellant_mass = 0.3,
    area = 0.008,
    cd = 0.45,
    thrust_nominal = 80.0,
    burn_time = 3.5
)

launch_angle_deg = 85.0
launch_angle_rad = np.radians(launch_angle_deg)

rail_speed = 0.1 # m/s
init_vx = rail_speed * np.cos(launch_angle_rad)
init_vz = rail_speed * np.sin(launch_angle_rad) 

# Initial state vector: [x, y, z, vx, vy, vz]
initial_flight_vector = [0.0, 0.0, 0.0, init_vx, 0.0, init_vz]

# Run the propagator
history, time = sim.propagate(initial_flight_vector, dt=0.01, max_duration=40.0)

# --- Clear Multi-Plot Telemetry Dashboard ---
plt.figure(figsize=(12, 5))

# Plot 1: Altitude Over Time
plt.figure(figsize=(6, 4))
plt.plot(time, history[:, 2], 'b-', linewidth=2)
plt.ylabel("Altitude (meters)")
plt.xlabel("Time (seconds)")
plt.title("Flight Telemetry: Altitude vs Time")
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig(os.path.join(media_plots_dir, "altitude_profile.png"), dpi=300, bbox_inches='tight')
plt.close()

# Plot 2: Range Profile (2D Flight Path Profile)
plt.figure(figsize=(6, 4))
plt.plot(history[:, 0], history[:, 2], 'g-', linewidth=2)
plt.ylabel("Altitude (meters)")
plt.xlabel("Downrange Distance (meters)")
plt.title("Mission Profile: 2DOF Spatial Trajectory")
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig(os.path.join(media_plots_dir, "spatial_profile.png"), dpi=300, bbox_inches='tight')
plt.close()

print(f"\n[SUCCESS] Portfolio assets saved to: {os.path.abspath(media_plots_dir)}")

print(f"Compiling flight datasets... Writing to {csv_filename}")

with open(csv_filename, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["time_s", "pos_x_m", "pos_y_m",
                     "alt_z_m", "vel_x_mps", "vel_y_mps",
                     "vel_z_mps"])
    for t, state in zip(time, history):
        writer.writerow([
            f"{t:.4f}",
            f"{state[0]:.4f}", f"{state[1]:.4f}", f"{state[2]:.4f}",
            f"{state[3]:.4f}", f"{state[4]:.4f}", f"{state[5]:.4f}"
        ])

print("Data logging sequence complete. Flight baseline stored successfully")

import numpy as np
import matplotlib.pyplot as plt
import math

class FlightPropagator:
    def __init__(self, mass, area, cd):
        self.mass = mass  # kg
        self.area = area  # m^2
        self.cd = cd      # Drag coefficient
        self.g = 9.80665  # m/s^2

    def get_density(self, altitude):
        """Standard Atmosphere Model"""
        rho0 = 1.255
        if altitude < 0: return rho0
        h_scale = 8500
        # formula: rho = rho0 * e^(-h / h_scale)
        rho = rho0 * np.exp(-altitude / 8500)  
        return rho

    def derivatives(self, state, t):
        """
        Calculates the instantaneous rates of change: [velocity, acceleration]
        'state' contains [x, y, z, vx, vy, vz]
        """
        x, y, z, vx, vy, vz = state
        
        velocity = np.array([vx, vy, vz])
        speed = np.linalg.norm(velocity) # total speed magnitude
        f_gravity = np.array([0, 0, -self.mass * self.g])

        # Drag
        if speed > 0:
            rho = self.get_density(z)
            drag_mag = 0.5 * rho * (speed**2) * self.cd * self.area
            f_drag = -drag_mag * (velocity / speed)

        else:
            f_drag = np.array([0, 0, 0])

        total_force = f_gravity + f_drag
        accel = total_force / self.mass

        return np.concatenate([velocity, accel])


    def propagate(self, initial_state, dt, duration):
        """The main loop using RK4 integration"""
        t_arr = np.arange(0, duration, dt)
        history = [initial_state]
        current_state = np.array(initial_state)

        for t in t_arr[:-1]:
            k1 = self.derivatives(current_state, t)
            k2 = self.derivatives(current_state + (dt/2) * k1, t + dt/2)
            k3 = self.derivatives(current_state + (dt/2) * k2, t + dt/2)
            k4 = self.derivatives(current_state + dt * k3, t + dt)
            
            current_state = current_state + (dt/6) * (k1 + 2*k2 + 2*k3 +
                                                      k4)

            if current_state[2] < 0:
                break

            history.append(current_state)

        return np.array(history), t_arr[:len(history)]

sim = FlightPropagator(mass = 1.0, area = 0.01, cd = 0.5)
history, time = sim.propagate([0,0,0, 0,0,100], dt = 0.01, duration = 20)

plt.plot(time, history[:, 2])
plt.ylabel("Altitude (m)")
plt.xlabel("Time (s)")
plt.show()

import numpy as np
import matplotlib.pyplot as plt

class FlightPropagator:
    def __init__(self, mass, area, cd):
        self.mass = mass  # kg
        self.area = area  # m^2
        self.cd = cd      # Drag coefficient
        self.g = 9.80665  # m/s^2

    def get_density(self, altitude):
        """Standard Atmosphere Model"""
        # TODO: Implement a basic exponential decay model for air density 
        # rho = rho0 * exp(-h/h_scale)
        return 1.225

    def derivatives(self, state, t):
        """
        Calculates the instantaneous rates of change: [velocity, acceleration]
        'state' contains [x, y, z, vx, vy, vz]
        """
        # 1. Extract position and velocity from state
        # 2. Calculate Gravity vector
        # 3. Calculate Drag vector
        # 4. Return derivatives
        pass

    def propagate(self, initial_state, dt, duration):
        """The main loop using RK4 integration"""
        # time-stepping
        pass

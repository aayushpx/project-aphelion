"""Physical constants used across Project Aphelion.

All values are SI units unless otherwise noted.
References: CODATA 2018, IERS Conventions 2010.
"""

# --- Gravitational ---
# Standard gravitational parameter for Earth (m^3/s^2)
MU_EARTH = 3.986004418e14

# Universal gravitational constant (m^3 kg^-1 s^-2)
G = 6.67430e-11

# Earth mass (kg)
M_EARTH = 5.9722e24

# --- Earth geometry ---
# Earth mean equatorial radius (m)
R_EARTH = 6.378137e6

# Earth flattening factor (dimensionless)
F_EARTH = 1.0 / 298.257223563

# --- Standard gravity ---
# Standard acceleration of gravity at sea level (m/s^2)
G0 = 9.80665

# --- Atmosphere (US Standard Atmosphere 1976) ---
# Sea-level atmospheric density (kg/m^3)
RHO_SEA_LEVEL = 1.225

# Scale height for exponential atmosphere model (m)
H_SCALE = 8500.0

# --- Reference ---
# Standard gravitational parameter for the Sun (m^3/s^2)
MU_SUN = 1.32712440018e20

# J2 zonal harmonic coefficient for Earth (dimensionless)
J2 = 1.08263e-3

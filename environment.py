from ambiance import Atmosphere
import numpy as np

# This file defines the Environment class, which models the atmospheric conditions and wind effects that the rocket experiences during its flight. 

class Environment:

    # Defining initial launch environment
    def __init__(self, launchpad_altitude_m=0, wind_vector=[0.0, 0.0, 0.0], temp_offset_c=0.0):
        self.launchpad_altitude = launchpad_altitude_m
        self.wind_vector = np.array(wind_vector)
        self.surface_temp_offset = temp_offset_c # This allows you to simulate hotter or colder days by adding an offset to the standard atmospheric temperature profile.
        self.tropopause_altitude = 11000.0  # Altitude at which the temperature offset effect completely washes out (meters)

    
    def get_wind_vector(self, rocket_altitude_m=0):
        return self.wind_vector
    
    # This function calculates the temperature offset based on the rocket's true altitude. The offset is strongest at the surface and linearly decreases to zero at the tropopause, simulating how temperature variations near the ground can affect atmospheric conditions.
    def get_current_offset(self, true_alt):
        if true_alt >= self.tropopause_altitude:
            return 0.0
        washout_factor = 1.0 - (true_alt / self.tropopause_altitude) # Linearly decrease the offset effect with altitude, completely washing out at the tropopause
        return self.surface_temp_offset * washout_factor 
    
    # This function calculates the air density at the rocket's altitude, taking into account the temperature offset. It uses the standard atmospheric model to get the base density and then adjusts it based on the ratio of standard temperature to the new temperature with the offset applied. This allows for more accurate simulation of aerodynamic forces under varying temperature conditions.
    def get_density(self, rocket_altitude_m):
        if np.isnan(rocket_altitude_m):
            return 1.225 # kg/m^3 at sea level under standard conditions
        true_alt = self.launchpad_altitude + rocket_altitude_m
        current_atm = Atmosphere(true_alt)
        standard_temp = current_atm.temperature[0]
        current_offset = self.get_current_offset(true_alt)
        new_temp = standard_temp + current_offset
        standard_density = current_atm.density[0]
        return standard_density * (standard_temp / new_temp)
    
    # This function calculates the temperature at the rocket's altitude, including the effect of the surface temperature offset.
    def get_temperature(self, rocket_altitude_m):
        if np.isnan(rocket_altitude_m):
            return 288.15 + self.surface_temp_offset
        true_alt = self.launchpad_altitude + rocket_altitude_m
        current_atm = Atmosphere(true_alt)
        current_offset = self.get_current_offset(true_alt)
        return current_atm.temperature[0] + current_offset
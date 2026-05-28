from ambiance import Atmosphere
import numpy as np

class Environment:
    def __init__(self, launchpad_altitude_m=0, wind_vector=[0.0, 0.0, 0.0], temp_offset_c=0.0):
        self.launchpad_altitude = launchpad_altitude_m
        self.wind_vector = np.array(wind_vector)
        self.surface_temp_offset = temp_offset_c
        self.tropopause_altitude = 11000.0  # in meters

    def get_wind_vector(self, rocket_altitude_m=0):
        return self.wind_vector
    
    def get_current_offset(self, true_alt):
        if true_alt >= self.tropopause_altitude:
            return 0.0
        washout_factor = 1.0 - (true_alt / self.tropopause_altitude)
        return self.surface_temp_offset * washout_factor
    
    def get_density(self, rocket_altitude_m):
        if np.isnan(rocket_altitude_m):
            return 1.225
        true_alt = self.launchpad_altitude + rocket_altitude_m
        current_atm = Atmosphere(true_alt)
        standard_temp = current_atm.temperature[0]
        current_offset = self.get_current_offset(true_alt)
        new_temp = standard_temp + current_offset
        standard_density = current_atm.density[0]
        return standard_density * (standard_temp / new_temp)
    
    def get_temperature(self, rocket_altitude_m):
        if np.isnan(rocket_altitude_m):
            return 288.15 + self.surface_temp_offset
        true_alt = self.launchpad_altitude + rocket_altitude_m
        current_atm = Atmosphere(true_alt)
        current_offset = self.get_current_offset(true_alt)
        return current_atm.temperature[0] + current_offset
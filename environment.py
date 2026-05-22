from ambiance import Atmosphere
import numpy as np

class Environment:
    def __init__(self, launchpad_altitude_m=0):
        self.launchpad_altitude = launchpad_altitude_m
    def get_density(self, rocket_altitude_m):

        if np.isnan(rocket_altitude_m):
            return 1.225
        
        true_alt = self.launchpad_altitude + rocket_altitude_m
        current_atm = Atmosphere(true_alt)
        return current_atm.density[0]
    
    def get_temperature(self, rocket_altitude_m):

        if np.isnan(rocket_altitude_m):
            return 288.15
        
        true_alt = self.launchpad_altitude + rocket_altitude_m
        current_atm = Atmosphere(true_alt)
        return current_atm.temperature[0]
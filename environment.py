from ambiance import Atmosphere

class Environment:
    def __init__(self, launchpad_altitude_m=0):
        self.launchpad_altitude = launchpad_altitude_m
    def get_density(self, rocket_altitude_m):
        true_alt = self.launchpad_altitude + rocket_altitude_m
        current_atm = Atmosphere(true_alt)
        return current_atm.density[0]
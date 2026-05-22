import numpy as np
from scipy.interpolate import interp1d

class Rocket:
    def __init__(self, manual_diameter, drag_file=None, motor_file=None, mass_file=None):
        self.diameter_m = manual_diameter
        self.reference_area = np.pi * (self.diameter_m / 2)**2

        self.cd_func = lambda mach: 0.75
        self.thrust_func = lambda time: 0.0
        self.mass_func = lambda time: 1.0

        if drag_file:
            self.load_drag_curve(drag_file)

        if motor_file:
            self.load_motor_curve(motor_file)

        if mass_file:
            self.load_mass_curve(mass_file)

    def load_motor_curve(self, motor_file):
        data = np.loadtxt(motor_file, delimiter=',', comments='#')
        raw_time = data[:, 0] 
        raw_thrust = data[:, 1]   

        unique_time, unique_indices = np.unique(raw_time, return_index=True)
        unique_thrust = raw_thrust[unique_indices]
        
        self.thrust_func = interp1d(unique_time, unique_thrust, kind='linear', bounds_error=False, fill_value=(0.0, 0.0))

    def get_thrust(self, current_time):
        return float(self.thrust_func(current_time))

    def load_drag_curve(self, drag_file):
        data = np.loadtxt(drag_file, delimiter=',', comments='#')
        raw_mach = data[:, 0] 
        raw_cd = data[:, 1]   

        unique_mach, unique_indices = np.unique(raw_mach, return_index=True)
        unique_cd = raw_cd[unique_indices]
        
        self.cd_func = interp1d(unique_mach, unique_cd, kind='linear', bounds_error=False, fill_value=(unique_cd[0], unique_cd[-1]))

    def get_cd(self, current_mach):
        drag_value = float(self.cd_func(current_mach))
        if np.isnan(drag_value):
            return 0.75
        return drag_value
    
    def load_mass_curve(self, mass_file):
        data = np.loadtxt(mass_file, delimiter=',', comments='#')
        raw_time = data[:, 0] 
        raw_mass_grams = data[:, 1]   

        raw_mass_kg = raw_mass_grams / 1000

        unique_time, unique_indices = np.unique(raw_time, return_index=True)
        unique_mass = raw_mass_kg[unique_indices]
        
        self.mass_func = interp1d(unique_time, unique_mass, kind='linear', bounds_error=False, fill_value=(unique_mass[0], unique_mass[-1]))
    
    def get_mass(self, current_time):
        mass_value = float(self.mass_func(current_time))
        if np.isnan(mass_value):
            return 1.0
        return mass_value
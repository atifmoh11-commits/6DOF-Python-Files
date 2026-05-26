import numpy as np
from scipy.interpolate import interp1d

class Rocket:
    def __init__(self, manual_diameter, drag_file=None, motor_file=None, mass_file=None, cg_file=None, moi_file=None):
        self.diameter_m = manual_diameter
        self.reference_area = np.pi * (self.diameter_m / 2)**2

        self.cd_func = lambda mach: 0.75
        self.thrust_func = lambda time: 0.0
        self.mass_func = lambda time: 1.0
        self.cg_func = lambda time: 0.5
        self.moi_func = lambda time: 0.05

        if drag_file:
            self.load_drag_curve(drag_file)

        if motor_file:
            self.load_motor_curve(motor_file)

        if mass_file:
            self.load_mass_curve(mass_file)

        if cg_file:
            self.load_cg_curve(cg_file)

        if moi_file:
            self.load_moi_curve(moi_file)

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
    
    def load_cg_curve(self, cg_file):
        data = np.loadtxt(cg_file, delimiter=',', comments='#')
        raw_time = data[:, 0] 
        raw_cg_meters = data[:, 1]   

        unique_time, unique_indices = np.unique(raw_time, return_index=True)
        unique_cg = raw_cg_meters[unique_indices]
        
        self.cg_func = interp1d(unique_time, unique_cg, kind='linear', bounds_error=False, fill_value=(unique_cg[0], unique_cg[-1]))
    def get_cg(self, current_time):
        cg_value = float(self.cg_func(current_time))
        if np.isnan(cg_value):
            return 0.5
        return cg_value
    
    def load_moi_curve(self, moi_file):
        data = np.loadtxt(moi_file, delimiter=',', comments='#')
        raw_time = data[:, 0] 
        raw_longitudinal = data[:, 1]
        raw_rotational = data[:, 2]   

        unique_time, unique_indices = np.unique(raw_time, return_index=True)
        unique_long = raw_longitudinal[unique_indices]
        unique_rot = raw_rotational[unique_indices]
        
        self.moi_long_func = interp1d(unique_time, unique_long, kind='linear', bounds_error=False, fill_value=(unique_long[0], unique_long[-1]))
        self.moi_rot_func = interp1d(unique_time, unique_rot, kind='linear', bounds_error=False, fill_value=(unique_rot[0], unique_rot[-1]))

    def get_inertia_tensor(self, current_time):
        i_long = float(self.moi_long_func(current_time))
        i_rot = float(self.moi_rot_func(current_time))
        if np.isnan(i_long):
            i_long = 0.05
        if np.isnan(i_rot):
            i_rot = 0.001
        return np.array([[i_rot, 0, 0], [0, i_long, 0], [0, 0, i_long]])
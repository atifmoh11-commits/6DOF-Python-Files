import numpy as np
from scipy.interpolate import interp1d

# This file defines the Rocket class, which encapsulates all the properties and behaviors of the rocket, including its geometry, mass, center of gravity, moments of inertia, and how these properties change over time. The class includes methods to load data from files for thrust, drag coefficient, mass, center of gravity, and moments of inertia, as well as methods to retrieve these values at any given time during the simulation. The get_inertia_tensor method returns the inertia tensor based on the current time, which is essential for calculating the rocket's rotational dynamics in the physics calculations.

class Rocket:
    def __init__(self, diameter, nose_length, num_fins, fin_root_chord, fin_tip_chord, fin_span, fin_sweep, dist_to_fins, fin_cant_angle=0.0, drag_file=None, motor_file=None, mass_file=None, cg_file=None, moi_file=None):
        # Defining Rocket properties
        self.diameter_m = diameter
        self.radius_m = diameter / 2.0
        self.reference_area = np.pi * (self.radius_m)**2

        self.nose_length = nose_length
        self.num_fins = num_fins
        self.fin_root_chord = fin_root_chord
        self.fin_tip_chord = fin_tip_chord
        self.fin_span = fin_span
        self.fin_sweep = fin_sweep
        self.dist_to_fins = dist_to_fins
        self.fin_cant_angle_rad = np.radians(fin_cant_angle)

        # Default functions that can be overridden by loading data from files
        self.cd_func = lambda mach: 0.75
        self.thrust_func = lambda time: 0.0
        self.mass_func = lambda time: 1.0           
        self.cg_func = lambda time: 0.5
        self.moi_long_func = lambda time: 0.05
        self.moi_rot_func = lambda time: 0.001

        # Load data from files if provided
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

    # Data loading functions
    # isnan checks are included in the get_ functions to handle any potential issues with the data files, such as missing values or formatting errors. If a value is NaN, a default value is returned to ensure the simulation can continue running without crashing.
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
        return np.array([[i_long, 0, 0], [0, i_long, 0], [0, 0, i_rot]]) # The inertia tensor is a 3x3 matrix that describes how the rocket's mass is distributed in space, which affects how it responds to torques and rotational forces. In this case, we assume the rocket has symmetry around its longitudinal axis, so the moments of inertia around the x and y axes are the same (i_long), while the moment of inertia around the z-axis (i_rot) can be different due to the distribution of mass along the length of the rocket.
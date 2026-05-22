import numpy as np
from scipy.interpolate import interp1d

class Rocket:
    def __init__(self, manual_mass, manual_diameter, drag_file=None):
        self.dry_mass_kg = manual_mass
        self.diameter_m = manual_diameter
        self.reference_area = np.pi * (self.diameter_m / 2)**2

        self.cd_func = lambda mach: 0.75

        if drag_file:
            self.load_drag_curve(drag_file)

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
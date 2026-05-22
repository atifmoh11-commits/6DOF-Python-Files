import numpy as np

class Rocket:
    def __init__(self, ork_file_path=None, manual_mass=None, manual_diameter=None):
        self.file_path = ork_file_path
        if self.file_path:
            print(f"System ready to parse OpenRocket file: {self.file_path}")
            self.dry_mass = 0.0
            self.diameter = 0.0
        else:
            self.dry_mass = manual_mass
            self.diameter = manual_diameter
        self.radius = self.diameter/2.0
        self.reference_area = np.pi * (self.radius ** 2)
        self.cg_location_m = 0.0
        self.inertia_xx = 0.0
        self.inertia_yy = 0.0
        self.inertia_zz = 0.0


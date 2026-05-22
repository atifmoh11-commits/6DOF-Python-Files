import numpy as np

def calculate_1dof_acceleration(rocket, environment, current_altitude_m, current_velocity_ms, current_thrust_n):
    g = 9.81
    force_gravity = rocket.dry_mass_kg * g
    rho = environment.get_density(current_altitude_m)
    current_temperature = environment.get_temperature(current_altitude_m)
    speed_of_sound = np.sqrt(1.4 * 287.05 * current_temperature)
    current_mach = abs(current_velocity_ms) / speed_of_sound
    drag_coefficient = rocket.get_cd(current_mach)
    force_drag = 0.5 * rho * (current_velocity_ms**2) * drag_coefficient * rocket.reference_area
    if current_velocity_ms < 0:
        force_drag = -1 * force_drag
    force_net = current_thrust_n - force_gravity - force_drag
    if current_altitude_m <= 0 and force_net < 0:
        force_net = 0
    acceleration = force_net / rocket.dry_mass_kg
    return acceleration
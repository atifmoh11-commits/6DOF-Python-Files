def calculate_1dof_acceleration(rocket, environment, current_altitude_m, current_velocity_ms, current_thrust_n):
    g = 9.81
    force_gravity = rocket.dry_mass * g
    rho = environment.get_density(current_altitude_m)
    drag_coefficient = 0.6
    force_drag = 0.5 * rho * (current_velocity_ms**2) * drag_coefficient * rocket.reference_area
    if current_velocity_ms < 0:
        force_drag = -1*force_drag
    force_net = current_thrust_n - force_gravity - force_drag
    acceleration = force_net/rocket.dry_mass
    return acceleration
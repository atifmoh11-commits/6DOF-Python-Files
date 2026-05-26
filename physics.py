import numpy as np

def quat_to_rot_matrix(quat):
    w, x, y, z = quat
    M = np.array([
        [1 - 2*y**2 - 2*z**2,     2*x*y - 2*w*z,         2*x*z + 2*w*y],
        [2*x*y + 2*w*z,           1 - 2*x**2 - 2*z**2,   2*y*z - 2*w*x],
        [2*x*z - 2*w*y,           2*y*z + 2*w*x,         1 - 2*x**2 - 2*y**2]
    ])
    return M

def calculate_6dof_kinematics(rocket, environment, pos, vel, quat, omega, current_thrust_n, current_mass_kg, inertia_tensor):
    rot_matrix = quat_to_rot_matrix(quat)
    rocket_pointing_dir = rot_matrix @ np.array([0, 0, 1])

    g = np.array([0, 0, -9.81])
    force_gravity = current_mass_kg * g
    speed = np.linalg.norm(vel)
    rho = environment.get_density(pos[2])
    temp = environment.get_temperature(pos[2])

    speed_of_sound = np.sqrt(1.4 * 287.05 * temp)
    current_mach = speed / speed_of_sound

    if speed > 0.1:
        drag_dir = -vel / speed
        drag_coefficient = rocket.get_cd(current_mach)
        force_drag = 0.5 * rho * (speed**2) * drag_coefficient * rocket.reference_area * drag_dir
    else:
        force_drag = np.array([0.0, 0.0, 0.0])

    thrust_vec = rocket_pointing_dir * current_thrust_n
    force_net = thrust_vec + force_gravity + force_drag

    if pos[2] <= 0 and force_net[2] < 0:
        force_net[2] = 0

    acceleration = force_net / current_mass_kg

    torque_net = np.array([0.0, 0.0, 0.0])  # Placeholder for net torque calculation
    inertia_inv = np.linalg.inv(inertia_tensor)
    gyroscopic_torque = np.cross(omega, inertia_tensor @ omega)

    angular_acceleration = inertia_inv @ (torque_net - gyroscopic_torque)

    return acceleration, angular_acceleration
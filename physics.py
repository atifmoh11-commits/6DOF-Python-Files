import numpy as np

def quat_to_rot_matrix(quat):
    w, x, y, z = quat
    M = np.array([
        [1 - 2*y**2 - 2*z**2,     2*x*y - 2*w*z,         2*x*z + 2*w*y],
        [2*x*y + 2*w*z,           1 - 2*x**2 - 2*z**2,   2*y*z - 2*w*x],
        [2*x*z - 2*w*y,           2*y*z + 2*w*x,         1 - 2*x**2 - 2*y**2]
    ])
    return M

def calculate_aerodynamics(rocket, alpha_rads):
    cn_nose = 2.0
    cp_nose = 0.5 * rocket.nose_length
    R = rocket.radius_m
    S = rocket.fin_span
    Cr = rocket.fin_root_chord
    Ct = rocket.fin_tip_chord
    Lf = rocket.fin_sweep
    Xr = rocket.dist_to_fins

    k_fb = 1 + (R/ (S + R))

    cn_fins_term1 = 4.0 * rocket.num_fins * (S / rocket.diameter_m)**2
    cn_fins_term2 = 1.0 + np.sqrt(1.0 + (2.0 * Lf / (Cr + Ct))**2)
    cn_fins = k_fb * (cn_fins_term1 / cn_fins_term2)

    cp_fins = Xr + (Lf / 3.0) * ((Cr + 2.0 * Ct) / (Cr + Ct)) + (1.0 / 6.0) * ((Cr + Ct) - (Cr * Ct) / (Cr + Ct))

    cn_total = cn_nose + cn_fins
    cp_total = ((cn_nose * cp_nose) + (cn_fins * cp_fins)) / cn_total

    return cn_total, cp_total

def calculate_6dof_kinematics(rocket, environment, pos, vel, quat, omega, current_thrust_n, current_mass_kg, current_cg, inertia_tensor):
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

    wind_vector = environment.get_wind_vector(pos[2])  # Example wind vector (5 m/s in x-direction)
    air_velocity = vel - wind_vector
    airspeed = np.linalg.norm(air_velocity)

    torque_net = np.array([0.0, 0.0, 0.0])  # Placeholder for net torque calculation

    if airspeed > 0.1 and vel[2] > 0:
        air_dir = air_velocity / airspeed
        cos_alpha = np.dot(rocket_pointing_dir, air_dir)
        cos_alpha = np.clip(cos_alpha, -1.0, 1.0)
        alpha = np.arccos(cos_alpha)

        cn_total, cp_total = calculate_aerodynamics(rocket, alpha)
        normal_force_mag = 0.5 * rho * (airspeed**2) * cn_total * rocket.reference_area * alpha
        lever_arm = cp_total - current_cg
        torque_axis = np.cross(rocket_pointing_dir, air_dir)
        if np.linalg.norm(torque_axis) > 0.001:
            torque_axis = torque_axis / np.linalg.norm(torque_axis)
            torque_net = (normal_force_mag * lever_arm) * torque_axis

        omega_inertial = rot_matrix @ omega

        # accounting for imperfections in rocket that induce roll (fin cant etc.)
        cant_angle_rad = np.radians(0.1)

        fin_area = rocket.fin_span * (rocket.fin_root_chord + rocket.fin_tip_chord) / 2.0
        moment_arm = (rocket.diameter_m / 2.0) + (rocket.fin_span / 2.0)
        cl_alpha = 2.0 * np.pi
        q = 0.5 * rho * (airspeed**2)

        w_roll = np.dot(omega_inertial, rocket_pointing_dir)
        
        roll_force_per_fin = q * fin_area * cl_alpha * cant_angle_rad
        roll_driving_torque_mag = rocket.num_fins * roll_force_per_fin * moment_arm
        roll_damping_torque_mag = -(rocket.num_fins * q * fin_area * cl_alpha * (moment_arm**2) * w_roll) / airspeed

        total_roll_torque_mag = roll_driving_torque_mag + roll_damping_torque_mag
        roll_torque_vec = total_roll_torque_mag * rocket_pointing_dir

        torque_net += roll_torque_vec

        pitch_yaw_omega_inertial = omega_inertial - (w_roll * rocket_pointing_dir)
        damping_factor = 0.05 * rho * airspeed * rocket.reference_area * (rocket.dist_to_fins**2)
        pitch_yaw_damping_torque = -damping_factor * pitch_yaw_omega_inertial
        torque_net += pitch_yaw_damping_torque
        torque_net_body = rot_matrix.T @ torque_net
    else:
        damping_torque_body = -1.0 * omega
        target_dir = np.array([0.0, 0.0, -1.0])
        pendulum_torque_world = 1.0 * np.cross(rocket_pointing_dir, target_dir)
        pendulum_torque_body = rot_matrix.T @ pendulum_torque_world
        torque_net_body = damping_torque_body + pendulum_torque_body

    inertia_inv = np.linalg.inv(inertia_tensor)
    gyroscopic_torque = np.cross(omega, inertia_tensor @ omega)
    angular_acceleration = inertia_inv @ (torque_net_body - gyroscopic_torque)

    return acceleration, angular_acceleration


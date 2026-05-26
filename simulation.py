from physics import calculate_6dof_kinematics
import numpy as np

def flight_loop(time, state, rocket, environment):
    pos = np.array(state[0:3])  # x, y, z
    vel = np.array(state[3:6])  # vx, vy, vz
    quat = np.array(state[6:10])  # q1, q2, q3, q4
    omega = np.array(state[10:13])  # wx, wy, wz

    current_thrust = rocket.get_thrust(time)
    current_mass = rocket.get_mass(time)
    inertia_tensor = rocket.get_inertia_tensor(time)

    acceleration, angular_acceleration = calculate_6dof_kinematics(rocket, environment, pos, vel, quat, omega, current_thrust, current_mass, inertia_tensor)

    w_x, w_y, w_z = omega
    q0, q1, q2, q3 = quat
    dq0 = 0.5 * (-w_x*q1 - w_y*q2 - w_z*q3)
    dq1 = 0.5 * (w_x*q0 - w_y*q3 + w_z*q2)
    dq2 = 0.5 * (w_x*q3 + w_y*q0 - w_z*q1)
    dq3 = 0.5 * (-w_x*q2 + w_y*q1 + w_z*q0)
    d_quat = np.array([dq0, dq1, dq2, dq3])  

    return np.concatenate([vel, acceleration, d_quat, angular_acceleration])

def hit_ground(time, state, rocket, environment):
    if time < 1.0:
        return 100 - (100*time)
    return state[2]

hit_ground.terminal = True
hit_ground.direction = -1
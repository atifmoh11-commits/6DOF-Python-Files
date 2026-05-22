from physics import calculate_1dof_acceleration

def flight_loop(time, state, rocket, environment):
    current_altitude = state[0]
    current_velocity = state[1]

    if time <= 2.0:
        current_thrust = 200.0
    else:
        current_thrust = 0.0

    acceleration = calculate_1dof_acceleration(rocket=rocket, environment=environment, current_altitude_m=current_altitude, current_velocity_ms=current_velocity, current_thrust_n=current_thrust)

    return [current_velocity, acceleration]

def hit_ground(time, state, rocket, environment):
    return state[0]

hit_ground.terminal = True
hit_ground.direction = -1
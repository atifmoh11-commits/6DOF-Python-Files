from physics import calculate_1dof_acceleration

def flight_loop(time, state, rocket, environment):
    current_altitude = state[0]
    current_velocity = state[1]

    current_thrust = rocket.get_thrust(time)
    acceleration = calculate_1dof_acceleration(rocket=rocket, environment=environment, current_altitude_m=current_altitude, current_velocity_ms=current_velocity, current_thrust_n=current_thrust)

    return [current_velocity, acceleration]

def hit_ground(time, state, rocket, environment):
    if time < 1.0:
        return 100
    return state[0]

hit_ground.terminal = True
hit_ground.direction = -1
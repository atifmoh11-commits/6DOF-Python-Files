import matplotlib.pyplot as plt
from rocket import Rocket
from environment import Environment
from simulation import flight_loop, hit_ground
from scipy.integrate import solve_ivp

#ROCKET GEOMETRY CONFIGURATION (meters)
DIAMETER = 0.080
REFERENCE_AREA = 3.14159 * (DIAMETER / 2.0)**2

NOSE_LENGTH = 0.178
NUM_FINS = 3
FIN_ROOT_CHORD = 0.127
FIN_TIP_CHORD = 0.0635
FIN_SPAN = 0.0927
FIN_SWEEP = 0.1016

# Assuming fins are mounted flush with the bottom of the tube.
# Nose + Tube = total length. 
# Fin root leading edge = total length - root chord = distance from nose tip.
# inches -> meters.
DIST_TO_FINS = 0.965

my_rocket = Rocket(
    diameter=DIAMETER, 
    nose_length=NOSE_LENGTH,
    num_fins=NUM_FINS,
    fin_root_chord=FIN_ROOT_CHORD,
    fin_tip_chord=FIN_TIP_CHORD,
    fin_span=FIN_SPAN,
    fin_sweep=FIN_SWEEP,
    dist_to_fins=DIST_TO_FINS,
    drag_file="drag_data.csv",
    motor_file="motor_data.csv",
    mass_file="mass_data.csv",
    cg_file="cg_data.csv",
    moi_file="moi_data.csv"
)

my_env = Environment(launchpad_altitude_m=0)

time_limit = (0.0, 60.0)
initital_state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #x, y, z, vx, vy, vz, q1, q2, q3, q4, wx, wy, wz

ground_event = lambda t, y: hit_ground(t, y, my_rocket, my_env)
ground_event.terminal = True
ground_event.direction = -1

flight_data = solve_ivp(
    fun=lambda t, y: flight_loop(t, y, my_rocket, my_env),
    t_span=time_limit,
    y0=initital_state,
    events=ground_event,
    max_step=0.01
)

times = flight_data.t
altitudes = flight_data.y[2]
velocities = flight_data.y[5]

apogee = max(altitudes)

plt.figure(figsize=(10, 5))
plt.plot(times, altitudes, label="Altitude (m)", color="blue", linewidth=2)
plt.axhline(y=apogee, color='red', linestyle='--', label=f"Apogee ({apogee:.1f} m)")
plt.xlabel("Time (seconds)")
plt.ylabel("Altitude (meters)")
plt.title("6DOF Rocket Flight Trajectory")
plt.legend()
plt.grid(True)
plt.show()
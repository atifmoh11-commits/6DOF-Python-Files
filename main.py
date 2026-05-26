import matplotlib.pyplot as plt
from rocket import Rocket
from environment import Environment
from simulation import flight_loop, hit_ground
from scipy.integrate import solve_ivp

my_rocket = Rocket(manual_diameter=0.076, drag_file="drag_data.csv", motor_file="motor_data.csv", mass_file="mass_data.csv", cg_file="cg_data.csv", moi_file="moi_data.csv")
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
plt.title("1DOF Rocket Flight Trajectory")
plt.legend()
plt.grid(True)
plt.show()
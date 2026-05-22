import matplotlib.pyplot as plt
from rocket import Rocket
from environment import Environment
from simulation import flight_loop, hit_ground
from scipy.integrate import solve_ivp

my_rocket = Rocket(manual_mass=1, manual_diameter=0.076)
my_env = Environment(launchpad_altitude_m=0)

time_limit = (0.0, 30.0)
initital_state = [0.0, 0.0] #altitude, velocity

flight_data = solve_ivp(
    fun=lambda t, y: flight_loop(t, y, my_rocket, my_env),
    t_span=time_limit,
    y0=initital_state,
    events=lambda t, y: hit_ground(t, y, my_rocket, my_env),
    max_step=0.01
)

times = flight_data.t
altitudes = flight_data.y[0]
velocities = flight_data.y[1]

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
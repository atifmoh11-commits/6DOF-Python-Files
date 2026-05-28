import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import config
from rocket import Rocket
from environment import Environment
from simulation import flight_loop, hit_ground
from scipy.integrate import solve_ivp
from scipy.spatial.transform import Rotation

my_rocket = Rocket(
    diameter=config.DIAMETER, 
    nose_length=config.NOSE_LENGTH,
    num_fins=config.NUM_FINS,
    fin_root_chord=config.FIN_ROOT_CHORD,
    fin_tip_chord=config.FIN_TIP_CHORD,
    fin_span=config.FIN_SPAN,
    fin_sweep=config.FIN_SWEEP,
    dist_to_fins=config.DIST_TO_FINS,
    drag_file=config.DRAG_FILE,
    motor_file=config.MOTOR_FILE,
    mass_file=config.MASS_FILE,
    cg_file=config.CG_FILE,
    moi_file=config.MOI_FILE
)

my_env = Environment(launchpad_altitude_m=config.LAUNCHPAD_ALTITUDE_M, wind_vector=config.WIND_VECTOR, temp_offset_c=config.TEMP_OFFSET_C)

#if you want to change wind direction vector please head to physics.py and change the wind_vector variable in the calculate_6dof_kinematics function. It is currently set to 5 m/s in the x direction. You can change the magnitude and direction as needed.

time_limit = (0.0, config.TIME_LIMIT)
initital_state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #x, y, z, vx, vy, vz, q1, q2, q3, q4, wx, wy, wz

ground_event = lambda t, y: hit_ground(t, y, my_rocket, my_env)
ground_event.terminal = True
ground_event.direction = -1

flight_data = solve_ivp(
    fun=lambda t, y: flight_loop(t, y, my_rocket, my_env),
    t_span=time_limit,
    y0=initital_state,
    events=ground_event,
    max_step=0.01,
)

times = flight_data.t
x_pos, y_pos, z_pos = flight_data.y[0:3]
vx, vy, vz = flight_data.y[3:6]
q0, q1, q2, q3 = flight_data.y[6:10]
altitudes = z_pos
velocities = np.sqrt(vx**2 + vy**2 + vz**2)
apogee = max(altitudes)
apogee_index = np.argmax(altitudes)
apogee_time = times[apogee_index]

quats_scipy = np.vstack((q0, q1, q2, q3)).T
rotations = Rotation.from_quat(quats_scipy)
euler_angles = rotations.as_euler('xyz', degrees=True)

pitch = euler_angles[:, 0]
yaw = euler_angles[:, 1]
roll = np.rad2deg(np.unwrap(np.deg2rad(euler_angles[:, 2])))

accelerations = np.gradient(velocities, times)
mach_numbers = velocities / 343.0

telemetry_data = {
    "Time": times, "X": x_pos, "Y": y_pos, "Z": z_pos,
    "Q0": q0, "Q1": q1, "Q2": q2, "Q3": q3,
    "Velocity": velocities,
    "Acceleration": accelerations,
    "Mach": mach_numbers
}
df = pd.DataFrame(telemetry_data)
df.to_csv("telemetry.csv", index=False)
print(f"Flight complete. Apogee: {apogee:.1f} m. Telemetry saved to CSV.")

# --- 4. BUILD THE DASHBOARD ---
fig = plt.figure(figsize=(16, 10))
fig.suptitle("6DOF Rocket Telemetry Dashboard", fontsize=18, fontweight='bold')

# Subplot 1: 3D Trajectory (Left Half)
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot(x_pos, y_pos, z_pos, label="Flight Path", color="blue", linewidth=2)
ax1.scatter([0], [0], [0], color='green', s=100, label="Launch Pad", marker='s')
ax1.scatter([x_pos[apogee_index]], [y_pos[apogee_index]], [apogee], color='red', s=100, label=f"Apogee ({apogee:.1f} m)")
ax1.set_xlabel("Downrange (m) [Crosswind Direction]")
ax1.set_ylabel("Crossrange (m)")
ax1.set_zlabel("Altitude (m)")
ax1.set_title("3D Flight Trajectory")
ax1.legend()

# Force equal aspect ratio for drift accuracy
max_drift = max(max(abs(x_pos)), max(abs(y_pos)), 10.0)
ax1.set_xlim([-max_drift, max_drift])
ax1.set_ylim([-max_drift, max_drift])

# Subplot 2: Altitude & Velocity (Top Right)
ax2 = fig.add_subplot(222)
color1 = 'tab:blue'
ax2.plot(times, altitudes, color=color1, linewidth=2)
ax2.set_ylabel('Altitude (m)', color=color1)
ax2.tick_params(axis='y', labelcolor=color1)
ax2.grid(True)

ax2_twin = ax2.twinx()  
color2 = 'tab:red'
ax2_twin.plot(times, velocities, color=color2, linewidth=2, linestyle='--')
ax2_twin.set_ylabel('Velocity (m/s)', color=color2)
ax2_twin.tick_params(axis='y', labelcolor=color2)
ax2.set_title("Altitude and Velocity vs. Time")

# Subplot 3: Orientation / Weathercocking (Bottom Right)
ax3 = fig.add_subplot(224)
ax3.plot(times, pitch, label="Pitch (Degrees)", color="purple")
ax3.plot(times, yaw, label="Yaw (Degrees)", color="orange")
ax3.plot(times, roll, label="Roll (Degrees)", color="green")
ax3.axvline(x=apogee_time, color='grey', linestyle=':', label="Apogee Reached")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Tilt Angle (Degrees)")
ax3.set_title("Rocket Orientation (Weathercocking)")
ax3.legend()
ax3.grid(True)

plt.tight_layout()
plt.show()
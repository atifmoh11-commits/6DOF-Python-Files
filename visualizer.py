import pyvista as pv
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation
import time  

# 1. Load the telemetry and 3D model
try: 
    data = pd.read_csv("telemetry.csv")
    mesh = pv.read("rocket_model.obj")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Ensure 'telemetry.csv' and 'rocket_model.obj' are in the same folder!")
    exit()

max_time = data['Time'].iloc[-1]
apogee_idx = data['Z'].idxmax()
apogee_time = data['Time'].iloc[apogee_idx]

dz = np.diff(data['Z'])
burnout_idx = np.argmax(dz)
burnout_time = data['Time'].iloc[burnout_idx]

plotter = pv.Plotter()

# --- AESTHETIC UPGRADES ---
plotter.set_background("#3f3f3f")  # grayish-black background
actor = plotter.add_mesh(mesh, color="green", smooth_shading=True)  # green rocket

plotter.add_axes()
plotter.show_grid(color="gray")

current_time = 0.0
is_playing = False
speed_multiplier = 1.0  # Controls the slo-mo/fast-forward

# 2. The Core Update Function
def update_frame(time_val):
    global current_time
    current_time = time_val
    
    idx = (np.abs(data['Time'] - time_val)).argmin()
    
    x, y, z = data['X'][idx], data['Y'][idx], data['Z'][idx]
    q0, q1, q2, q3 = data['Q0'][idx], data['Q1'][idx], data['Q2'][idx], data['Q3'][idx]
    vel = data['Velocity'][idx]          
    accel = data['Acceleration'][idx]    
    mach = data['Mach'][idx]             
    
    rot = Rotation.from_quat([q1, q2, q3, q0])
    rot_matrix = rot.as_matrix()
    
    # Calculate Pitch and Roll dynamically on the fly
    euler = rot.as_euler('xyz', degrees=True)
    pitch = euler[0]
    yaw = euler[1]
    roll = euler[2]
    
    transform = np.eye(4)
    transform[:3, :3] = rot_matrix
    transform[0, 3] = x
    transform[1, 3] = y
    transform[2, 3] = z
    
    actor.user_matrix = transform
    
    if time_val < burnout_time:
        stage = "POWERED ASCENT"
        color = "orange"
    elif time_val < apogee_time:
        stage = "COASTING"
        color = "cyan"
    else:
        stage = "APOGEE REACHED"
        color = "lime"

    # Upgraded Telemetry HUD with Pitch, Roll, and bright colors
    dashboard_text = (
        f"--- LIVE TELEMETRY ---\n"
        f"Time:  {time_val:.2f} s\n"
        f"Alt:   {z:.1f} m\n"
        f"Down:  {x:.1f} m\n"
        f"Vel:   {vel:.1f} m/s\n"
        f"Accel: {accel:.1f} m/s²\n"
        f"Mach:  {mach:.2f}\n"
        f"Pitch: {pitch:.1f}°\n"
        f"Yaw:   {yaw:.1f}°\n"
        f"Roll:  {roll:.1f}°\n"
        f"Stage: {stage}"
    )
    plotter.add_text(dashboard_text, position="upper_left", font_size=14, name="dashboard", color=color)

# 3. Build the UI Controls

# Main Timeline Slider (Shortened slightly to fit the speed slider)
my_slider = plotter.add_slider_widget(
    callback=update_frame,
    rng=[0, max_time],
    value=0,
    title="Time (seconds)",
    pointa=(0.02, 0.05),
    pointb=(0.60, 0.05),
    style="modern"
)

# Playback Speed Slider (Slo-mo to Fast Forward)
def set_speed(val):
    global speed_multiplier
    speed_multiplier = val

plotter.add_slider_widget(
    callback=set_speed,
    rng=[0.25, 2.0],
    value=1.0,
    title="Playback Speed (x)",
    pointa=(0.65, 0.05),
    pointb=(0.95, 0.05),
    style="modern"
)

def set_play_state(state):
    global is_playing
    is_playing = state

def toggle_spacebar():
    global is_playing
    set_play_state(not is_playing)

# Zoom Functions for Mac Trackpads
def zoom_in():
    plotter.camera.zoom(1.2)

def zoom_out():
    plotter.camera.zoom(0.8)

# Buttons and Keyboard Shortcuts
plotter.add_checkbox_button_widget(
    set_play_state,
    value=False,
    position=(20, 400),
    size=30,
    color_on="green",
    color_off="red"
)

plotter.add_text("Play/Pause (Space)", position=(60, 405), font_size=12, name="play_label", color="white")
plotter.add_text("Zoom: Press 'i' (In) or 'o' (Out)", position=(60, 440), font_size=12, name="zoom_label", color="white")

plotter.add_key_event("space", toggle_spacebar)
plotter.add_key_event("i", zoom_in)
plotter.add_key_event("o", zoom_out)

update_frame(0.0)
print("Launching 6DOF Rocket Telemetry Visualizer...")

# 4. THE MAIN THREAD FIX (MAC OPTIMIZED)
plotter.show(auto_close=False, interactive_update=True)

while plotter.iren.initialized and not plotter._closed:
    if is_playing:
        # Scale the animation speed by the new Speed Slider
        step = 0.05 * speed_multiplier
        new_time = current_time + step
        
        # Stop at the end of the flight instead of looping
        if new_time >= max_time:
            new_time = max_time
            is_playing = False
            print("Flight complete. Animation parked at Apogee.")
            
        my_slider.GetRepresentation().SetValue(new_time)
        update_frame(new_time)
        
    plotter.update()
    time.sleep(0.02)
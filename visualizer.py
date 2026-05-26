import pyvista as pv
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation

try: 
    data = pd.read_csv("telemetry.csv")
    mesh = pv.read("rocket_model.obj")
except FileNotFoundError:
    print(f"Error: {e}")
    print("Ensure 'telemetry.csv' and 'rocket_model.obj' are in the same folder!")
    exit()

plotter = pv.Plotter()

actor = plotter.add_mesh(mesh, color="white", smooth_shading=True)
plotter.add_axes()
plotter.show_grid()

def update_frame(value):
    frame = int(value)

    x, y, z = data['X'][frame], data['Y'][frame], data['Z'][frame]
    q0, q1, q2, q3 = data['Q0'][frame], data['Q1'][frame], data['Q2'][frame], data['Q3'][frame]

    rot = Rotation.from_quat([q1, q2, q3, q0])
    rot_matrix = rot.as_matrix()

    transform = np.eye(4)
    transform[:3, :3] = rot_matrix
    transform[0, 3] = x
    transform[1, 3] = y
    transform[2, 3] = z

    actor.user_matrix = transform
    plotter.render()

max_frame = len(data) - 1
plotter.add_slider_widget(callback=update_frame, rng=[0, max_frame], value=0, title="Flight Timeline", pointa=(0.1, 0.05), pointb=(0.9, 0.05), style="modern")

print("Launching 6DOF Rocket Visualizer...")
plotter.show()
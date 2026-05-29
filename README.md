# Custom 6DOF Rocket Flight Simulator

## Project Overview

The primary goal of this project is to accurately visualize custom rockets in flight in full 3D, while simultaneously providing a highly precise physics engine for apogee predictions, trajectory drift analysis, and weathercocking simulations.

Built entirely in Python from the ground up, it bypasses basic 1D kinematic models to simulate exactly how a rocket translates and rotates in Six Degrees of Freedom (6DOF) under complex, changing atmospheric conditions. The modular architecture decouples the physics logic from the rocket data, allowing the simulation of everything from standard Level 1 certification rockets up to complex, heavy-lift experimental airframes (like the 13.6 kg CASSIE rocket).

---

## Verification & Accuracy Statistics

The simulation engine has been rigorously tested against both established software (OpenRocket) and real-world flight telemetry to verify its mathematical models:

- **Heavy-Lift Experimental (CASSIE Rocket):** The 6DOF Python simulation calculated an apogee of 9,578.2 meters (31,424.5 feet). Compared to the real-world flight telemetry data benchmark of 30,994 feet, the simulation achieved a margin of error of just **~1.38%**.

- **Level 1 Certification Rocket:** For a standard L1 airframe, the 6DOF simulation predicted an apogee of 714 meters, compared to an OpenRocket simulation of 711.4 meters—a difference of just **~2.6 meters**.

- **Visualizer Fidelity:** When comparing real-world launch footage of the CASSIE rocket to the PyVista 3D visualizer replay, the simulated weathercocking, pitch, and roll rates mirrored the physical flight almost exactly.

---

## Python Libraries Used

This project relies on several powerful scientific and visualization libraries to handle the heavy mathematical lifting and graphics:

- **NumPy (`numpy`):** Handles all the core mathematical operations, matrix inversions for the inertia tensor, quaternion normalizations, and 3D vector cross/dot products.

- **SciPy (`scipy`):** * `scipy.integrate.solve_ivp` : The core ODE solver that steps through the flight loop at millisecond precision.
  - `scipy.interpolate.interp1d` : Creates dynamic data curves to handle continuously shifting variables like mass, CG, and motor thrust.
  - `scipy.spatial.transform.Rotation` : Converts the 4D quaternions back into human-readable Euler angles (Pitch, Yaw, Roll) for telemetry.

- **Pandas (`pandas`):** Packages the raw flight state arrays into structured dataframes and exports them to the `telemetry.csv` file.

- **Matplotlib (`matplotlib`):** Generates the post-flight 2D telemetry dashboard, mapping out the altitude, velocity, and weathercocking angles over time.

- **PyVista (`pyvista`):** Powers the real-time 3D interactive visualizer, rendering the 1:1 scale `.obj` rocket model and animating its exact 6DOF translation and rotation.

- **Ambiance (`ambiance`):** Provides the standard `Atmosphere` model to establish a realistic baseline for air density and temperature across different altitudes.

---

## Core Physics & Equations

The simulation engine runs on several fundamental aerospace and physics formulas to dictate the rigid body dynamics. Here is how each mathematical concept directly drives the simulation:

### Newton's Second Law (Linear Translation):

$$a = \frac{F_{thrust} + F_{gravity} + F_{drag}}{m}$$

**Simulation Role:** Calculates the linear acceleration for every microsecond of flight. The engine continuously takes the current motor thrust (pointing exactly where the 3D nose points), subtracts the force of gravity (which dynamically scales with the burning mass of the rocket), and applies the aerodynamic drag force (which strictly pushes in the exact opposite direction of the velocity vector).

---

### Euler's Equations of Motion (Rigid Body Rotation):

$$\alpha = I^{-1}(\tau_{net} - \omega \times (I\omega))$$

**Simulation Role:** Calculates angular acceleration, determining how the rocket rotates, tumbles, or stabilizes. It factors in the net torque from weathercocking, gyroscopic precession (the resistance of a spinning mass to changing direction), and uses an inverse 3x3 inertia matrix ($I$) that constantly updates as propellant burns out.

---

### The Barrowman Equations:

**Simulation Role:** Approximates the Normal Force Coefficient ($C_N$) and aerodynamic Center of Pressure ($C_P$) based on the nosecone and trapezoidal fin geometry. By calculating exactly where the wind forces push on the airframe and comparing that to the rocket's shifting Center of Gravity (CG), the simulation finds the "lever arm." This lever arm dictates exactly how aggressively the crosswind will torque the rocket into a weathercocking maneuver

**Fin-body interference factor:**
$$k_{fb} = 1 + \frac{R}{S + R}$$

**Fin normal force coefficient — term 1 (fin lifting area):**
$$C_{N,fins,1} = \frac{4 N \left(\frac{S}{d}\right)^2}{1}$$

> $N$ = number of fins, $S$ = fin span, $d$ = body diameter

**Fin normal force coefficient — term 2 (sweep correction):**
$$C_{N,fins,2} = 1 + \sqrt{1 + \left(\frac{2 L_f}{C_r + C_t}\right)^2}$$

> $L_f$ = fin sweep length, $C_r$ = root chord, $C_t$ = tip chord

**Combined fin normal force coefficient:**
$$C_{N,fins} = k_{fb} \cdot \frac{C_{N,fins,1}}{C_{N,fins,2}}$$

**Nosecone normal force coefficient (conical):**
$$C_{N,nose} = 2.0$$

**Nosecone center of pressure (conical):**
$$C_{P,nose} = 0.5 \cdot L_{nose}$$

**Fin center of pressure (Mean Aerodynamic Chord — trapezoidal fin):**
$$C_{P,fins} = X_r + \frac{L_f}{3} \cdot \frac{C_r + 2C_t}{C_r + C_t} + \frac{1}{6} \cdot \frac{(C_r + C_t)^2 - C_r C_t}{C_r + C_t}$$

> $X_r$ = distance from nose tip to fin root leading edge

**Total normal force coefficient:**
$$C_{N,total} = C_{N,nose} + C_{N,fins}$$

**Total center of pressure (weighted average):**
$$C_{P,total} = \frac{(C_{N,nose} \cdot C_{P,nose}) + (C_{N,fins} \cdot C_{P,fins})}{C_{N,total}}$$.

---

### Standard Aerodynamic Drag:

$$F_d = \frac{1}{2}\rho v^2 C_d A$$

**Simulation Role:** Opposes the rocket's ascent. The engine dynamically looks up the drag coefficient ($C_d$) from the OpenRocket CSV curves based on the current Mach number. Crucially, the air density ($\rho$) is dynamically fed from the environment model, dropping as the rocket climbs so that drag forces accurately lessen in the upper atmosphere.

---

### Ideal Gas Law (Speed of Sound):

$$a = \sqrt{\gamma R T}$$

**Simulation Role:** Calculates a highly localized dynamic speed of sound. Because the simulation tracks dropping temperatures ($T$) at higher altitudes, the speed of sound also decreases. This means the rocket hits higher Mach numbers in the upper atmosphere for the exact same physical speed, which correctly spikes the Mach-dependent drag coefficient curves right when they matter most.

---

### ISA Troposphere Lapse Rate:

$$T_{dynamic} = T_{base} - (0.0065 \times h)$$

**Simulation Role:** Feeds the Ideal Gas Law. This models the troposphere by dropping the ambient temperature by exactly 0.0065 Kelvin for every meter climbed. It perfectly mimics how real-world weather and altitude thin out the air density.

---

### Quaternion Derivatives:

$$\dot{q} = \frac{1}{2} q \otimes \omega$$

**Simulation Role:** Safely tracks the 3D orientation. Unlike standard Euler angles (pitch, yaw, roll) which suffer from "gimbal lock" mathematics if a rocket points perfectly straight up, quaternions smoothly track the rocket's rotation in a 4D space, allowing extreme maneuvers, weathercocking, and tumbling without breaking the ODE solver.

---

## ⚙️ Flight Dynamics Features

- **Rigid Body Kinematics:** The simulation continuously tracks the rocket's orientation using the quaternion state vector, actively normalizing it back to a length of `1.0` every time step. This prevents floating-point math errors from physically "warping" or distorting the rotational axes during extreme flight profiles.

- **Dynamic ISA Atmosphere:** The `Environment` class applies the ISA lapse rate alongside a customizable surface temperature offset. It calculates dropping temperatures and expands/contracts air density accordingly. It also applies a "washout factor" so that hot launch pad days linearly taper off by the time the rocket hits the tropopause (11,000m), creating a professional-grade meteorological model.

- **Time-Varying Properties:** The rocket's mass, Center of Gravity (CG), Thrust, and Moments of Inertia do not use average or static numbers. They seamlessly shift at millisecond intervals throughout the motor burn using `interp1d` interpolation arrays based on OpenRocket CSV exports.

- **Range Safety Lockout:** Includes an automated safety abort that triggers if the rocket exceeds a 25° angle of attack. This prevents the "Apogee Illusion" bug by strictly enforcing this lockout only during the critical launch rail clearance and initial ascent phase (under 100 meters), allowing natural horizontal weathercocking once the rocket coasts over apogee.

---

## 🛠️ Development & Commit Timeline

This project was developed iteratively, ensuring each mathematical layer was verified before introducing the next degree of complexity.

1. **Initial Physics:** Integration of changing mass over time and basic 1D/3D translations.
2. **Rigid Body Transition:** Shifted to a full 6DOF rigid body model using quaternions and dynamic inertia tensors.
3. **Aerodynamic Integration:** Implemented the Barrowman equations to calculate static margins, restoring torques, and crosswind weathercocking.
4. **Telemetry & Visuals:** Built a complete telemetry dashboard (Matplotlib) and launched a real-time 3D flight visualizer (PyVista) to replay flight data.
5. **Modular Architecture:** Refactored the codebase to fully separate data files from the engine (`config.py`), allowing instant swapping of rocket models. Resolved branch merges to maintain a clean, single-tree `main` workflow.

---

## 💻 How to Run the Simulator

### Prerequisites

You will need Python 3.x installed along with the required libraries:

```bash
pip install numpy scipy pandas matplotlib pyvista ambiance
```

### Running a Flight

1. **Simulate the Launch:** Run the main orchestrator script. This computes the flight kinematics and generates both a `telemetry.csv` file and a 2D matplotlib dashboard of the trajectory.

```bash
python main.py
```

2. **Visualize in 3D:** Once the telemetry is generated, launch the interactive visualizer. This replays the exact pitch, yaw, roll, and translation of the rocket in a 3D environment.

```bash
python "visualizer new.py"
```

---

## Simulating Your Own Rocket

Because this engine is entirely modular, you do not need to rewrite any physics code to test a new rocket.

1. **Export Data:** Pull your rocket's data from OpenRocket. You will need CSV files for Thrust, Drag vs. Mach, Mass over time, CG over time, and MOI over time.
2. **Export CAD:** Export your rocket as a 1:1 scale `.obj` file.
3. **Organize:** Create a dedicated folder for your rocket (e.g., `CASSIE/`) and place the CSVs and the `.obj` file inside.
4. **Update Config:** Open `config.py`. Update the file paths to point to your new folder, and input your specific fin geometries, nosecone length, and environmental conditions (crosswind, temp offsets, launch rail length).
5. Run `main.py` to fly!

---

## Future Scope

While the core physics engine is robust, future development branches will focus on expanding utility and user experience:

- **Direct XML Parsing:** Eliminating the need to export individual CSVs by writing a parser that directly reads native `.ork` (OpenRocket) XML files.

- **Advanced Recovery Physics:** Implementing parachute deployment triggers, separate drag calculations for drogue/main chutes, and high-altitude wind drift predictions for recovery operations.

- **Multi-Staging Capabilities:** Upgrading the physics engine and classes to handle instantaneous mass drops and secondary motor ignitions for two-stage vehicles.

- **Native Mass Properties:** Allowing the import of highly detailed CAD models (from software like Siemens NX or SolidWorks) to derive internal inertia tensors and CGs directly, rather than relying on OpenRocket approximations.

- **UI/UX Overhaul:** Wrapping the python scripts in a dedicated Graphical User Interface (GUI) to streamline the configuration process and real-time visualization controls.

# ==========================================
# 6DOF ROCKET SIMULATION CONFIGURATION FILE
# ==========================================

# --- DATA FILES FROM OPENROCKET ---
# Provide the file paths to your CSV data.
# Format for all files should be two columns: 'Time, Value' (or 'Mach, Value' for drag)
DRAG_FILE = "drag_data.csv"     
MOTOR_FILE = "motor_data.csv"   #Newtons
MASS_FILE = "mass_data.csv"   #grams
CG_FILE = "cg_data.csv"     # meters    
MOI_FILE = "moi_data.csv" #make sure to check "Time", "Longitudinal MOI", and "Rotational Inertia" in that order from OpenRocket" kgm^2
ROCKET_MODEL_FILE = "rocket_model.obj" # OBJ file of your rocket model for 3D visualization  (make sure scale is 1:1 when exporting)

# --- ROCKET GEOMETRY ---
# ALL UNITS MUST BE IN METERS (m)
DIAMETER = 0.08
NOSE_LENGTH = 0.178
NUM_FINS = 3
FIN_ROOT_CHORD = 0.127
FIN_TIP_CHORD = 0.064
FIN_SPAN = 0.093
FIN_SWEEP = 0.102
FIN_CANT_ANGLE_DEG = 0.01 # Very slight cant angle to add realism (degrees) or SET TO 0.0 FOR NO CANT
ROCKET_COLOR = "green" # Color for visualization (e.g., "red", "blue", "green") choose basic colors

# Distance from the very tip of the nosecone to the leading edge of the fin root
DIST_TO_FINS = 0.965

# --- ENVIRONMENT ---
LAUNCHPAD_ALTITUDE_M = 0     # Altitude of the launch pad above sea level (meters)
TEMP_OFFSET_C = 0            # Surface temperature offset from ISA standard (15°C)

LAUNCH_RAIL_LENGTH_M = 1     # Length of the launch rail in meters.

# Wind vector: [X-velocity, Y-velocity, Z-velocity] in meters per second
# Example: [5.0, 0.0, 0.0] means a 5 m/s wind blowing in the +X direction
WIND_VECTOR = [2, 2, 0.0]   

# --- SIMULATION PARAMETERS ---
TIME_LIMIT = 40.0               # Maximum allowed simulation time in seconds
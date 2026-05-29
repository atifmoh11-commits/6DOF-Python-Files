# ==========================================
# 6DOF ROCKET SIMULATION CONFIGURATION FILE
# ==========================================

# --- DATA FILES FROM OPENROCKET ---
# Provide the file paths to your CSV data.
# Format for all files should be two columns: 'Time, Value' (or 'Mach, Value' for drag)
DRAG_FILE = "CASSIE/drag_data_CASSIE.csv"     
MOTOR_FILE = "CASSIE/motor_data_CASSIE.csv"   #Newtons
MASS_FILE = "CASSIE/mass_data_CASSIE.csv"   #grams
CG_FILE = "CASSIE/cg_data_CASSIE.csv"     # meters    
MOI_FILE = "CASSIE/moi_data_CASSIE.csv" #make sure to check "Time", "Longitudinal MOI", and "Rotational Inertia" in that order from OpenRocket" kgm^2
ROCKET_MODEL_FILE = "CASSIE/rocket_model_CASSIE.obj" # OBJ file of your rocket model for 3D visualization  (make sure scale is 1:1 when exporting)

# --- ROCKET GEOMETRY ---
# ALL UNITS MUST BE IN METERS (m)
DIAMETER = 0.081
NOSE_LENGTH = 0.41
NUM_FINS = 4
FIN_ROOT_CHORD = 0.203
FIN_TIP_CHORD = 0.076
FIN_SPAN = 0.083
FIN_SWEEP = 0.178
FIN_CANT_ANGLE_DEG = 0.0  # Very slight cant angle to add realism (degrees) or SET TO 0.0 FOR NO CANT

# Distance from the very tip of the nosecone to the leading edge of the fin root
DIST_TO_FINS = 1.9

# --- ENVIRONMENT ---
LAUNCHPAD_ALTITUDE_M = 213.36      # Altitude of the launch pad above sea level (meters)
TEMP_OFFSET_C = 12.22            # Surface temperature offset from ISA standard (15°C)

LAUNCH_RAIL_LENGTH_M = 3.05     # Length of the launch rail in meters.

# Wind vector: [X-velocity, Y-velocity, Z-velocity] in meters per second
# Example: [5.0, 0.0, 0.0] means a 5 m/s wind blowing in the +X direction
WIND_VECTOR = [-1.37, 3.30, 0.0]   

# --- SIMULATION PARAMETERS ---
TIME_LIMIT = 40.0               # Maximum allowed simulation time in seconds
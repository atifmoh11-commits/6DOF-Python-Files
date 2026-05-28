# ==========================================
# 6DOF ROCKET SIMULATION CONFIGURATION FILE
# ==========================================

# --- DATA FILES FROM OPENROCKET ---
# Provide the file paths to your CSV data.
# Format for all files should be two columns: 'Time, Value' (or 'Mach, Value' for drag)
DRAG_FILE = "drag_data.csv"     
MOTOR_FILE = "motor_data.csv"   
MASS_FILE = "mass_data.csv"     
CG_FILE = "cg_data.csv"         
MOI_FILE = "moi_data.csv" #make sure to check "Time", "Longitudinal MOI", and "Rotational Inertia" in that order from OpenRocket"       

# --- ROCKET GEOMETRY ---
# ALL UNITS MUST BE IN METERS (m)
DIAMETER = 0.080
NOSE_LENGTH = 0.178
NUM_FINS = 3
FIN_ROOT_CHORD = 0.127
FIN_TIP_CHORD = 0.0635
FIN_SPAN = 0.0927
FIN_SWEEP = 0.1016

# Distance from the very tip of the nosecone to the leading edge of the fin root
DIST_TO_FINS = 0.965  

# --- ENVIRONMENT ---
LAUNCHPAD_ALTITUDE_M = 0.0      # Altitude of the launch pad above sea level (meters)
TEMP_OFFSET_C = 0.0             # Surface temperature offset from ISA standard (15°C)

# Wind vector: [X-velocity, Y-velocity, Z-velocity] in meters per second
# Example: [5.0, 0.0, 0.0] means a 5 m/s wind blowing in the +X direction
WIND_VECTOR = [5.0, 0.0, 0.0]   

# --- SIMULATION PARAMETERS ---
TIME_LIMIT = 60.0               # Maximum allowed simulation time in seconds
import numpy as np

from toom_utils import * # Import utility functions specific to Toom's rule and error handling

def SHEARING(param, option, view={"record_var" : "Logical"}):

############################### Initialisation ################################
    
    rng = np.random.default_rng() # Random number generator for reproducibility

    # Parameters for time steps and grid dimensions
    T = param["T"]
    L, h = param["K"], 2

    # Error rates for data and measurement
    error_rate = param["error_rate"]
    meas_error_rate = param["error_rate"] if option["id_error_rate"] else param["meas_error_rate"]

    # Booleans for activation of different error types
    errors_bool = option["error_bool"]
    meas_error_bool = option["meas_error_bool"]

    # Boolean initial data configuration
    init_var = param["init_var"]

    # Record variable controls output format (logical or data array)
    record_var = view["record_var"]
    if record_var == "Trajectory":
        dt = view["dt"]
        t_array = np.array([t for t in range(0,T,dt)]).astype(np.int32)
        configuration_list = []

    # Initialize data array based on selected configuration
    if init_var == "Zeros":
        data_array = np.zeros((h,L)).astype(np.int8)
    elif init_var == "Random":
        data_array = error_channel(h,L,0.5,rng).astype(np.int8)
    elif init_var == "Random Error":
        data_array = error_channel(h,L,error_rate,rng).astype(np.int8)
    elif init_var == "Specified":
        init_data_array = param["init_data_array"]
        data_array = init_data_array.astype(np.int8)

    # Main simulation loop
    for t in range(T):

################################# Errors ######################################

        if errors_bool: # Introduce random errors if enabled
            new_errors_array = error_channel(h,L,error_rate,rng)
            data_array = (data_array + new_errors_array)%2

################################# Parities ####################################

        if t%2 == 0:
            # Compute syndromes (error detection patterns)
            syndrome_hor,syndrome_vert = get_syndrome(data_array,meas_error_bool,meas_error_rate,rng)

################################ Correction ###################################

            # Switch correction direction periodically based on log-scaled time steps
            new_correction_array = get_correction_periodic(syndrome_hor,syndrome_vert)
            # Apply correction to data array
            data_array = (data_array + new_correction_array)%2
            
        
        if t%2 == 1:
            # SWAP qubits long diagonals
            data_array = SWAP(data_array)

################################# Output ######################################
            
        if record_var == "Trajectory":
            if t in t_array:
                configuration_list.append(data_array)

    # Return either logical outcome (majority vote) or final data array
    if record_var == "Logical":
        return(int(np.sum(data_array)>(L*h/2)))
    elif record_var == "Data":
        return(data_array)
    elif record_var == "Trajectory":
        return(np.stack(configuration_list))
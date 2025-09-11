import numpy as np

from toom_utils import * # Import utility functions specific to Toom's rule and error handling

def TOOM(param, option, view={"record_var" : "Logical"}):

############################### Initialisation ################################

    rng = np.random.default_rng() # Random number generator for reproducibility

    # Parameters for time steps and grid dimensions
    T = param["T"]
    L, h = param["K"], param["K"]

    # Error rates for data and measurement
    error_rate = param["error_rate"]
    meas_error_rate = param["error_rate"] if option["id_error_rate"] else param["meas_error_rate"]

    # Booleans for activation of different error types
    errors_bool = option["error_bool"]
    meas_error_bool = option["meas_error_bool"]
    shuffling = option["shuffling"]
    intensity = option["intensity"]
    periodic_bool = option["periodic_bool"]

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
        data_array = np.zeros((L,L)).astype(np.int8)
    elif init_var == "Random":
        data_array = error_channel(L,L,0.5,rng).astype(np.int8)
    elif init_var == "Random Error":
        data_array = error_channel(L,L,error_rate,rng).astype(np.int8)
    elif init_var == "Specified":
        init_data_array = param["init_data_array"]
        data_array = init_data_array.astype(np.int8)

    # List of four Toom's directions for cyclic switching
    Tooms_direction_list = [(1,1),(1,-1),(-1,1),(-1,-1)]
    direction = Tooms_direction_list[0]
    S = 0

    # Main simulation loop
    for t in range(T):

################################# Errors ######################################

        if errors_bool: # Introduce random errors if enabled
            new_errors_array = error_channel(L,h,error_rate,rng)
            data_array = (data_array + new_errors_array)%2

################################  Parities #####################################

        # Compute syndromes (error detection patterns)
        syndrome_hor,syndrome_vert = get_syndrome(data_array,meas_error_bool,meas_error_rate,rng)

################################ Correction ###################################
        
        if periodic_bool == True:
            new_correction_array = get_correction_periodic(syndrome_hor,syndrome_vert)
            data_array = (data_array + new_correction_array)%2

        if periodic_bool == False:
            if shuffling == "None":
                # Switch correction direction periodically based on log-scaled time steps
                direction = Tooms_direction_list[(t//np.ceil(np.log(L)).astype(int))%4]
                new_correction_array = get_correction_non_periodic(syndrome_hor,syndrome_vert,direction)
                # Apply correction to data array
                data_array = (data_array + new_correction_array)%2

            elif shuffling in ["SN","SNA","SND","Global"]:

                if t%2 == 0:
                    direction = Tooms_direction_list[(t//np.ceil(np.log(L)).astype(int))%4]
                    new_correction_array = get_correction_non_periodic(syndrome_hor,syndrome_vert,direction)

                    data_array = (data_array + new_correction_array)%2

                elif t%2 == 1:
                    if shuffling == "SN":
                        for i in range(intensity):
                            data_array = SN(data_array,"None",S%4)
                            S += 1
                    elif shuffling == "SNA":
                        for i in range(intensity):
                            data_array = SNA(data_array,"None",S%4)
                            S += 1
                    elif shuffling == "SND":
                        for i in range(intensity):
                            data_array = SND(data_array,"None",S%8)
                            S += 1
                    elif shuffling == "Global":
                        for i in range(intensity):
                            data_array = Global(data_array,rng)
                            S += 1

################################# Output ######################################
        
        if record_var == "Trajectory":
            if t in t_array:
                configuration_list.append(data_array)

    # Return either logical outcome (majority vote) or final data array
    if record_var == "Logical":
        logical = int(np.sum(data_array)>(L*h/2))
        return(logical)
    elif record_var == "Data":
        return(data_array)
    elif record_var == "Trajectory":
        return(np.stack(configuration_list))
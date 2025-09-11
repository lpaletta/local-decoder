import numpy as np

from sgn_utils import * # Import utilities for signal propagation and error correction
from analysis import * # Import tools for data analysis

def SIGNAL(param, option, view={"record_var" : "Logical"}):

############################### Initialisation ################################

    rng = np.random.default_rng() # Random number generator for reproducibility

    # Parameters for time steps and grid dimensions
    T = param["T"]
    L = param["K"]

    # Error rates for data and measurement
    error_rate = param["error_rate"]
    meas_error_rate = param["error_rate"] if option["id_error_rate"] else param["meas_error_rate"]

    # Signal velocity parameters
    anti_signal_velocity = param["anti_signal_velocity"]
    backward_signal_velocity = param["backward_signal_velocity"]
    # Initial configuration and options
    init_var = param["init_var"]
    errors_bool = option["error_bool"]
    meas_error_bool = option["meas_error_bool"]
    bidirectional_bool = option["bidirectional_bool"]

    record_var = view["record_var"]

    # Output-specific initializations
    if record_var == "Poisson":
        dt = view["dt"]
        t_array = np.array([t for t in range(0,T,dt)]).astype(np.int32)
        logical_array = np.zeros(len(t_array)).astype(np.int32)
    if record_var == "Stack":
        M = view["M"]
        stack_distribution_array = np.zeros(M).astype(np.int32)
    if record_var == "Trajectory":
        dt = view["dt"]
        t_array = np.array([t for t in range(0,T,dt)]).astype(np.int32)
        configuration_list = []
    if record_var == "View":
        global_hist_array = np.zeros((6,1,L)).astype(np.int8)

    # Initialize data array based on initial condition
    if init_var == "Zeros":
        data_array = np.zeros((1,L)).astype(np.int8)
    elif init_var == "Random":
        data_array = error_channel(1,L,0.5,rng).astype(np.int8)
    elif init_var == "Random Error":
        data_array = error_channel(1,L,error_rate,rng).astype(np.int8)
    elif init_var == "Specified":
        init_data_array = param["init_data_array"]
        data_array = init_data_array

    # Initialize arrays for ASR or SSR
    if bidirectional_bool == True:
        defect_array = np.zeros((2,L)).astype(np.int8)
        forward_signal_array = np.zeros((2,L)).astype(np.int8)
        backward_signal_array = np.zeros((2,L)).astype(np.int8)
        anti_signal_array = np.zeros((2,L)).astype(np.int8)
        stack_array = np.zeros((2,L)).astype(np.int32)
    elif bidirectional_bool == False:
        defect_array = np.zeros((1,L)).astype(np.int8)
        forward_signal_array = np.zeros((1,L)).astype(np.int8)
        backward_signal_array = np.zeros((1,L)).astype(np.int8)
        anti_signal_array = np.zeros((1,L)).astype(np.int8)
        stack_array = np.zeros((1,L)).astype(np.int32)

    # Main simulation loop
    for t in range(T):

################################### Errors ####################################

        if errors_bool: # Introduce random errors if enabled
            new_errors_array = error_channel(1,L,error_rate,rng)
            data_array = (data_array + new_errors_array)%2

############################### Measure Parities ###############################

        defect_array = get_defect(bidirectional_bool,data_array,meas_error_bool,meas_error_rate,rng)

################################## Update rules ################################
        
        # Track system history if trajectory recording is enabled
        if record_var == "View":
            global_hist_array = update_global_hist(data_array,defect_array,forward_signal_array,backward_signal_array,anti_signal_array,stack_array,global_hist_array)

        # Instantaneous correction
        instantaneous_correction_array = get_instantaneous_correction(bidirectional_bool,defect_array)
        data_array, defect_array = (data_array + instantaneous_correction_array)%2, (defect_array + get_defect(bidirectional_bool,instantaneous_correction_array,False,0,rng))%2

        # defect deactivation
        desactivated_defect_array = get_desactivated_defect(bidirectional_bool,defect_array)

        # Forward signal propagation and stack updates
        forward_signal_array,stack_array = send_forward_signal((defect_array+desactivated_defect_array)%2,forward_signal_array,stack_array)
        forward_signal_array = propagate_signals(bidirectional_bool,forward_signal_array,1)
        if record_var == "Stack":
            max_stack = int(np.max(stack_array))
            stack_distribution_array[max_stack] += 1

        # Final correction step
        final_correction_array,forward_signal_array,backward_signal_array = correction(defect_array,forward_signal_array,backward_signal_array,bidirectional_bool)
        data_array, defect_array = (data_array+final_correction_array)%2, (defect_array + get_defect(bidirectional_bool,final_correction_array,False,0,rng))%2

        # Backward signal propagation and recombination
        for k in range(backward_signal_velocity):
            backward_signal_array = propagate_signals(bidirectional_bool,backward_signal_array,-1)
            backward_signal_array,anti_signal_array = recombine_signals(backward_signal_array,anti_signal_array)
            backward_signal_array,stack_array = recombine_stack(backward_signal_array,stack_array)

        # Anti-signal propagation and recombination
        anti_signal_array,stack_array = send_anti_signal(defect_array,anti_signal_array,stack_array)

        for k in range(anti_signal_velocity-1):
            anti_signal_array = propagate_signals(bidirectional_bool,anti_signal_array,1)
            forward_signal_array,anti_signal_array = recombine_signals(forward_signal_array,anti_signal_array)
            backward_signal_array,anti_signal_array = recombine_signals(backward_signal_array,anti_signal_array)

        anti_signal_array = propagate_signals(bidirectional_bool,anti_signal_array,1)
        backward_signal_array,anti_signal_array = recombine_signals(backward_signal_array,anti_signal_array)
        
################################# Output ######################################

        if record_var == "Poisson":
            if t in t_array:
                idx = np.where(t_array == t)[0]
                logical_array[idx] = int(np.sum(data_array)>(L*1/2))
        if record_var == "Trajectory":
            if t in t_array:
                configuration_list.append(data_array)

    # Return appropriate output based on record_var setting
    if record_var == "Logical":
        return(int(np.sum(data_array)>(L*1/2)))
    elif record_var == "Stack":
        return(stack_distribution_array)
    elif record_var == "Poisson":
        return(logical_array)
    elif record_var == "View":
        return(global_hist_array)
    elif record_var == "Trajectory":
        return(np.stack(configuration_list))
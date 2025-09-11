import numpy as np

from hr_utils import *

def HR(param, option, view={"record_var" : "Logical"}):

############################### Initialisation ################################

    rng = np.random.default_rng()

    T = param["T"]
    number_of_level = param["K"]
    colony_size = param["colony_size"]
    L = colony_size**number_of_level

    error_rate = param["error_rate"]
    sqrt_work_period = param["sqrt_work_period"]
    work_period = sqrt_work_period**2
    fC = param["fC"]
    fN = param["fN"]
    init_var = param["init_var"]

    errors_bool = option["errors_bool"]
    meas_error_bool = option["meas_error_bool"]

    record_var = view["record_var"]

    if init_var == "Zeros":
        data_array = np.zeros((1,L)).astype(np.int8)
    elif init_var == "Random":
        data_array = error_channel(1,L,0.5,rng).astype(np.int8)
    elif init_var == "Random Error":
        data_array = error_channel(1,L,error_rate,rng).astype(np.int8)
    elif init_var == "Specified":
        init_data_array = param["init_data_array"]
        data_array = init_data_array.astype(np.int8)

    correction_dict = {}

    for t in range(T):

################################### Errors ####################################

        if errors_bool:
            new_errors_array = error_channel(1,L,error_rate,rng)
            data_array = (data_array + new_errors_array)%2

############################### Measure Parities ###############################

        syndrome_lvl_0_array = get_syndrome_lvl_0(data_array,meas_error_bool,error_rate,rng)

################################## Update rules ################################
        
        if t==0:
            hist_syndrome_array = syndrome_lvl_0_array
        elif t<=work_period**(number_of_level-1)-1:
            hist_syndrome_array = np.concatenate((hist_syndrome_array,syndrome_lvl_0_array),axis=0)
        elif t>work_period**(number_of_level-1)-1:
            hist_syndrome_array = np.concatenate((hist_syndrome_array,syndrome_lvl_0_array),axis=0)
            hist_syndrome_array = np.delete(hist_syndrome_array,0,axis=0)

        correction_lvl_0_array = compute_correction_lvl_k(syndrome_lvl_0_array,0,colony_size,L)

        correction_dict = update_correction(correction_dict,correction_lvl_0_array,t,colony_size,0)
        
        for k in range(1,number_of_level,1):
            if (t+1)%(work_period**k)==0:
                syndrome_lvl_k_array = get_syndrome_lvl_k(hist_syndrome_array[-work_period**k:],k,sqrt_work_period,fC,fN)
                correction_lvl_k_array = compute_correction_lvl_k(syndrome_lvl_k_array,k,colony_size,L)

                correction_dict = update_correction(correction_dict,correction_lvl_k_array,t,colony_size,k)
        
        if t in correction_dict:
            if np.shape(correction_dict[t]) == (L,):
                correction_array = correction_dict[t]
            else:
                correction_array = np.sum(correction_dict[t],axis=0)

            del correction_dict[t]

        data_array = (data_array + correction_array)%2

################################# Output ######################################

    if record_var == "Logical":
        return(int(np.sum(data_array)>(L*1/2)))
    elif record_var == "Data":
        return(data_array)
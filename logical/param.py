import numpy as np

alg_list = ["Signal","Toom", "Shearing"]
error_rate_list = np.round(np.logspace(np.log10(0.001),np.log10(0.1),14,endpoint=False),4).tolist()
K_sgn_list = [5,7,9,11,13,15,17,20,25,30,35,40,50,60,70,80,90,100]
K_toom_list = [3,4,5,6,7,8,9,10]
K_shearing_list = [3,5,8,12,16,20,25,30,35,40,45,50]


param_dict = {
    "T" : 50,
    "K" : 3,
    "error_rate" : 0.2,
    "meas_error_rate" : 0.2,
    "init_var": "Zeros",
}

option_dict = {
    "error_bool": True,
    "meas_error_bool": True,
    "id_error_rate": True
}

view_dict = {
    "record_var" : "Logical",
    "dt": 10,
    "M": 50
}

param_sgn_dict = {
    "anti_signal_velocity": 3,
    "backward_signal_velocity": 3,
    "init_data_array": np.array(())
}

option_sgn_dict = {
    "bidirectional_bool": True
}

param_toom_dict = {
    "init_data_array": np.array(()),
    "periodic_bool":False
}

option_toom_dict = {
    "shuffling": "None",
    "intensity":1,
    "periodic_bool":False
}

param_shearing_dict = {
    "init_data_array": np.array(())
}

option_shearing_dict = {
}


mc_dict = {
    "alg_name": "Signal",
    "T_inner_job": 10000,
    "T_cum_max": 10**7,
    "positive_max": 100
}
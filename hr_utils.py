import numpy as np

def error_channel(h,L,error_rate,rng):
    new_errors_array = (rng.random((h,L)) < error_rate)
    return(new_errors_array.astype(np.int8))

#def error_channel(lattice_size,error_rate):
#    random_array = np.random.rand(lattice_size)
#    new_errors = (random_array < error_rate).astype(int)
#    new_errors_array = np.array(new_errors)
#    return(new_errors_array)
    
#def get_syndrome_lvl_0(data_array,lattice_size):
#    new_syndrome_array = np.zeros_like([[0]*lattice_size]).astype(int)
#    for i in range(lattice_size):
#        if data_array[i%lattice_size]!=data_array[(i+1)%lattice_size]:
#            new_syndrome_array[0,i]=1
#    return(new_syndrome_array)

def get_syndrome_lvl_0(data_array,meas_error_bool,error_rate,rng):
    h, L = data_array.shape
    syndrome_array = np.zeros((h,L)).astype(np.int8)
    if meas_error_bool:
        syndrome_array[0,:] = ((data_array != np.roll(data_array,-1))+error_channel(h,L,error_rate,rng))%2
    else:
        syndrome_array[0,:] = (data_array != np.roll(data_array,-1))
    return(syndrome_array.astype(np.int8))


def get_syndrome_lvl_k(hist_syndrome_array,level,sqrt_work_period,fC,fN):

    work_period = sqrt_work_period**2

    bins = np.arange(1,work_period**level,sqrt_work_period**level)

    window = hist_syndrome_array[-sqrt_work_period**level:,:]
    syndrome_temp_array = np.array([np.sum(window,axis=0)])
    

    for i in range(sqrt_work_period**level,work_period**level, sqrt_work_period**level):
        window = hist_syndrome_array[-(i)-sqrt_work_period**level:-(i),:]
        syndrome_temp_array = np.concatenate((syndrome_temp_array,np.array([np.sum(window,axis=0)])),axis=0)
    syndrome_temp_array = (syndrome_temp_array > fC*sqrt_work_period**level).astype(int)
    syndrome_temp_array = np.array([np.sum(syndrome_temp_array,axis=0)])
    new_syndrome_lvl_k_array = (syndrome_temp_array > fN*sqrt_work_period**level).astype(int)
    return(new_syndrome_lvl_k_array)
    
def compute_correction_lvl_k(syndrome_array,level,colony_size,lattice_size):
    
    actual_colony_size = colony_size**level
    sup_colony_size = colony_size**(level+1)
    correction_array = np.zeros_like([0]*lattice_size).astype(int)
    address_list = [-1+a for a in np.arange(start=0,stop=lattice_size,step=actual_colony_size)]

    for i in range(len(address_list)):
        actual_syndrome = [syndrome_array[0,address_list[(i-1)%len(address_list)]],syndrome_array[0,address_list[i]],syndrome_array[0,address_list[(i+1)%len(address_list)]]]
        cond_beg = (address_list[i]+(sup_colony_size//2)*actual_colony_size+1)%sup_colony_size==0
        cond_inf = (address_list[i]+1+sup_colony_size//2)%sup_colony_size<sup_colony_size//2
        cond_center = (address_list[i]+1)%sup_colony_size==0
        cond_sup = (address_list[i]+1+sup_colony_size//2)%sup_colony_size>sup_colony_size//2
              
        if cond_beg:
            if actual_syndrome[1]==0:
                pass
            elif actual_syndrome[0]==1:
                correction_indices = np.arange(address_list[i]-actual_colony_size+1, address_list[i]+1)
                correction_indices %= lattice_size  # Ensure indices wrap around if they exceed lattice_size
                correction_array[correction_indices] = 1
            elif actual_syndrome[2]==1:
                correction_indices = np.arange(address_list[i]+1,address_list[i]+actual_colony_size+1)
                correction_indices %= lattice_size  # Ensure indices wrap around if they exceed lattice_size
                correction_array[correction_indices] = 1
            
            else:
                correction_indices = np.arange(address_list[i]+1,address_list[i]+actual_colony_size+1)
                correction_indices %= lattice_size  # Ensure indices wrap around if they exceed lattice_size
                correction_array[correction_indices] = 1

        elif cond_inf:
            if actual_syndrome[1]==0:
                pass
            elif actual_syndrome[2]==1:
                correction_indices = np.arange(address_list[i]+1,address_list[i]+actual_colony_size+1)
                correction_indices %= lattice_size  # Ensure indices wrap around if they exceed lattice_size
                correction_array[correction_indices] = 1
            elif actual_syndrome[0]==1:
                pass
            else:
                correction_indices = np.arange(address_list[i]+1,address_list[i]+actual_colony_size+1)
                correction_indices %= lattice_size
                correction_array[correction_indices] = 1

        elif cond_center:
            pass

        elif cond_sup:
            if actual_syndrome[1]==0:
                pass
            elif actual_syndrome[0]==1:
                correction_indices = np.arange(address_list[i]-actual_colony_size+1,address_list[i]+1)
                correction_indices %= lattice_size  # Ensure indices wrap around if they exceed lattice_size
                correction_array[correction_indices] = 1
            elif actual_syndrome[2]==1:
                pass
            else:
                correction_indices = np.arange(address_list[i]-actual_colony_size+1,address_list[i]+1)
                correction_indices %= lattice_size  # Ensure indices wrap around if they exceed lattice_size
                correction_array[correction_indices] = 1

    return(correction_array)
    
def update_correction(correction_dict,correction,t,colony_size,level):
    if t-1+colony_size**level in correction_dict:
        correction_dict[t-1+colony_size**level] = np.append(np.array([correction_dict[t-1+colony_size**level]]),np.array([correction]),axis=0)
    else:
        correction_dict[t-1+colony_size**level] = correction
    return(correction_dict)
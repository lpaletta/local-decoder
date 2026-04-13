import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from import_data import *

# use custom style
# ---------------------------------------------------------------------
# Plot style
# ---------------------------------------------------------------------

plt.style.use("rgplot")

# ---------------------------------------------------------------------
# Figure / font constants
# ---------------------------------------------------------------------


LABEL_FONTSIZE = 7
TICK_FONTSIZE_SMALL = 5.5

AXWIDTH = 0.6
LINEWIDTH = 1.2
MARKER_SIZE = 2.5
SCATTER_SIZE = 10

magenta = "#CE93D8"
grey = "#D6D6D6"

def compute_sigma(stack_value, T, number_of_runs):
    if stack_value.all() == 0:
        return(0)
    else:
        r = stack_value / number_of_runs
        return 1.96 * np.sqrt(r * (1 - r)) / (T * np.sqrt(number_of_runs))
    

    #fig, ax = plt.subplots(1,1,figsize=(1.7,2.4))
    #ax.set_xlabel("number of qubits ($n$)",labelpad=0.5,fontsize=7.5)
    #ax.set_ylabel("effective distance ($\\gamma_n$)",labelpad=0.5,fontsize=7.5)
    #ax.tick_params(axis='both', which='major', labelsize=6)
    #ax.tick_params(axis='both', which='minor', labelsize=6)
    #ax.legend(loc="lower right",frameon=False,fontsize=7)

def plot_distribution(df,path_fig,name):

    fig, ax = plt.subplots(1,1,figsize=(4.6,2))

    ax.scatter([],[],color='black',marker='o',s=SCATTER_SIZE,label="$\\varepsilon = 10^{-2}$")
    ax.scatter([],[],edgecolors='black',marker='o',facecolors="white",s=SCATTER_SIZE,label="$\\varepsilon = 10^{-3}$")

    for error_rate in list(set(df["error_rate"].to_list())):
        df_e = df[df["error_rate"]==error_rate]

        
        
        plt.gca().set_prop_cycle(plt.rcParams['axes.prop_cycle'])
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        colors[5] = colors[4]
        colors[4] = magenta
        i = 0

        for n, group in df_e.groupby("n"):
            color = colors[i]

            M = int(group["M"].iloc[0])
            T = int(group["T"].iloc[0])
            number_of_runs = int(group["number_of_runs"].iloc[0])
            m_list = [str(m) for m in range(M)]

            X = np.array([int(m) for m in range(M)])
            Y = group[m_list].to_numpy()[0]
            number_of_entries = Y[0]
            Y = np.where(Y<10,0,Y)
            Y_norm = Y/(number_of_entries)
            S = compute_sigma(Y,T,number_of_runs)
            if error_rate == 0.01:
                ax.scatter(X,Y_norm,color=color,marker='o',s=SCATTER_SIZE,label="$n=%i$"%n,zorder=5)
            elif error_rate == 0.001:
                ax.scatter(X,Y_norm,edgecolors=color,marker='o',s=SCATTER_SIZE,facecolors='white',zorder=6)
            i += 1

    ax.set_xlabel("maximum stack ($m$)",fontsize=7.5,labelpad=0.5)
    ax.set_ylabel("survival function $(S_M(m))$",fontsize=7.5,labelpad=0.5)#,rotation=-90)

    ax.set_xlim(0,16)
    ax.set_ylim(10**(-8),10**(0))

    ax.set_yscale("log")
    #ax.yaxis.set_label_position("right")
    #ax.yaxis.tick_right()

    ax.tick_params(labelsize=TICK_FONTSIZE_SMALL, width=AXWIDTH)

    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)

   # Grid (as in original)
    ax.grid(which='major', color=grey, linestyle='-', linewidth=AXWIDTH/2, alpha=0.2)
    ax.grid(which='minor', color=grey, linestyle='-', linewidth=AXWIDTH/3, alpha=0.2)
    #ax.grid(False)

    for spine in ax.spines.values():
        spine.set_linewidth(AXWIDTH)

    ax.legend(loc="upper right",frameon=False,fontsize=8)

    plt.savefig(path_fig+"/"+name)
    plt.close()

def get_integral(df):

    M = int(df["M"].iloc[0])
    m_list = [str(m) for m in range(M)]

    df_numeric = df[m_list]
    df_without_num = df.drop(columns=m_list)
    
    df_cumsum = df_numeric.copy()
    for i in range(len(df_numeric.columns)):
        df_cumsum.iloc[:, i] = df_numeric.iloc[:, i:].sum(axis=1)
    df_result = pd.concat([df_without_num, df_cumsum], axis=1)
    return(df_result)
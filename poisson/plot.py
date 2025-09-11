import matplotlib.pyplot as plt
import numpy as np

import matplotlib.ticker as ticker
from matplotlib.colors import to_rgb

# use custom style
plt.style.use('rgplot')

grey = to_rgb("#D6D6D6")

def plot_poisson(df,path_fig):

    plt.gca().set_prop_cycle(plt.rcParams['axes.prop_cycle'])
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    i=0

    fig, ax = plt.subplots(1,1,figsize=(1.7,2.8))
    ax.scatter([],[],s=1,label=" ",color='w')

    for n, group_n in df.groupby("n"):

        if n == 9:
            T_list = np.sort(list(set(df["T"].to_list())))
            T_list_reduced = [T_list[i] for i in range(len(T_list)) if i%2==0]

            group_n = group_n[group_n["T"].isin(T_list_reduced)]
        if n == 15:
            T_list = np.sort(list(set(df["T"].to_list())))
            T_list_reduced = [T_list[i] for i in range(len(T_list)) if i%10==0]

            group_n = group_n[group_n["T"].isin(T_list_reduced)]
        elif n > 15:
            T_list = np.sort(list(set(df["T"].to_list())))
            T_list_reduced = [T_list[i] for i in range(len(T_list)) if i%20==0]

            group_n = group_n[group_n["T"].isin(T_list_reduced)]

        group_n = group_n[group_n["positive"]<(45*group_n["number_of_runs"]/100)]

        X = group_n["T"].to_numpy()
        Y = 1-2*group_n["ratio"].to_numpy()
        S = 2*group_n["sigma"].to_numpy()
        
        if n == 35:
            ax.errorbar(X,Y,yerr=S,fmt="o",color=grey,capsize=1,markersize=2,label="$n=%i$"%n)
        else:
            ax.errorbar(X,Y,yerr=S,fmt="o",color=colors[i],capsize=1,markersize=2,label="$n=%i$"%n)
            i+=1

    ax.set_xlim([1,10**6])
    plt.xticks([1,100000,500000,1000000], 
           ['1', '10⁵', '5×10⁵', '10⁶'])
    minor_ticks_x = [1*10**5,2*10**5,3*10**5,4*10**5,5*10**5,6*10**5,7*10**5,8*10**5,9*10**5]
    plt.gca().set_xticks(minor_ticks_x, minor=True)

    ax.set_yscale("log")
    ax.set_ylim([0.1,1])

    #ax.yaxis.set_label_position("right")
    #ax.yaxis.tick_right()

    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())

    ax.grid(False)

    ax.set_xlabel("simulation time ($\\tau$)",fontsize=7.5,labelpad=0.5)
    ax.set_ylabel("$1-2 \\times P(\\tau)$",fontsize=7.5,labelpad=0.5)#,rotation=-90)

    ax.legend(loc="lower right",frameon=False,handletextpad=0.1,labelspacing=0.25,borderpad=0.25,fontsize=7.5,ncol=2,columnspacing=0.5)
    
    plt.savefig(path_fig+"/analysis_poisson.pdf")
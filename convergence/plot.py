import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

# use custom style
plt.style.use('rgplot')

grey = to_rgb("#D6D6D6")
light_grey = to_rgb("#F1F1F1")

from scipy.interpolate import make_interp_spline, BSpline

    #fig, ax = plt.subplots(1,1,figsize=(1.7,2.4))
    #ax.set_xlabel("number of qubits ($n$)",labelpad=0.5,fontsize=7.5)
    #ax.set_ylabel("effective distance ($\\gamma_n$)",labelpad=0.5,fontsize=7.5)
    #ax.tick_params(axis='both', which='major', labelsize=6)
    #ax.tick_params(axis='both', which='minor', labelsize=6)
    #ax.legend(loc="lower right",frameon=False,fontsize=7)

def plot_f_T(df,fit_bool,path_fig):

    plt.gca().set_prop_cycle(plt.rcParams['axes.prop_cycle'])
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    df_plot = df.copy()
    df_plot = df_plot.dropna(subset="pL")

    for name_e, group_e in df_plot.groupby("error_rate"):
        fig, ax = plt.subplots(1,1,figsize=(2.4,1.5))

        i=0

        for n, group_n in group_e.groupby("n"):

            group_n_subset = group_n[group_n["T"].isin([2,3]+[t for t in range(1,200,3)])]
            X = group_n_subset["T"].to_numpy()
            Y = group_n_subset["pL"].to_numpy()
            S = group_n_subset["sigma"].to_numpy()

            if n == 35:
                ax.errorbar(X,Y,yerr=S,capsize=1,markersize=2,fmt='o',color=grey,label="$n=%i$"%n)
            else:
                ax.errorbar(X,Y,yerr=S,capsize=1,markersize=2,fmt='o',color=colors[i],label="$n=%i$"%n)
                i+=1

            if fit_bool:
                Y = group_n_subset["pL_fit"].to_numpy()
                ax.plot(X,Y,linestyle="dotted",color=colors[i])

        ax.set_xlim(0,200)

        ax.set_yscale("log")
        ax.set_ylim(10**(-10),10**(-4))

        ax.set_xlabel("simulation time ($\\tau$)",fontsize=7.5,labelpad=0.5)
        #ax.set_ylabel("normalized logical flip ($P(\\tau)/\\tau$)",fontsize=7.5,labelpad=0.5)
        ax.set_ylabel("$P(\\tau)/\\tau$",fontsize=7.5,labelpad=5,rotation=-90)

        ax.tick_params(axis='both', which='major', labelsize=6)
        ax.tick_params(axis='both', which='minor', labelsize=6)
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()

        ax.grid(False)

        if fit_bool:
            plt.savefig(path_fig+"/logical_f_T_e={}.pdf".format(name_e))
        else:
            plt.savefig(path_fig+"/logical_f_T_e={}_wo_fit.pdf".format(name_e))
        plt.close()

def plot_transient_f_n(df,path_fig):

    fig, ax = plt.subplots(1,1,figsize=(2.4,0.8))

    df_plot = df.copy()
    df_plot = df_plot[["n","T_steady","T_steady_fit"]]
    df_plot = df_plot.drop_duplicates()

    X = df_plot["n"].to_numpy()
    Y = df_plot["T_steady"].to_numpy()

    ax.scatter(X,Y,s=10,color="black",facecolors='black',marker='D')

    X_fit = df_plot[df_plot["n"]>=10]["n"].to_numpy()
    Y_fit = df_plot[df_plot["n"]>=10]["T_steady_fit"].to_numpy()

    ax.plot(X_fit,Y_fit,color="black",linestyle="dotted",zorder=-1)

    ax.set_xlim(0,50)
    ax.set_ylim(0,100)

    ax.set_xlabel("number of qubits ($n$)",fontsize=7.5,labelpad=0.5)
    ax.set_ylabel("cut-off time ($\\tau_n$)",fontsize=7.5,labelpad=11,rotation=-90)

    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)
    #ax.xaxis.set_label_position("top")
    #ax.xaxis.tick_top()
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    ax.grid(False)

    plt.savefig(path_fig+"/transient_f_n.pdf")
    plt.close()

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import to_rgb
import matplotlib.patches as patches

from matplotlib.ticker import NullFormatter

# ---------------------------------------------------------------------
# Plot style
# ---------------------------------------------------------------------

plt.style.use("rgplot")

# ---------------------------------------------------------------------
# Figure / font constants
# ---------------------------------------------------------------------

FIGSIZE_ERROR = (2.8, 2.1)
FIGSIZE_GAMMA = (1.85, 2.1)
FIGSIZE_ESTIMATION = (2.3, 2.1)

LABEL_FONTSIZE = 7
TICK_FONTSIZE_SMALL = 5.5

AXWIDTH = 0.6
LINEWIDTH = 1.2
MARKER_SIZE = 2.5
SCATTER_SIZE = 6

# ---------------------------------------------------------------------
# Physical / numerical cutoffs
# ---------------------------------------------------------------------

D_PLOT_CUTOFF = 6
D_FIT_CUTOFF = 15
PL_FIT_CUTOFF = 1e-9

# ---------------------------------------------------------------------
# Axis limits
# ---------------------------------------------------------------------

X_ERROR_LIM = (1e-3, 1e-1)
Y_ERROR_LIM = (1e-9, 1e-1)

X_GAMMA_LIM = (0, 110)
Y_GAMMA_LIM = (0, 20)

grey = to_rgb("#D6D6D6")
light_grey = to_rgb("#F1F1F1")
magenta = to_rgb("#CE93D8")

def plot_f_E(df,fit_bool,key,plim_fit,path_fig):

    fig, ax = plt.subplots(1,1,figsize=FIGSIZE_ERROR)

    alg_name = df["alg_name"].to_list()[0]
    df_plot = df.copy()
    df_plot = df_plot.reset_index()

    plt.gca().set_prop_cycle(plt.rcParams['axes.prop_cycle'])
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colors[5] = colors[4]
    colors[4] = magenta
    i=0

    for name, group in df_plot.groupby("n"):
        X = group["error_rate"].to_numpy()
        Y = group["pL"].to_numpy()
        S = group["sigma"].to_numpy()
        if alg_name == "Signal":
            if name <= 6:
                ax.errorbar(X,Y,yerr=S,fmt="o",color=grey,markersize=MARKER_SIZE,label="$n=%i$"%name)
                ax.plot(X,Y,color=grey,linewidth=1.2)
            elif name > 6:
                ax.errorbar(X,Y,yerr=S,fmt="o",color=colors[i],markersize=MARKER_SIZE,label="$n=%i$"%name)
                ax.plot(X,Y,color=colors[i],linewidth=1.2)
                i+=1
        elif alg_name == "Shearing":
            if name <= 6:
                ax.errorbar(X,Y,yerr=S,fmt="^",color=grey,markersize=MARKER_SIZE,label="$n=%i$"%name)
                ax.plot(X,Y,color=grey,linewidth=1.2)
            elif name > 6:
                ax.errorbar(X,Y,yerr=S,fmt="^",color=colors[i],markersize=MARKER_SIZE,label="$n=%i$"%name)
                ax.plot(X,Y,color=colors[i],linewidth=1.2)
                i+=1
        elif alg_name == "Toom":
            if name <= 6:
                ax.errorbar(X,Y,yerr=S,fmt="s",color=grey,markersize=2,label="$n=%i$"%name)
                ax.plot(X,Y,color=grey,linewidth=1.2)
            elif name > 6:
                ax.errorbar(X,Y,yerr=S,fmt="s",color=colors[i],markersize=2,label="$n=%i$"%name)
                ax.plot(X,Y,color=colors[i],linewidth=1.2)
                i+=1
        elif alg_name == "Harrington":
            if name == 9:
                ax.errorbar(X,Y,yerr=S,fmt="X",color=colors[0],markersize=MARKER_SIZE,label="$n=%i$"%name)
                ax.plot(X,Y,color=colors[0],linewidth=1.2)
            elif name == 27:
                ax.errorbar(X,Y,yerr=S,fmt="X",color=colors[2],markersize=MARKER_SIZE,label="$n=%i$"%name)
                ax.plot(X,Y,color=colors[2],linewidth=1.2)
            elif name == 81:
                ax.errorbar(X,Y,yerr=S,fmt="X",color=colors[4],markersize=MARKER_SIZE,label="$n=%i$"%name)
                ax.plot(X,Y,color=colors[4],linewidth=1.2)

    if fit_bool:
        i=0
        for name, group in df_plot.groupby("n"):
            group = group[group["error_rate"]<plim_fit]
            if alg_name == "Harrington":
                if name == 9:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=colors[0], linestyle=':',linewidth=1.2)
                elif name == 27:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=colors[2], linestyle=':',linewidth=1.2)
                elif name == 81:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=colors[4], linestyle=':',linewidth=1.2)
            else:
                if name <= 6:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=grey, linestyle=':',linewidth=1.2)
                elif name > 6:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=colors[i], linestyle=':',linewidth=1.2)
                    i+=1

    ax.set_xlabel("physical error ($\\varepsilon = \\varepsilon_d = \\varepsilon_m$)",fontsize=LABEL_FONTSIZE)
    ax.set_ylabel("logical error ($\\varepsilon_L$)",fontsize=LABEL_FONTSIZE)

    # ax.set_xlabel("data error ($\\varepsilon_d$)",fontsize=LABEL_FONTSIZE)
    # ax.set_ylabel("measurement error ($\\varepsilon_m$)",fontsize=LABEL_FONTSIZE)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(*X_ERROR_LIM)
    ax.set_ylim(*Y_ERROR_LIM)

    ax.xaxis.set_minor_formatter(NullFormatter())
    #ax.xaxis.tick_top()
    #ax.xaxis.set_label_position("top")

    ax.tick_params(labelsize=TICK_FONTSIZE_SMALL, width=AXWIDTH)

    # Grid (as in original)
    ax.grid(which='major', color=grey, linestyle='-', linewidth=AXWIDTH/2, alpha=0.2)
    ax.grid(which='minor', color=grey, linestyle='-', linewidth=AXWIDTH/3, alpha=0.2)
    #ax.grid(False)

    ax.legend(
        loc="upper left",
        frameon=False,
        fontsize=7,
    )

    for spine in ax.spines.values():
        spine.set_linewidth(AXWIDTH)

    if not fit_bool:
        plt.savefig(path_fig+"/logical_f_E_wo_fit.pdf")
    elif fit_bool:
        plt.savefig(path_fig+"/logical_f_E_{}.pdf".format(key))
    plt.close()

def plot_gamma_n(df,fit_bool,key,path_fig):

    fig, ax = plt.subplots(1,1,figsize=FIGSIZE_GAMMA)

    plt.gca().set_prop_cycle(plt.rcParams['axes.prop_cycle'])
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    blue = colors[0]
    yellow = colors[3]
    black = 'black'

    for name_alg, group_alg in df.groupby('alg_name'):
        if name_alg in ["Signal","Toom","Shearing"]:
            if name_alg=="Signal":

                n_reduced_list = list(set(group_alg["n"].to_list()))
                group_alg = group_alg[group_alg["n"].isin(n_reduced_list)]
                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                ax.scatter(X,Y,facecolors=blue, edgecolors=blue,marker='o',s=SCATTER_SIZE,zorder=40,label="SSR")
                ax.plot(X,Y,color=blue,linewidth=LINEWIDTH,zorder=40)
            elif name_alg=="Toom":

                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                ax.scatter(X,Y,facecolors=black, edgecolors=black,marker='s',s=2/3*SCATTER_SIZE,zorder=30,label="Toom")
                ax.plot(X,Y,color=black,linewidth=LINEWIDTH,zorder=30)
            elif name_alg=="Shearing":

                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                ax.scatter(X,Y,facecolors=yellow, edgecolors=yellow,marker='^',s=SCATTER_SIZE,zorder=35,label="Shear.")
                ax.plot(X,Y,color=yellow,linewidth=LINEWIDTH,zorder=35)
            elif name_alg=="Harrington":

                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                ax.scatter(X,Y,facecolors=yellow, edgecolors=yellow,marker='p',s=SCATTER_SIZE,zorder=45,label="Shear.")
                ax.plot(X,Y,color=yellow,linewidth=LINEWIDTH,zorder=45)

    X = np.linspace(0,100,50)
    Y = (X+1)/2
    ax.plot(X,Y,color="black",linestyle="dashdot",linewidth=LINEWIDTH,zorder=20,label=" $\\frac{n+1}{2}$")

    df  = df[df["n"]>15]

    if fit_bool:
        i=0
        for name_alg, group_alg in df.groupby("alg_name"):
            if name_alg in ["Signal","Toom","Shearing"]:
                alpha = group_alg["alpha"].iloc[0]
                beta = group_alg["beta"].iloc[0]
                label="$\\alpha=%.2f, \\beta=%.2f$"%(alpha,beta)
                ax.plot(group_alg["n"].to_numpy(), group_alg[key].to_numpy(), linestyle='dashed',label=label)
                ax.set_title("$\\varepsilon_L = An(\\varepsilon/\\varepsilon_{th})^{\\gamma_n}$")
            i+=1

    ax.set_xlabel("number of qubits ($n$)",fontsize=LABEL_FONTSIZE)
    ax.set_ylabel("effective distance ($\\gamma_n$)",fontsize=LABEL_FONTSIZE)
    
    ax.set_xlim(*X_GAMMA_LIM)
    ax.set_ylim(*Y_GAMMA_LIM)

    ax.tick_params(labelsize=TICK_FONTSIZE_SMALL, width=AXWIDTH)

    # Grid (as in original)
    ax.grid(which='major', color=grey, linestyle='-', linewidth=AXWIDTH/2, alpha=0.2)
    ax.grid(which='minor', color=grey, linestyle='-', linewidth=AXWIDTH/3, alpha=0.2)
    #ax.grid(False)

    for spine in ax.spines.values():
        spine.set_linewidth(AXWIDTH)

    try:
        handles, labels = plt.gca().get_legend_handles_labels()
        order=[1,0,2,3]
        ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc="lower right",frameon=False,fontsize=7.5)
    except:
        ax.legend(loc="lower right",frameon=False,fontsize=7.5)

    if not fit_bool:
        plt.savefig(path_fig+"/gamma_f_n_wo_fit.pdf")
    elif fit_bool:
        plt.savefig(path_fig+"/gamma_f_n.pdf")
    plt.close()

def plot_estimate_f_n(df,df_proof,path_fig):
    fig, ax = plt.subplots(1,1,figsize=FIGSIZE_ESTIMATION)

    plt.gca().set_prop_cycle(plt.rcParams['axes.prop_cycle'])
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    blue = colors[0]
    yellow = colors[3]
    grey = colors[4]
    black = 'black'

    rect = patches.Rectangle((10**(-9), 0), 1, 100, linewidth=0, edgecolor=None, facecolor=light_grey,zorder=-40)
    ax.add_patch(rect)

    df_plot = df.copy()
    df_plot = df_plot.reset_index()

    for name, group in df_plot.groupby("alg_name"):
        if name=="Signal":
            error_rate=0.001
            group_0001=group[group["error_rate"]==error_rate]
            X_proof = df_proof[df_proof["error_rate"]==error_rate]["pL"].to_numpy()
            Y_proof = df_proof[df_proof["error_rate"]==error_rate]["n"].to_numpy()
            S_proof = df_proof[df_proof["error_rate"]==error_rate]["sigma"].to_numpy()
            ax.scatter(X_proof,Y_proof,facecolors='white', edgecolors=blue,marker='o',s=3*SCATTER_SIZE,linewidths=1,zorder=-8)
            ax.errorbar(X_proof,Y_proof,xerr=S_proof,fmt="o",color=blue,markersize=1.5*MARKER_SIZE,zorder=-9)
            Y = group_0001["n"].to_numpy()
            X = group_0001["pL_fit"].to_numpy()
            Y_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["n"].to_numpy()
            X_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["pL_fit"].to_numpy()
            Y_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["n"].to_numpy()
            X_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["pL_fit"].to_numpy()
            ax.scatter(X_inf,Y_inf,facecolors='white', edgecolors=blue,marker='o',s=SCATTER_SIZE,linewidths=0.8,zorder=-9)
            ax.scatter(X_sup,Y_sup,facecolors=light_grey, edgecolors=blue,marker='o',s=SCATTER_SIZE,linewidths=0.8,zorder=-0)
            ax.plot(X,Y,color=blue,linewidth=LINEWIDTH,zorder=-10)
            error_rate=0.01
            group_001=group[group["error_rate"]==error_rate]
            X_proof = df_proof[df_proof["error_rate"]==error_rate]["pL"].to_numpy()
            Y_proof = df_proof[df_proof["error_rate"]==error_rate]["n"].to_numpy()
            S_proof = df_proof[df_proof["error_rate"]==error_rate]["sigma"].to_numpy()
            #ax.scatter(X_proof,Y_proof,facecolors='white', edgecolors=blue,marker='o',s=8*SCATTER_SIZE,linewidths=LINEWIDTH,zorder=-8)
            ax.errorbar(X_proof,Y_proof,xerr=S_proof,fmt="o",color=blue,markersize=1.5*MARKER_SIZE,zorder=-9)
            Y = group_001["n"].to_numpy()
            X = group_001["pL_fit"].to_numpy()
            ax.scatter(X,Y,facecolors=blue, edgecolors=blue,marker='o',s=SCATTER_SIZE,linewidths=1,zorder=-10)
            ax.plot(X,Y,color=blue,linewidth=LINEWIDTH,zorder=-10)
        elif name=="Toom":
            error_rate=0.001
            group_0001=group[group["error_rate"]==error_rate]
            Y = group_0001["n"].to_numpy()
            X = group_0001["pL_fit"].to_numpy()
            Y_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["n"].to_numpy()
            X_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["pL_fit"].to_numpy()
            Y_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["n"].to_numpy()
            X_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["pL_fit"].to_numpy()
            ax.scatter(X_inf,Y_inf,facecolors='white', edgecolors=black,marker='s',s=2/3*SCATTER_SIZE,linewidths=0.8,zorder=-19)
            ax.scatter(X_sup,Y_sup,facecolors=light_grey, edgecolors=black,marker='s',s=2/3*SCATTER_SIZE,linewidths=0.8,zorder=-19)
            ax.plot(X,Y,color=black,linewidth=LINEWIDTH,zorder=-20)
            error_rate=0.01
            group_001=group[group["error_rate"]==error_rate]
            Y = group_001["n"].to_numpy()
            X = group_001["pL_fit"].to_numpy()
            ax.plot(X,Y,color=black,linewidth=LINEWIDTH,zorder=-26)
            ax.scatter(X,Y,facecolors=black, edgecolors=black,marker='s',s=2/3*SCATTER_SIZE,linewidths=1,zorder=-19)
        elif name=="Shearing":
            error_rate=0.001
            group_0001=group[group["error_rate"]==error_rate]
            Y = group_0001["n"].to_numpy()
            X = group_0001["pL_fit"].to_numpy()
            Y_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["n"].to_numpy()
            X_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["pL_fit"].to_numpy()
            Y_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["n"].to_numpy()
            X_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["pL_fit"].to_numpy()
            ax.plot(X,Y,color=yellow,linewidth=1,zorder=-15)
            ax.scatter(X_inf,Y_inf,facecolors='white', edgecolors=yellow,marker='^',s=SCATTER_SIZE,linewidths=0.8,zorder=-14)
            ax.scatter(X_sup,Y_sup,facecolors=light_grey, edgecolors=yellow,marker='^',s=SCATTER_SIZE,linewidths=0.8,zorder=-14)
            error_rate=0.01
            group_001=group[group["error_rate"]==error_rate]
            Y = group_001["n"].to_numpy()
            X = group_001["pL_fit"].to_numpy()
            ax.plot(X,Y,color=yellow,linewidth=1,zorder=-15)
            ax.scatter(X,Y,facecolors=yellow, edgecolors=yellow,marker='^',s=SCATTER_SIZE,linewidths=1,zorder=-14)

    ax.scatter([],[],facecolor='black', edgecolors='black',marker='o',s=1.5*SCATTER_SIZE,linewidths=0.8,label="$\\varepsilon = 10^{-2}$")
    ax.scatter([],[],facecolor='white', edgecolors='black',marker='o',s=1.5*SCATTER_SIZE,linewidths=0.8,label="$\\varepsilon = 10^{-3}$")

    ax.set_xlabel("logical error ($\\varepsilon_L$)",fontsize=LABEL_FONTSIZE,labelpad=0.5)
    ax.set_ylabel("number of qubits ($n$)",fontsize=LABEL_FONTSIZE,labelpad=5,rotation=-90)

    ax.set_xscale("log")
    ax.set_xlim(10**(-14),10**(-6))
    ax.set_ylim(0,100)

    ax.tick_params(labelsize=TICK_FONTSIZE_SMALL, width=AXWIDTH)

    # Grid (as in original)
    ax.grid(which='major', color=grey, linestyle='-', linewidth=AXWIDTH/2, alpha=0.2)
    ax.grid(which='minor', color=grey, linestyle='-', linewidth=AXWIDTH/3, alpha=0.2)
    #ax.grid(False)

    ax.legend(loc="lower right", frameon=False, fontsize=7)

    for spine in ax.spines.values():
        spine.set_linewidth(AXWIDTH)

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    ax.legend(loc="upper right",fontsize=7.5,frameon=False)

    plt.savefig(path_fig+"/logical_estimate_f_n.pdf")
    
    plt.close()
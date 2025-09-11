import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import to_rgb
import matplotlib.patches as patches

# use custom style
plt.style.use('rgplot')

grey = to_rgb("#D6D6D6")
light_grey = to_rgb("#F1F1F1")
magenta = to_rgb("#CE93D8")

def plot_f_E(df,fit_bool,key,plim_fit,path_fig):

    fig, ax = plt.subplots(1,1,figsize=(2.7,2.4))

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
                ax.errorbar(X,Y,yerr=S,fmt="o",color=grey,capsize=2.5,markersize=5,label="$n=%i$"%name)
            elif name > 6:
                ax.errorbar(X,Y,yerr=S,fmt="o",color=colors[i],capsize=2.5,markersize=5,label="$n=%i$"%name)
                i+=1
        elif alg_name == "Shearing":
            if name <= 6:
                ax.errorbar(X,Y,yerr=S,fmt="^",color=grey,capsize=2.5,markersize=5,label="$n=%i$"%name)
            elif name > 6:
                ax.errorbar(X,Y,yerr=S,fmt="^",color=colors[i],capsize=2.5,markersize=5,label="$n=%i$"%name)
                i+=1
        elif alg_name == "Toom":
            if name <= 6:
                ax.errorbar(X,Y,yerr=S,fmt="s",color=grey,capsize=2.5,markersize=4,label="$n=%i$"%name)
            elif name > 6:
                ax.errorbar(X,Y,yerr=S,fmt="s",color=colors[i],capsize=2.5,markersize=4,label="$n=%i$"%name)
                i+=1
        elif alg_name == "Harrington":
            if name == 9:
                ax.errorbar(X,Y,yerr=S,fmt="X",color=colors[0],capsize=2.5,markersize=5,label="$n=%i$"%name)
            elif name == 27:
                ax.errorbar(X,Y,yerr=S,fmt="X",color=colors[2],capsize=2.5,markersize=5,label="$n=%i$"%name)
            elif name == 81:
                ax.errorbar(X,Y,yerr=S,fmt="X",color=colors[4],capsize=2.5,markersize=5,label="$n=%i$"%name)

    if fit_bool:
        i=0
        for name, group in df_plot.groupby("n"):
            group = group[group["error_rate"]<plim_fit]
            if alg_name == "Harrington":
                if name == 9:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=colors[0], linestyle='dotted')
                elif name == 27:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=colors[2], linestyle='dotted')
                elif name == 81:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=colors[4], linestyle='dotted')
            else:
                if name <= 6:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=grey, linestyle='dotted')
                elif name > 6:
                    ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=colors[i], linestyle='dotted')
                    i+=1

    ax.set_xlabel("physical error ($\\varepsilon = \\varepsilon_d = \\varepsilon_m$)",fontsize=7.5,labelpad=0.5)
    ax.set_ylabel("logical error ($\\varepsilon_L$)",fontsize=7.5,labelpad=0.5)

    ax.set_xscale("log")
    ax.set_xlim(10**(-3),0.072)

    ax.set_yscale("log")
    ax.set_ylim(10**(-9),10**(-1))

    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)

    ax.grid(False)

    ax.legend(loc="upper left",frameon=False,handletextpad=0.1,labelspacing=0.25,borderpad=0.25,fontsize=7.5)

    if not fit_bool:
        plt.savefig(path_fig+"/logical_f_E_wo_fit.pdf")
    elif fit_bool:
        plt.savefig(path_fig+"/logical_f_E_{}.pdf".format(key))
    plt.close()

def plot_gamma_n(df,fit_bool,key,path_fig):

    fig, ax = plt.subplots(1,1,figsize=(1.7,2.4))

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
                ax.scatter(X,Y,facecolors=blue, edgecolors=blue,marker='o',s=14,linewidths=1,zorder=-10,label="SSR")
                ax.plot(X,Y,color=blue,linewidth=1,zorder=-10)
            elif name_alg=="Toom":

                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                ax.scatter(X,Y,facecolors=black, edgecolors=black,marker='s',s=13,linewidths=1,zorder=-26,label="Toom")
                ax.plot(X,Y,color=black,linewidth=1,zorder=-26)
            elif name_alg=="Shearing":

                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                ax.scatter(X,Y,facecolors=yellow, edgecolors=yellow,marker='^',s=18,linewidths=1,zorder=-15,label="Shear.")
                ax.plot(X,Y,color=yellow,linewidth=1,zorder=-15)
            elif name_alg=="Harrington":

                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                ax.scatter(X,Y,facecolors=yellow, edgecolors=yellow,marker='p',s=18,linewidths=1,zorder=-15,label="Shear.")
                ax.plot(X,Y,color=yellow,linewidth=1,zorder=-15)

    X = np.linspace(0,100,50)
    Y = (X+1)/2
    ax.plot(X,Y,color="black",linestyle="dashdot",zorder=-40,label=" $\\frac{n+1}{2}$")

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

    ax.set_xlabel("number of qubits ($n$)",labelpad=0.5,fontsize=7.5)
    ax.set_xlim(0,100)

    ax.set_ylabel("effective distance ($\\gamma_n$)",labelpad=0.5,fontsize=7.5)
    ax.set_ylim(0,20)

    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)

    ax.grid(False)

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
    fig, ax = plt.subplots(1,1,figsize=(2.55,2.4))

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
            ax.scatter(X_proof,Y_proof,facecolors='white', edgecolors=blue,marker='o',s=50,linewidths=1,zorder=-8)
            ax.errorbar(X_proof,Y_proof,xerr=S_proof,fmt="o",color=blue,capsize=3,markersize=6,zorder=-9)
            Y = group_0001["n"].to_numpy()
            X = group_0001["pL_fit"].to_numpy()
            Y_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["n"].to_numpy()
            X_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["pL_fit"].to_numpy()
            Y_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["n"].to_numpy()
            X_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["pL_fit"].to_numpy()
            ax.scatter(X_inf,Y_inf,facecolors='white', edgecolors=blue,marker='o',s=16,linewidths=1,zorder=-9)
            ax.scatter(X_sup,Y_sup,facecolors=light_grey, edgecolors=blue,marker='o',s=16,linewidths=1,zorder=-0)
            ax.plot(X,Y,color=blue,linewidth=1,zorder=-10)
            error_rate=0.01
            group_001=group[group["error_rate"]==error_rate]
            X_proof = df_proof[df_proof["error_rate"]==error_rate]["pL"].to_numpy()
            Y_proof = df_proof[df_proof["error_rate"]==error_rate]["n"].to_numpy()
            S_proof = df_proof[df_proof["error_rate"]==error_rate]["sigma"].to_numpy()
            ax.errorbar(X_proof,Y_proof,xerr=S_proof,fmt="o",color=blue,capsize=3,markersize=6,zorder=-9)
            Y = group_001["n"].to_numpy()
            X = group_001["pL_fit"].to_numpy()
            ax.scatter(X,Y,facecolors=blue, edgecolors=blue,marker='o',s=16,linewidths=1,zorder=-10)
            ax.plot(X,Y,color=blue,linewidth=1,zorder=-10)
        elif name=="Toom":
            error_rate=0.001
            group_0001=group[group["error_rate"]==error_rate]
            Y = group_0001["n"].to_numpy()
            X = group_0001["pL_fit"].to_numpy()
            Y_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["n"].to_numpy()
            X_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["pL_fit"].to_numpy()
            Y_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["n"].to_numpy()
            X_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["pL_fit"].to_numpy()
            ax.scatter(X_inf,Y_inf,facecolors='white', edgecolors=black,marker='s',s=14,linewidths=1,zorder=-19)
            ax.scatter(X_sup,Y_sup,facecolors=light_grey, edgecolors=black,marker='s',s=14,linewidths=1,zorder=-19)
            ax.plot(X,Y,color=black,linewidth=1,zorder=-20)
            error_rate=0.01
            group_001=group[group["error_rate"]==error_rate]
            Y = group_001["n"].to_numpy()
            X = group_001["pL_fit"].to_numpy()
            ax.plot(X,Y,color=black,linewidth=1,zorder=-26)
            ax.scatter(X,Y,facecolors=black, edgecolors=black,marker='s',s=14,linewidths=1,zorder=-19)
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
            ax.scatter(X_inf,Y_inf,facecolors='white', edgecolors=yellow,marker='^',s=22,linewidths=1,zorder=-14)
            ax.scatter(X_sup,Y_sup,facecolors=light_grey, edgecolors=yellow,marker='^',s=22,linewidths=1,zorder=-14)
            error_rate=0.01
            group_001=group[group["error_rate"]==error_rate]
            Y = group_001["n"].to_numpy()
            X = group_001["pL_fit"].to_numpy()
            ax.plot(X,Y,color=yellow,linewidth=1,zorder=-15)
            ax.scatter(X,Y,facecolors=yellow, edgecolors=yellow,marker='^',s=22,linewidths=1,zorder=-14)

    ax.scatter([],[],color=light_grey,linewidth=1,label="$\\varepsilon = 10^{-2}$")
    ax.scatter([],[],color=light_grey,linewidth=1,label="$\\varepsilon = 10^{-3}$")

    ax.set_xlabel("logical error ($\\varepsilon_L$)",fontsize=7.5,labelpad=0.5)
    ax.set_ylabel("number of qubits ($n$)",fontsize=7.5,labelpad=5,rotation=-90)

    ax.set_xscale("log")
    ax.set_xlim(10**(-14),10**(-6))
    ax.set_ylim(0,100)

    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    ax.grid(False)

    ax.legend(loc="upper right",fontsize=7.5,frameon=False)

    plt.savefig(path_fig+"/logical_estimate_f_n.pdf")
    
    plt.close()
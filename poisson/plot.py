import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ---------------------------------------------------------------------
# Plot style
# ---------------------------------------------------------------------

plt.style.use("rgplot")

# ---------------------------------------------------------------------
# Figure / font constants
# ---------------------------------------------------------------------

FIGSIZE_POISSON = (3.2, 2.0)

LABEL_FONTSIZE = 7
TICK_FONTSIZE = 5.5

AXWIDTH = 0.8
LINEWIDTH = 1.2
MARKER_SIZE = 3.5

# ---------------------------------------------------------------------
# Axis limits
# ---------------------------------------------------------------------

X_POISSON_LIM = (0, 1e6)
Y_POISSON_LIM = (0.1, 1.0)

# ---------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

GREY = "#D6D6D6"
MAGENTA = "#CE93D8"
ORANGE = "#FBB03B"
APPLE = "#A8D5A2"
COPPER = "#8C564B"
PINK = "#FADADD"

BLUE, RED, GREEN, YELLOW = colors[:4]

DISTANCE_TO_COLOR = {
    5: GREY,
    9: BLUE,
    15: RED,
    25: GREEN,
    35: PINK,
    50: YELLOW,
    75: APPLE,
    100: MAGENTA
}

# ---------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------

def plot_poisson(df, path):
    fig, ax = plt.subplots(figsize=FIGSIZE_POISSON)
    ax.scatter([],[],s=1,label=" ",color='w')

    for distance, group in df.groupby("n"):
        T_list = np.sort(list(set(df["T"].to_list())))
        group = group[group["positive"] < 3 * group["number_of_runs"] / 4]
        if distance <= 9:
            T_list_reduced = [T_list[i] for i in range(len(T_list)) if i%2==0]
        elif distance == 15:
            T_list_reduced = [T_list[i] for i in range(len(T_list)) if i%5==0]
        else:
            T_list_reduced = [T_list[i] for i in range(len(T_list)) if i%10==0]

        group = group[group["T"].isin(T_list_reduced)]

        ax.errorbar(
            group["T"],
            (1 - 2*group["ratio"]),
            yerr= 2*group["sigma"],
            fmt="o",
            markersize=2,
            color=DISTANCE_TO_COLOR[distance],
            label=rf"$n={distance}$",
        )

    ax.set_xlabel(r"simulation time ($\tau$)", fontsize=LABEL_FONTSIZE, labelpad=1)
    ax.set_ylabel(r"$1 - 2 \cdot P_L(\tau)$", fontsize=LABEL_FONTSIZE, labelpad=-12)

    ax.set_yscale("log")
    ax.set_xlim(*X_POISSON_LIM)
    ax.set_ylim(*Y_POISSON_LIM)

    ax.tick_params(labelsize=TICK_FONTSIZE, width=AXWIDTH)
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())

    # Grid (as in original)
    ax.grid(which='major', color=GREY, linestyle='-', linewidth=AXWIDTH/2, alpha=0.2)
    ax.grid(which='minor', color=GREY, linestyle='-', linewidth=AXWIDTH/3, alpha=0.2)
    #ax.grid(False)

    ax.set_xlim([1,10**6])
    plt.xticks([1,100000,500000,1000000], 
           ['1', '10⁵', '5×10⁵', '10⁶'])
    minor_ticks_x = [1*10**5,2*10**5,3*10**5,4*10**5,5*10**5,6*10**5,7*10**5,8*10**5,9*10**5]
    plt.gca().set_xticks(minor_ticks_x, minor=True)

    ax.legend(
        loc="lower right",
        frameon=False,
        fontsize=LABEL_FONTSIZE,
        ncol=2,
        columnspacing=0.5,
    )

    for spine in ax.spines.values():
        spine.set_linewidth(AXWIDTH)

    fig.tight_layout()
    plt.savefig(f"{path}/poisson.pdf")
    plt.close()
import os
import sys

# ---------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from import_data import *
from plot import *


# ---------------------------------------------------------------------
# Global configuration
# ---------------------------------------------------------------------

DATA_PATH = "poisson/data/"
FIG_PATH = "poisson/fig/"

DATA_FILE = "data.csv"

# ---------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------

df = import_data(DATA_PATH, DATA_FILE, "Poisson")

# Distances used for plotting
D_PLOT_ALL = df["n"].unique()

# -------------------------------------------------------------
# Plot jump probability (selected distances)
# -------------------------------------------------------------

plot_poisson(df, path=FIG_PATH)



# import sys
# import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from import_data import *
# from plot import *

# path, data_name = "poisson/data/", "data.csv"
# path_fig = "poisson/fig/"

# df = import_data(path, data_name, "Poisson")

# plot_poisson(df,path_fig)
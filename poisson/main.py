import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from import_data import *
from plot import *

path, data_name = "poisson/data/", "data.csv"
path_fig = "poisson/fig/"

df = import_data(path, data_name, "Poisson")

plot_poisson(df,path_fig)
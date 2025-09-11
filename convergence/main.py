import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from import_data import *
from analysis import *
from plot import *

path, data_name = "convergence/data/", "data.csv"
path_fig = "convergence/fig/"

df = import_data(path, data_name, "Convergence")
df = get_end_transient(df)
A, B = fit_end_transient(df[df["n"]>=10])
df = add_fit_transient(df,A,B)

plot_f_T(df,False,path_fig)
plot_transient_f_n(df,path_fig)












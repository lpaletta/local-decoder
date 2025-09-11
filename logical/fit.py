import numpy as np

from scipy.optimize import curve_fit


def fit_pL_single_alg(df,pth_guess,plim_fit):

    df_fit = df.copy()
    df_fit = df_fit.dropna(subset="pL")

    df_fit = df_fit[df_fit["error_rate"]<plim_fit]

    n_list = np.sort(list(set(df_fit["n"].to_list())))
    dict_n_index = dict(zip(list(n_list),[int(i) for i in range(len(n_list))]))
    df_fit["i_n"] = df_fit["n"].apply(lambda x: map_in_to_n(x,dict_n_index))
    df["i_n"] = df["n"].apply(lambda x: map_in_to_n(x,dict_n_index))

    gamma_n_guess_list = [n/10 for n in n_list]
    gamma_n_bound_list = len(n_list)*[50]

    guess = np.array(gamma_n_guess_list+[0.1,pth_guess])
    upper_bound = np.array(gamma_n_bound_list+[100,2*pth_guess])

    fit = curve_fit(f=func_logical,xdata=(df_fit["n"].to_numpy(),df_fit["error_rate"].to_numpy(),df_fit["i_n"].to_numpy()),ydata=np.log(df_fit["pL"].to_numpy()),p0=guess,bounds=(0,list(upper_bound)))

    param_opt_value = fit[0]
    A, pth = param_opt_value[-1], param_opt_value[-2]

    df.loc[:,"A"] = A
    df.loc[:,"pth"] = pth
    print(pth)
    for i in range(len(n_list)):
        df.loc[df["i_n"]==i,"gamma_n"] = param_opt_value[i]

    df = df.drop(columns=["i_n"])

    return(df)

def fit_gamma_n_single_alg(df):

    df_fit = df.copy()
    df_fit = df_fit.dropna(subset="gamma_n")

    df_fit = df_fit[df_fit["n"]>15]

    fit = curve_fit(f=get_exp,xdata=df_fit["n"].to_numpy(),ydata=df_fit["gamma_n"].to_numpy(),p0=[1,1],bounds=(0,[2,1]))

    param_opt_value = fit[0]
    alpha, beta = param_opt_value[0], param_opt_value[1]

    df.loc[:,"alpha"] = alpha
    df.loc[:,"beta"] = beta

    return(df)


def add_pL_fit(df,key):
    df.loc[:,key] = np.exp(ansatz(df.loc[:,"A"],df.loc[:,"n"],df.loc[:,"error_rate"],df.loc[:,"pth"],df.loc[:,"gamma_n"]))
    return(df)

def add_gamma_n_fit(df,key):
    df.loc[:,key] = get_exp(df.loc[:,"n"],df.loc[:,"alpha"],df.loc[:,"beta"])
    return(df)

def func_logical(X,*param):
    n, p, i_n = X
    gamma_n_list = param[:-2]
    A, pth = param[-1], param[-2]
    gamma_n = [gamma_n_list[int(i)] for i in i_n]
    return(ansatz(A,n,p,pth,gamma_n))

def ansatz(A,n,p,pth,gamma_n):
    return(np.log((n*A)*(p/pth)**(gamma_n)))

def get_exp(X,alpha,beta):
    n = X
    gamma_n = alpha*n**beta
    return(gamma_n)

def map_in_to_n(n,dict_n_index):
    if n in dict_n_index:
        return(dict_n_index[n])
    else:
        return(float("NaN"))
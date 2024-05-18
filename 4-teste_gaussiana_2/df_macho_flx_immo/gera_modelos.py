import numpy as np
import pandas as pd

import pickle 

import scipy.stats as stats

from sklearn.mixture import GaussianMixture
# from sklearn.mixture import GMM
from sklearn import mixture


def gerera_models(df,name, qnt= 14):
    X = df[name]
    x_a = np.array(X)
    s = x_a.reshape(-1, 1)
    N = np.arange(1, qnt)
    models = [None for i in range(len(N))]
    for i in range(len(N)):
        ls_models = []
        for an in range(30):
            ls_models.append(GaussianMixture(N[i]).fit(s))
            BIC_n = [m.bic(s)   for m in ls_models]
            best_bic_n = np.argmin(BIC_n)
            
        models[i] = ls_models[best_bic_n]
        print(i)
    AIC = [m.aic(s)   for m in models]
    BIC = [m.bic(s)   for m in models]
    LL  = [m.score(s) for m in models] 
    best_aic = np.argmin(AIC)
    best_bic = np.argmin(BIC)
    b_model_gaussian = models[best_bic]
    return {'name':name,'df_colun': df[name], 'ls_models':models, 
            'AIC': AIC, 'BIC':BIC, 'LL': LL, 'qnt':qnt,
           'best_aic': best_aic, 'best_bic': best_bic, 'best_model':b_model_gaussian }

def gera_modelos_a(df):

    ls_models =[]
    # ls_df_colum = [df['Vd_m_sum_nor'], df['dif_max_min_nor'], df['Vd_m_median_nor']]
    ls_df_name = ['median','mean', "sum"]
    for name in ls_df_name:
        ls_models.append(gerera_models(df, name, 15))
        
    return ls_models

def test_s():
    df_90 = pd.read_csv("/home/ethowatcher/analise_dados/4-teste_gaussiana_2/df_macho_flx_immo/90_all.csv")
    ls_models_90 = gera_modelos_a(df_90)

    print(ls_models_90)

if __name__ == "__main__":
    test_s()
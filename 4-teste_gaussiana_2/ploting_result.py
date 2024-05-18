import numpy as np
from matplotlib import pyplot as plt


def plt_gaussianas(ax, mo_dic, numero_modelo, title):
#     numero_modelo = 8
#     mo_dic = ls_models[2]
    g = mo_dic['ls_models'][numero_modelo]
    bic_m = mo_dic['BIC'][numero_modelo]
    weights = g.weights_
    means = g.means_
    covars = g.covariances_
#     print(bic_m, weights, means, covars)
    
    x = mo_dic['df_colun']
    f = np.ravel(x).astype(np.float)
    f = f.reshape(-1,1)
#     plt.hist(f, bins=100, histtype='bar', density=True, ec='red', alpha=0.5)
    
    f_axis = f.copy().ravel()
    f_axis.sort()
    for i, valor in enumerate(g.weights_):
        ax.plot(f_axis,weights[i]*stats.norm.pdf(f_axis,means[i],np.sqrt(covars[i])).ravel(), label= f'{i}')
        ax.legend()
    # plt.plot(f_axis,weights[1]*stats.norm.pdf(f_axis,means[1],np.sqrt(covars[1])).ravel(), c='red')
    # plt.plot(f_axis,weights[2]*stats.norm.pdf(f_axis,means[2],np.sqrt(covars[2])).ravel(), c='red')
    ax.hist(f, bins=100, histtype='bar', density=True, alpha=0.2)
    ax.set_xlabel("Mediana de uma janela móvel de 100 quadros")
    ax.set_title(title)
    return ax
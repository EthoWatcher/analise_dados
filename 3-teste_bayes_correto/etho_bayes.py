import numpy as np 
import pandas as pd 
import arviz as az

# Aproximado quando tem muito dado
def calculo_tamanho_efeito(veiculo, tratado):
    m_veiculo = np.mean(veiculo)
    m_tratado = np.mean(tratado)
    var_veiculo = np.var(veiculo)
    var_tratado = np.var(tratado)
    # cohen tamanho do efeito, simplificado.
    diff_of_means =  m_tratado - m_veiculo
    effect_size = diff_of_means / np.sqrt((var_veiculo + var_tratado) / 2)
    return effect_size


def creat_struct_saida(data):
    saida = {}
    saida["data"] = data
    # saida["x_weights"] = np.ones_like(data) / len(data)
    tamanho_amostra = len(data)
    saida["x_weights"] = np.full(tamanho_amostra , 1/tamanho_amostra)
    saida["mean"] = np.mean(data)
    saida["std"] = np.std(data)
    
    saida["hdi"] = az.hdi(data, hdi_prob=.94)
    saida["prob"] =[0.00, 0.00]
    return saida


def data_saida(veiculo, tratado):
    saida = {}
    v_m = np.mean(veiculo)
    t_m = np.mean(tratado)
    
    saida["cohen_d"] = np.abs(calculo_tamanho_efeito(veiculo, tratado))

    saida["hdi"] = [v_m, t_m]
    saida["prob"] =[0.00, 0.00]
    return saida

def calc_p_menor_zero(data):
    saida = {}
    tamanho_amostra = len(data) 
    filt_dif = data < 0 


    menor_0 = len(data[filt_dif])
    p_ser_menor_0 = menor_0 /tamanho_amostra

    saida["p"] = p_ser_menor_0
    saida["hdi"] = [0, -0.2]
    saida["prob"] = [0.001, 0.001]
    return saida


def calc_p_maior(data):
    saida = {}
    tamanho_amostra = len(data) 
    filt_dif = data > 0 


    menor_0 = len(data[filt_dif])
    p_ser_menor_0 = menor_0 /tamanho_amostra

    saida["p"] = p_ser_menor_0
    saida["hdi"] = [0, 0.152]
    saida["prob"] = [0.06, 0.06]
    return saida
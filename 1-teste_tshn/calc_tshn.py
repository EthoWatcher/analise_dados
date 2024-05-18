import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def gera_novas_observacoes(todos_dados, qnt_dados):
    saida = np.random.choice(todos_dados, qnt_dados, replace=True)
    return saida

def get_dif_medias(controle, tratamento):
    return np.mean(tratamento) - np.mean(controle)

class Novo_experimento():
    def __init__(self, todos_dados):
        self.todos_dados = todos_dados
        self.qnt_dados = len(todos_dados)
        self.controle = gera_novas_observacoes(todos_dados, self.qnt_dados)
        self.controle_media = np.mean(self.controle)
        
        self.tratamento = gera_novas_observacoes(todos_dados, self.qnt_dados)
        self.tratamento_media = np.mean(self.tratamento)
        
    def get_diferenca_entre_medias(self):
        return get_dif_medias(self.controle, self.tratamento)


class test_hipotese:
    def __init__(self,controle, tratamento, qt_medicoes_boots=1000):
        self.controle = controle
        self.tratamento = tratamento
        self.qt_medicoes_boots = qt_medicoes_boots
        self.todos_dados = np.concatenate([controle, tratamento])
        
        
        self.media_dif_medida_original = self._get_dif_medias(tratamento, controle)
        self._calcula()
        self._calc_list_medi()
        self._calc_p()
    
    def get_p(self, alpha=2.5):
        # print(self.p)
        return self.p < alpha
    
    def _get_dif_medias(self, tratamento, controle):
        return np.mean(tratamento) - np.mean(controle)
        
    def _calcula(self):
        self.medicoes_boostrap = []
        for _ in range(self.qt_medicoes_boots):
            nova_medicao_exp = Novo_experimento(self.todos_dados)

            self.medicoes_boostrap.append(nova_medicao_exp)
            

    def _calc_list_medi(self):
        self.list_dif_meidas = []
        def map_dif_medias(nova_medicao_experimento: Novo_experimento):
            return nova_medicao_experimento.get_diferenca_entre_medias()

        self.list_dif_meidas = list(map(map_dif_medias, self.medicoes_boostrap ))

        
    def _calc_p(self):
        def filter_aray(media_dif_medida_original, media_boots):
            r_medicao_positiva = media_dif_medida_original >= 0
            
            if(r_medicao_positiva):
                r_medicao_mais_improvavel = media_boots >= media_dif_medida_original
                return r_medicao_mais_improvavel
            else:
                r_medicao_mais_improvavel = media_boots <= media_dif_medida_original
                return r_medicao_mais_improvavel
        
        def calc_p(media_dif_medida_original, list_dif_meidas):
            qnt_dados = len(list_dif_meidas)
            b =0
            for a in range(qnt_dados):
                r_valor_mais_infre = filter_aray(media_dif_medida_original, list_dif_meidas[a])
                if(r_valor_mais_infre):
                    b+=1
  
            return b/qnt_dados *100

        self.p = calc_p(self.media_dif_medida_original, self.list_dif_meidas)


class test_hipotese_scipy:
    def __init__(self,controle, tratamento, TSHN=stats.mannwhitneyu):
        self.controle = controle
        self.tratamento = tratamento
        self.TSHN =  TSHN
        
        self._calc_p()
    
    def _calc_p(self):
        s, self.p = self.TSHN(self.controle, self.tratamento )
        self.p = self.p *100

    def get_p(self, alpha=5): # alpha de 5%
        # print(self.p)
        r_reijeitou = self.p <= alpha
        return r_reijeitou
    
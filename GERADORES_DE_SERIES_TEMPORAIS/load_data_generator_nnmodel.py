import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd
from generator_nnmodel import generator_nnmodel
from random import gauss
"""
    Script para geração de séries de carga a partir de um histórico de dados a carga refere-se a carga total de um alimentador
    de de dist. Fonte dos dados: Light S.A (Artigo JCAE 2020 PLANCAP)
    Link análise estatística -> https://www.mathworks.com/help/econ/infer-residuals.html
"""
# Obtendo o caminho da série temporal a partir de um arquivo TXT
path_1 = Path(__file__).parent / 'BASE_DE_DADOS' / 'Dafeira_load.TXT'
path_2 = Path(__file__).parent / 'BASE_DE_DADOS' / 'Bandeira_load.TXT'

load15_Table_1 = pd.read_csv(path_1, delimiter = '\t') # header não há cabeçalho
load15_Table_2 = pd.read_csv(path_2, delimiter = '\t') # header não há cabeçalho

load15_tsdata_1 = load15_Table_1.values[:, 0] # Obtendo todos os valores da coluna 0 da série temporal
load15_tsdata_2 = load15_Table_2.values[:, 0] # Obtendo todos os valores da coluna 0 da série temporal

# Plotagem das séries carregadas
# x1 = np.arange(0, load15_tsdata_1.shape[0])
# x2 = np.arange(0, load15_tsdata_2.shape[0])
# plt.figure(figsize = (10, 4))
# plt.plot(x1, load15_tsdata_1,'r')
# plt.plot(x2, load15_tsdata_2,'b')
# plt.legend(['Dafeira', 'Bandeira'])
# plt.show()

while True:
    janela = input('Janelas de amostras: ')
    if janela == '':
        janela = 8760
        break
    try:
        janela = int(janela)
        if janela > 0:
            janela = janela
        else:
            print('Inserir um valor númerico válido')
    except ValueError:
        print('Inserir um valor númerico válido')

load15_tsdata = load15_tsdata_1[: janela]

# Obtendo o tamanho da primeira entrada da série já fatiada
M = load15_tsdata.shape[0]
print(load15_tsdata)
plt.figure(figsize = (10, 4))
plt.plot(np.arange(0, M), load15_tsdata)
plt.show()

# # Criando um array booleano com o mesmo tamanho da série, por padrão, inicializado como False
# idx = np.zeros_like(load15_tsdata, dtype = bool)

# # Fatiando a série com um intervalo de 4 em 4 (cada dado equivale a 15 minutos)
# for time in range(0, M, 4):
#     idx[time] = True

# # Vetor já fatiado pelo laço acima pois, onde idx for True o valor será incorporado no vetor abaixo
# hourly_load_tsdata = list(load15_tsdata[idx])

# # Importando a função generator_nnmodel onde, uma lista deve ser fornecida em seu argumento e está retornará o modelo, o lag, as saídas esperadas, e a saída obtidas pelo modelo de previsão MLPRegressor
# net, p, Y, Yhat = generator_nnmodel(hourly_load_tsdata)

# # Ajustando a dimensão do vetor unidimensional para um vetor bidimensional
# yhat = Yhat.reshape((len(Yhat), 1))
# # Ajustando a dimensão do vetor unidimensional para um vetor bidimensional
# hourly_load_tsdata = np.array(hourly_load_tsdata).reshape(-1 ,1)

# Npoints = 8760 # quantidade de horas no ano
# T = len(hourly_load_tsdata) # 1/4 da janela digitada
# pred_hourly_load_tsdata = np.zeros((Npoints, 1)) # Criando um vetor bidimensional com zeros
# pred_hourly_load_tsdata[: p] = hourly_load_tsdata[: p] # Adicionando o lag no vetor
# pred_hourly_load_tsdata[p + 1: T + 1] = yhat # Adicionando a saída prevista no vetor

# t = T
# # Adicionando o restante das previsões no vetor pred_hourly_tsdata
# while t < Npoints:
#     pred_hourly_load_tsdata[t] = net.predict(pred_hourly_load_tsdata[t - p: t].reshape(1, -1)) # Adicionando os restantes da previsão
#     t += 1 

# pred_hourly_load_tsdata = pred_hourly_load_tsdata[0: Npoints + 1]

# # Plotagem da série original e da sintética
# plt.figure(figsize = (12, 6))
# plt.subplot(1, 2, 1)
# plt.plot(hourly_load_tsdata)
# plt.xlabel('Epoch')
# plt.ylabel('Amplitude')
# plt.grid(True)
# plt.title('Original')
# plt.subplot(1, 2, 2)
# plt.plot(pred_hourly_load_tsdata, color = 'm')
# plt.xlabel('Epoch')
# plt.ylabel('Amplitude')
# plt.xlim(-50, len(hourly_load_tsdata) + 50)
# plt.ylim(max(100, min(hourly_load_tsdata)), max(hourly_load_tsdata) + 10)
# plt.yticks(np.arange(100, np.max(hourly_load_tsdata), 25))
# plt.title('Synthetic')
# plt.grid(True)
# plt.show()

# # Gerando cenários de cargas com Processo Gaussiano
# # Nscenarios = input(int('Insira a quantidade de cenários: ))
# Nscenarios = int(input("Insira a quantidade de cenário(s) desejado: ") or 11)
# pred_hourly_load_tsdata = pred_hourly_load_tsdata.flatten() # Transformando a previsão em vetor unidimensional
# load_houly_series = np.zeros((Nscenarios, Npoints)) # Criando uma matriz 11 x 8760
# load_houly_series[0, :] = pred_hourly_load_tsdata # atribuindo os valores de pred na primeira linha de load_hourly_series


# for s in range(1, Nscenarios):
#     delta = 0.05 * pred_hourly_load_tsdata * gauss(1, Npoints)
#     load_houly_series[s, :] = pred_hourly_load_tsdata + delta

# load_houly_series = np.sqrt(3) * 13.8e3 * load_houly_series

# # Salvando a série em DataFrame e em arquivo CSV
# load_houly_series_df = pd.DataFrame(load_houly_series)
# load_houly_series_df.to_csv('C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\load_hourly_series.csv',
#     sep = ';',
#     index = False,
#     header = None
#     )

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
# Obtendo os caminhos dos arquivos Dafeira e Bandeira
path_1 = Path(__file__).parent / 'BASE_DE_DADOS' / 'Dafeira_load.TXT'
path_2 = Path(__file__).parent / 'BASE_DE_DADOS' / 'Bandeira_load.TXT'
# Obtendo o caminho da série temporal a partir de um arquivo TXT
load15_Table_1 = pd.read_csv(path_1, delimiter = '\t') #delimiter(limitador tabular)
load15_Table_2 = pd.read_csv(path_2, delimiter = '\t') #delimiter(limitador tabular)
# Obtendo os valores da série
load15_tsdata_1 = load15_Table_1.values[:, 0] # Obtendo todos os valores da coluna 0 da série temporal
load15_tsdata_2 = load15_Table_2.values[:, 0] # Obtendo todos os valores da coluna 0 da série temporal
# Obtendo o tamanho da série
idx_1 = load15_tsdata_1.shape
idx_2 = load15_tsdata_2.shape

# Plotagem das séries originais carregadas
x1 = np.arange(0, load15_tsdata_1.shape[0])
x2 = np.arange(0, load15_tsdata_2.shape[0])
plt.figure(figsize = (10, 4))
plt.plot(x1, load15_tsdata_1,'r')
plt.plot(x2, load15_tsdata_2,'b')
plt.legend(['Dafeira', 'Bandeira'])
plt.show()

# # Obtendo o índice máximo que o vetor poderá ter sabendo que o tamanho do próximo vetor será 8760
idx_1 = np.random.randint(idx_1[0] -  8760)
idx_2 = np.random.randint(idx_2[0] -  8760)

# Obtendo uma janela a partir da entrada do usuário ou com um default de 8760
while True:
    janela = input('Insira o tamanho da janela de amostras ou tecle enter para 8760: ')
    if janela == '':
        janela = 8760
        break
    try:
        janela = int(janela)
        if janela > 0:
            janela = janela
            break
        else:
            print('Inserir um valor númerico válido')
    except ValueError:
        print('Inserir um valor númerico válido')

load15_tsdata_1 = load15_tsdata_1[idx_1: idx_1 + janela]
load15_tsdata_2 = load15_tsdata_2[idx_2: idx_2 + janela]

# Obtendo o tamanho da primeira entrada da série já fatiada
# M = load15_tsdata_1.shape[0]
# N = load15_tsdata_2.shape[0]
# plt.figure(figsize = (10, 4))
# plt.title('Series das cargas Dafeira e Bandeira')
# plt.plot(np.arange(0, M), load15_tsdata_1)
# plt.plot(np.arange(0, N), load15_tsdata_2)
# plt.xlabel('hora')
# plt.ylabel('Potência')
# plt.legend(['Dafeira', 'Bandeira'])
# plt.show()
    
# Criando um array booleano com o mesmo tamanho da série, por padrão, inicializado como False
idx_1 = np.zeros_like(load15_tsdata_1, dtype = bool)
idx_2 = np.zeros_like(load15_tsdata_1, dtype = bool)
M = load15_tsdata_1.shape[0]
N = load15_tsdata_2.shape[0]

# Fatiando a série com um intervalo de 4 em 4 (cada dado equivale a 15 minutos)
for time in range(0, M, 4):
    idx_1[time] = True
for time in range(0, N, 4):
    idx_2[time] = True

# Vetor já fatiado pelo laço acima pois, onde idx for True o valor será incorporado no vetor abaixo
hourly_load_tsdata_1 = load15_tsdata_1[idx_1]
hourly_load_tsdata_2 = load15_tsdata_2[idx_2]

# plotagem da série que será fornecida para o modelo MPLRegressor
# plt.figure(figsize = (10, 4))
# plt.title('Séries fatiadas de 15 em 15 minutos')
# plt.plot(np.arange(0, hourly_load_tsdata_1.shape[0]), hourly_load_tsdata_1)
# plt.plot(np.arange(0, hourly_load_tsdata_2.shape[0]), hourly_load_tsdata_2)
# plt.xlabel('epoch')
# plt.ylabel('amplitude')
# plt.legend(['Dafeira', 'Bandeira'])
# plt.show()

# Importando a função generator_nnmodel onde, uma lista deverá ser fornecida em seu argumento, e está retornará o modelo(net_n), o lag(p_n), as saídas esperadas(Y_n), e a saída obtidas pelo modelo de previsão MLPRegressor(Yhat_n)
net_1, p_1, Y_1, Yhat_1 = generator_nnmodel(hourly_load_tsdata_1)
net_2, p_2, Y_2, Yhat_2 = generator_nnmodel(hourly_load_tsdata_2)

Npoints = 8760 # quantidade de horas no ano
T = len(hourly_load_tsdata_1) # 1/4 da janela digitada
pred_hourly_load_tsdata_1 = np.zeros(Npoints) # Criando um vetor unidimensional com zeros. O shape do vetor é (8760, )
pred_hourly_load_tsdata_1[: p_1] = hourly_load_tsdata_1[: p_1] # Adicionando o lag no vetor
pred_hourly_load_tsdata_1[p_1: T] = Yhat_1 # Adicionando a saída prevista no vetor

t = T # Na configuração de default, t = 2190 e Npoints - t = 6570
while t < Npoints:
    # print(t-p_1,' ', t)
    p = np.array((pred_hourly_load_tsdata_1[t - p_1: t]))
    p = p.reshape(-1, p_1)
    # print(p)
    # break
    prev = net_1.predict(p)
    pred_hourly_load_tsdata_1[t] = prev[0]
    t += 1

# # Plotagem da série com lag e com as novas previsões
# plt.figure(figsize=(12, 5))
# plt.plot(np.arange(Npoints), pred_hourly_load_tsdata_1)
# plt.title('')
# plt.xlabel('hora')
# plt.ylabel('Carga')
# plt.show()

S = len(hourly_load_tsdata_2) # 1/4 da janela digitada
pred_hourly_load_tsdata_2 = np.zeros(Npoints) # Criando um vetor unidimensional
pred_hourly_load_tsdata_2[:p_2] = hourly_load_tsdata_2[:p_2] # Adicionando o lag ao vetor 
pred_hourly_load_tsdata_2[p_2: S] = Yhat_2 # Adiconando as previsões

s = S
while s < Npoints:
    p = np.array((pred_hourly_load_tsdata_2[s - p_2: s]))
    p = p.reshape(-1, p_2)
    prev = net_2.predict(p)
    pred_hourly_load_tsdata_2[s] = prev[0]
    s += 1

# # Plotagem da série com lag e com as novas previsões
# # plt.figure(figsize=(12, 5))
# # plt.plot(np.arange(Npoints), pred_hourly_load_tsdata_2)
# plt.title('')
# plt.xlabel('hora')
# plt.ylabel('Carga')
# # plt.show()

# pred_hourly_load_tsdata_1 = pred_hourly_load_tsdata_1[0: Npoints + 1]
# pred_hourly_load_tsdata_2 = pred_hourly_load_tsdata_2[0: Npoints + 1]

# Plotagem da série original e da sintética
plt.figure(figsize = (14, 6))
plt.subplot(2, 2, 1)
plt.plot(load15_tsdata_1)
plt.xlabel('Epoch')
plt.ylabel('Amplitude')
plt.grid(True)
plt.title('Original')
plt.subplot(2, 2, 2)
plt.plot(pred_hourly_load_tsdata_1, color = 'm')
plt.xlabel('Epoch')
plt.ylabel('Amplitude')
plt.title('Synthetic')
plt.grid(True)
plt.subplot(2, 2, 3)
plt.plot(load15_tsdata_2, color = 'r')
plt.xlabel('Epoch')
plt.ylabel('Amplitude')
plt.title('Original')
plt.grid(True)
plt.subplot(2, 2, 4)
plt.plot(pred_hourly_load_tsdata_2, color = 'k')
plt.xlabel('Epoch')
plt.ylabel('Amplitude')
plt.title('Synthetic')
plt.grid(True)
plt.subplots_adjust(hspace=0.5, wspace=0.5)
plt.show()

# Gerando cenários de cargas com Processo Gaussiano
while True:
    Nscenarios = input("Insira a quantidade de cenário(s) desejado ou tecle enter para 11: ")
    if Nscenarios == '':
        Nscenarios = 11
        break
    try:
        Nscenarios = int(Nscenarios)
        if Nscenarios > 0:
            Nscenarios = Nscenarios
            break
        else:
            print('Insira um valor inteiro positivo válido')
    except ValueError:
        print('Insira um valor inteiro positivo válido')

pred_hourly_load_tsdata_1 = pred_hourly_load_tsdata_1.flatten() # Transformando a previsão em vetor unidimensional
load_houly_series_1 = np.zeros((Nscenarios, Npoints)) # Criando uma matriz 11 x 8760
load_houly_series_1[0, :] = pred_hourly_load_tsdata_1 # atribuindo os valores de pred na primeira linha de load_hourly_series

pred_hourly_load_tsdata_2 = pred_hourly_load_tsdata_2.flatten() # Transformando a previsão em vetor unidimensional
load_houly_series_2 = np.zeros((Nscenarios, Npoints)) # Criando uma matriz 11 x 8760
load_houly_series_2[0, :] = pred_hourly_load_tsdata_2 # atribuindo os valores de pred na primeira linha de load_hourly_series

for s in range(Nscenarios):

    delta_1 = 0.05 * pred_hourly_load_tsdata_1 * np.random.randn(Npoints)
    load_houly_series_1[s, :] = pred_hourly_load_tsdata_1 + delta_1

    delta_2 = 0.05 * pred_hourly_load_tsdata_2 * np.random.randn(Npoints)
    load_houly_series_2[s, :] = pred_hourly_load_tsdata_2 + delta_1

load_houly_series_1 = np.sqrt(3) * 13.8e3 * load_houly_series_1
load_houly_series_2 = np.sqrt(3) * 13.8e3 * load_houly_series_2

# Salvando a série em DataFrame e em arquivo CSV
load_houly_series_df_1 = pd.DataFrame(load_houly_series_1)
load_houly_series_df_1.to_csv(Path(__file__).parent / 'SERIES_GERADAS' / 'load_hourly_series.csv', sep = ';', index = False, header = None)

load_houly_series_df_2 = pd.DataFrame(load_houly_series_2)
load_houly_series_df_2.to_csv(Path(__file__).parent / 'SERIES_GERADAS' / 'dload_hourly_series.csv', sep = ';', index = False, header = None)

# path_1_raf = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\load_hourly_sistem.csv"
# load_df_raf = pd.read_csv(path_1_raf, sep = ';', header = None)
# for i in range(11):
#     plt.figure(figsize=(12,4))
#     plt.plot(np.arange(24), load_houly_series[i,:24] )
#     plt.plot(np.arange(24), load_df_raf.iloc[i,:24] )
#     plt.show()
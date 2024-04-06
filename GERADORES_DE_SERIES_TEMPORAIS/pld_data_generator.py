import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
""" 
    SCRIPT PARA GERAÇÃO DE SÉRIES DE PLD(PREÇO DE LIQUIDAÇÃO DE DIFERENÇA) A PARTIR DE UM HISTÓRICO DE  DADOS.
    FONTE DOS DADOS: <>
"""

# Caminho das séries históricas
path = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\BASE_DE_DADOS\\Historico_do_Preco_Horario(SE)_-_17_de_abril_de_2018_a_5_de_abril_de_2022.xlsx"

# Importando a tabela PLD e convertendo em séries históricas
PLD_Table = pd.read_excel(path)

# Obtendo os dados das 24 linhas(horas) e das 1437 colunas e atribuindo na váriavel Daely_PLD
Daily_PLD = PLD_Table.iloc[0: 24, 2:] # Período de 24 horas
# Obtendo as dimensões da matriz M = 24 linhas e N = 1437 colunas
M, N = Daily_PLD.shape
# Transformando os dados obtidos acima em vetor coluna(série temporal)
PLD_daily_tsdata = Daily_PLD.values.reshape((M * N, 1)) 
# Obtendo o tamanho da série temporal por ano
len_pld_timeseries = len(PLD_daily_tsdata) # 345122
# Variável com a quantidades de horas em um ano 24h x 365 = 8760h
Npoints = 8760
# Obtendo a quantidade de cenários(anos) em um número inteiro
Nscenarios = len_pld_timeseries // Npoints
# Criando uma matriz preenchida com zeros com dimenões Ncenários x Npoints
PLD_hourly_series = np.zeros((Nscenarios, Npoints))

for s in range(Nscenarios):
    inicio = Npoints * s
    fim = Npoints * (s + 1)
    PLD_hourly_series [s, :] = PLD_daily_tsdata[inicio: fim].flatten()

path_5_raf = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\PLD_hourly_series.csv"
PLD_df_raf = pd.read_csv(path_5_raf, sep = ';', header = None)

# print(PLD_hourly_series.shape)
# y = PLD_df_raf[0]
# print(y)
PLD_df_raf = PLD_df_raf.to_numpy()

# y = PLD_df_raf[0,:]
# print(y)

x = np.arange(PLD_hourly_series.shape[1])
r =  PLD_hourly_series.shape[0]
for i in range(r):

    y_1 = PLD_hourly_series[i, :] 
    y_2 = PLD_df_raf[i, :]
    plt.figure(figsize = (12, 5))
    plt.title(f'Série {i + 1}')
    plt.plot(x, y_1, 'm')
    plt.plot(x, y_2, 'b')
    plt.legend(['jon', 'raf'])
    plt.xlabel('hora')
    plt.ylabel('Carga')
    plt.show()

# Salvar o DataFrame em um arquivo CSV, Excel ou outro formato
PLD_hourly_df = pd.DataFrame(PLD_hourly_series)
PLD_hourly_df.to_csv("C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\PLD_hourly_data.csv",
    sep = ';',
    index = False,
    header = None
    )
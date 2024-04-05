import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt



while True:
    Nt = input('Informe o instante de tempo: ')
    if Nt == '':
        Nt = 24
        break
    try:
        Nt = int(Nt)
        if Nt > 0:
            Nt = Nt
            break
        else:
            print('Informe um valor numérico interio e positivo')
    except ValueError: 
        print('Informe um valor numérico interio e positivo')

path = Path(__file__).parent / "SERIES_GERADAS"
print(path)

path_1 = path / "load_hourly_series.csv"
path_1_raf = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\load_hourly_sistem.csv"

path_2 = path / "dload_hourly_series.csv"
path_2_raf = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\dload_hourly_seires.csv"

path_3 = path / "PVsystem_hourly_series.csv"
path_3_raf = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\PVsistem_hourly_system.csv"

path_4 = path / "WTGsystem_hourly_series.csv"
path_4_raf = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\WTGsystem_hourly_series.csv"

path_5 = path / "PLD_hourly_data.csv"
path_5_raf = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\PLD_hourly_series.csv"

path_6 = path / "TDist_hourly_series.csv"
path_6_raf = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\TDist_hourly_series.csv"

x = np.arange(1, Nt+1)

load_df = pd.read_csv(path_1, sep = ';', header = None)
load_df_raf = pd.read_csv(path_1_raf, sep = ';', header = None)

print(load_df.shape)
print(load_df_raf.shape)

m, _ = load_df.shape

# # Série de cargas despachaveis
# for i in range(m):

#     # load_series = load_df.iloc[i, :Nt]
#     load_series_raf = load_df_raf.iloc[i, :Nt]
#     # print(load_series.shape)

#     plt.figure(figsize = (10, 4))
#     plt.title(f'Série de cargas despachaveis {i+1}')
#     # plt.plot(x, load_series, 'r')
#     plt.plot(x, load_series_raf, 'b')
#     plt.xlabel("hora")
#     plt.ylabel("Potência")
#     plt.legend(['Raf'])
#     plt.legend(['Jon'])
#     plt.show()
# 
# dload_df = pd.read_csv(path_2, sep = ';', header = None)
# dload_df_raf = pd.read_csv(path_2_raf, sep = ';', header = None)

# m, _ = dload_df.shape

# Série de cargas NÂO despachaveis
# for i in range(m):  

#     dload_serie = dload_df.iloc[i, :Nt]
#     dload_series_raf = dload_df_raf.iloc[i, :Nt]
#     # print(load_series.shape)

#     plt.figure(figsize = (10, 4))
#     plt.title(f'Série de cargas NÂO despachaveis {i+1}')
#     # plt.plot(x, dload_serie, 'k')
#     plt.plot(x, dload_series_raf, 'b')
#     plt.xlabel("hora")
#     plt.ylabel("Potência")
#     # plt.legend(['Raf'])
#     plt.legend(['Raf'])
#     plt.show()

# PV_df = pd.read_csv(path_3, sep = ';', header = None)
# PV_df_raf = pd.read_csv(path_3_raf, sep = ';', header = None)
# # print(PV_df_raf.shape) ## shape (11, 8760)
# # print(PV_df.shape) ## shape (1, 8760) ERRO GRAVE
# m, _ = PV_df_raf.shape

# # Série de cargas FV
# for i in  range(m):

#     # PVsystem_series = PV_df.iloc[i, :Nt]
#     PVsystem_series_raf = PV_df_raf.iloc[i, :Nt].values / 1e3

#     plt.figure(figsize = (10, 4))
#     plt.title(f'Série de cargas Solar {i+1}')
#     # plt.plot(x, PVsystem_series, 'r')
#     plt.plot(x, PVsystem_series_raf, 'r')
#     plt.xlabel("hora")
#     plt.ylabel("Potência")
#     plt.show()


WTG_df = pd.read_csv(path_4, sep = ';', header = None)
WTG_df_raf = pd.read_csv(path_4_raf, sep = ';', header = None)


m, _ = WTG_df.shape

for i in range(m):

    # WTG_series = WTG_df.iloc[i, :Nt]
    WTG_series_raf = WTG_df_raf.iloc[i, :Nt].values / 1e3

    plt.figure(figsize = (10, 4))
    plt.title(f'Série de carga Eólica {i+1}')
    # plt.plot(x, WTG_series, 'r')
    plt.plot(x, WTG_series_raf, 'b')
    plt.xlabel('hora')
    plt.ylabel('Potência')
    plt.legend(['raf'])
    plt.show()

# PLD_df = pd.read_csv(path_5, sep = ';', header = None)
# PLD_df_raf = pd.read_csv(path_5_raf, sep = ';', header = None)

# print(PLD_df.shape)
# print(PLD_df_raf.shape)

# m, _ = PLD_df.shape

# for i in range(m):

#     PLD_series = PLD_df.iloc[i, :Nt]
#     PLD_series_raf = PLD_df_raf.iloc[i, :Nt]

#     plt.figure(figsize = (10, 4))
#     plt.plot(x, PLD_series, 'r')
#     plt.plot(x, PLD_series_raf, 'b')
#     plt.title(f'Série de Preço de Liquidação de Diferença {i+1}')
#     plt.xlabel('hora')
#     plt.ylabel('Potência')
#     plt.legend(['jon', 'raf'])
#     plt.show()

# Tdist_df = pd.read_csv(path_6, sep = ';', header = None).T
# Tdist_df_raf = pd.read_csv(path_6_raf, sep = ';', header = None)

# print(Tdist_df.shape)
# print(Tdist_df_raf.shape)

# m, _ = Tdist_df.shape

# for i in range(m):

#     TDist_series = Tdist_df.iloc[i, :Nt]
#     TDist_series_raf = Tdist_df_raf.iloc[i, :Nt]

#     plt.figure(figsize = (10, 4))
#     plt.title(f'Série de Tarifa da Distribuidora {i+1}')
#     plt.plot(x, TDist_series, 'r')
#     plt.plot(x, TDist_series_raf, 'b')
#     plt.xlabel('hora')
#     plt.xlabel('Potência')
#     plt.legend(['jon', 'raf'])
#     plt.show()

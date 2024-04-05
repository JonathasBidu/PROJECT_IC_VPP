import pandas as pd
import numpy as np

"""
    Carrega as projeções de carga, geração solar, geração eólica, e dados relacionados.

    Parâmetros:
    Nt (int): Número de intervalos de tempo na janela de projeção.
    Nl (int): Número de séries de carga a serem carregadas.
    Ndl (int): Número de séries de carga desconectada a serem carregadas.
    Npv (int): Número de séries de geração solar a serem carregadas.
    Nwt (int): Número de séries de geração eólica a serem carregadas.

    Retorna:
    Tuple: Uma tupla contendo arrays numpy representando as séries temporais de carga, geração solar, 
           geração eólica, carga desconectada de referência, carga desconectada mínima,
           carga desconectada máxima, PLD (Preço de Liquidação de Diferença), e Tau Dist.
           
    """

def carrega_projecoes(Nt:int, Nl:int, Ndl:int, Npv:int, Nwt:int)-> tuple:

    # Base de potência MW (Mega Watts)
    pbase = 1e6 
    # inicio = input('Instante inicial da série: ')
    inicio = 0

    # Caminho da primeira série
    # path_1 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\load_hourly_series.csv"
    path_1 =  "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\load_hourly_sistem.csv"

    # Carregamento da primeira série e extração da janela
    load_hourly_series_1 = pd.read_csv(path_1, sep = ';', header = None)
    # Desempacotamento do shape da primeira série
    m, _ = load_hourly_series_1.shape
    # Criando um vetor de números aleatórios não repetidos
    idx = np.random.choice(m, int(Nl), replace = False)
    # Selecionando um suconjunto de linha (idx) e um intervalo da série carregada load_hourly_series (inicio: (inicio + Nt))
    p_l = load_hourly_series_1.iloc[idx, inicio: (inicio + int(Nt))].values / pbase 
    
    # carregamento da segunda série e extração da janela
    # path_2 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\dload_hourly_series.csv"
    path_2 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\dload_hourly_seires.csv"
    load_hourly_series_2 = pd.read_csv(path_2, sep = ';', header = None)
    m, _ = load_hourly_series_2.shape
    idx = np.random.choice(m, int(Ndl)) 
    p_dl_ref = load_hourly_series_2.iloc[idx, inicio: (inicio + int(Nt))].values / pbase 
    
    # carregamento da terceira série e extração da janela
    # path_3 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\PVsystem_hourly_series.csv"
    path_3 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\PVsistem_hourly_system.csv"

    PVpwr_hourly_serie = pd.read_csv(path_3, sep = ';', header = None)
    m, _ = PVpwr_hourly_serie.shape
    idx = np.random.choice(m, int(Npv))
    p_pv = PVpwr_hourly_serie.iloc[idx, inicio: (inicio + int(Nt))].values / 1e3

    # carregamento da quarta série e extração da janela
    # path_4 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\WTGsystem_hourly_series.csv"
    path_4 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\WTGsystem_hourly_series.csv"
    WTGpwr_hourly_series = pd.read_csv(path_4, sep = ';', header = None)
    m, _ = WTGpwr_hourly_series.shape
    idx = np.random.choice(m, int(Nwt))
    p_wt = WTGpwr_hourly_series.iloc[idx, inicio: (inicio + int(Nt))].values / 1e3

    # carregamento da quinta série e extração da janela
    # path_5 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\PLD_hourly_data.csv"
    path_5 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\PLD_hourly_series.csv"
    PLD_hourly_series = pd.read_csv(path_5, sep = ';', header = None)
    tau_pld = PLD_hourly_series.iloc[0, inicio: (inicio + int(Nt))]

    # carregamento da sexta série e extração da janela
    # path_6 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\TDist_hourly_series.csv"
    path_6 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\TESTES_PYTHON\\SERIES_MATLAB\\TDist_hourly_series.csv"
    TDist_hourly_series = pd.read_csv(path_6, sep = ';', header = None)
    tau_dist = TDist_hourly_series.iloc[0, inicio: (inicio + int(Nt))]
    tau_dl = 0.15 * TDist_hourly_series.iloc[0, inicio: (inicio + int(Nt))] # Abatimento de 15% sobre o valor da tarifa

    dl_delta_min = np.zeros(int(Ndl))
    dl_delta_max = np.zeros(int(Ndl))

    for i in range(int(Ndl)):
        while True:
            dl_max = input(f'Limite superior de carga {i + 1} ((%) acima da referência): ')
            if dl_max == '':
                dl_max = 20.0 # Default de 20 por cento de limite de corte de carga superior
                break
            try:
                dl_max = float(dl_max)
                if dl_max > 0:
                    dl_delta_max[i] = dl_max
                    break
                print('Insira um valor real positivo')
            except ValueError:
                print("Informe um valor numérico válido")
    
    for i in range(int(Ndl)):
        while True:
            dl_min = input(f'Limite inferior de carga {i + 1} ((%) abaixo da referência): ')
            if dl_min == '':
                dl_delta_min[i] = 20.0 # Default de 20 por cento de limite de corte de carga inferior
                break
            try:
                dl_min = float(dl_min)
                if dl_min > 0:
                    dl_delta_min[i] = dl_min
                    break
                print('Insira um valor real positivo')
            except ValueError:
                print("Informe um valor numérico válido")

    print(' ')
    dl_delta_max = dl_delta_max / 100.0
    dl_delta_min = dl_delta_min / 100.0

    p_dl_max = np.zeros((int(Ndl), int(Nt)))
    p_dl_min = np.zeros((int(Ndl), int(Nt)))

    for i in range(int(Ndl)):
        p_dl_max[i, :] = p_dl_ref[i, :] + dl_delta_max[i] * np.abs(p_dl_ref[i,:])
        p_dl_min[i, :] = p_dl_ref[i, :] - dl_delta_min[i] * np.abs(p_dl_ref[i,:])

    return p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl

# Exemplo de uso

from vppdata1_module import vpp_data

data = vpp_data()

Nt = 24  # Número de pontos de dados na série temporal
Nl = data['Nl']   # Número de cargas
Ndl = data['Ndl'] # Número de cargas de referência
Npv = data['Npv']  # Número de sistemas fotovoltaicos
Nwt = data['Nwt']  # Número de sistemas de geração eólica

p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = carrega_projecoes(Nt, Nl, Ndl, Npv, Nwt)

# print(f'p_pl -> {p_l.shape} {type(p_l)} -> {p_l} \n')
# print(f'p_pv -> {p_pv.shape} {type(p_pv)} -> {p_pv} \n')
# print(f'p_wt -> {p_wt.shape} {type(p_wt)} -> {p_wt} \n')
# print(f'p_dl_ref -> {p_dl_ref.shape} {type(p_dl_ref)} -> {p_dl_ref} \n')
# print(f'p_dl_min -> {p_dl_min.shape} {type(p_dl_min)} -> {p_dl_min} \n')
# print(f'p_dl_max -> {p_dl_max.shape} {type(p_dl_max)} -> {p_dl_max} \n')
# print(f'tau_pld -> {tau_pld.shape} {type(tau_pld)} -> {tau_pld} \n')
# print(f'tau_dist -> {tau_dist.shape} {type(tau_dist)} -> {tau_dist} \n')
# print(f'tau_dl -> {tau_dl.shape} {type(tau_dl)} -> {tau_dl} \n')

import matplotlib.pyplot as plt

# Cargas despachaveis e não despachaveis
x_1 = np.concatenate((p_l.flatten(), p_dl_ref.flatten()))
d_1 = np.zeros((Nl + Ndl) * Nt) # Nl = 3, Nt = 24, Ndl = 2

# cargas das usinas
x_2 = np.concatenate((p_pv.flatten(), p_wt.flatten()))
d_2 = np.zeros((Npv + Nwt) * Nt) # Npv = 3, Nt = 24, Nwt = 3

pos = 0
for xi in x_1:
    d_1[pos] = np.sum(x_1 >= xi)
    pos += 1

pos = 0
for xi in x_2:
    d_2[pos] = np.sum(x_2 >= xi)
    pos += 1

idx_1 = np.argsort(d_1)
d_ord_1 = np.sort(d_1)
idx_2 = np.argsort(d_2)
d_ord_2 = np.sort(d_2)

plt.figure(figsize = (10, 5))
plt.plot(d_ord_1, x_1[idx_1])
plt.plot(d_ord_2, x_2[idx_2])
plt.title('Gráfico de duração de cargas')
plt.xlabel('duração')
plt.ylabel('Cargas')
plt.legend(['desp', 'ger'])
plt.tight_layout()
plt.show()

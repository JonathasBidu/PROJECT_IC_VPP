#  SCRIPT PARA GERAÇÃO DE SÉRIES DE IRRADIÂNCIA E TEMEPERATURA DE UMA USINA
#  FV, CÉLULAS FV DO TIPO POLYCRISTALINAS À PARTIR DE UM HISTÓRICO DE  DADOS
#  FONTE DO DADOS: <>
#  O SCRIPT GERA A POTÊNCIA ELÉTRICA CONSIDERANDO UM MODELO DE 2 DIODOS

#  filename: C:\Users\abelt\OneDrive\Área de Trabalho\Timeseries_Base_Diaria.csv
import numpy as np
import pandas as pd
from PVGenPwr import PVGenPwr as pv

#  Obtendo o arquivo .csv a partir da oitava linha
path = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\BASE_DE_DADOS\\Timeseries_diario_2010_2020_2.csv"
data = pd.read_csv(path, sep = ';',skiprows = 8)

# Convertendo a coluna G(i) que contém a irradiância em números flutuantes
data['G(i)'] = pd.to_numeric(data['G(i)'], errors = 'coerce')
# Selecionando apenas G(i)(irradiância solar) e T2m(temperatura(em graus Celsius))
solar_tsdata = data[['G(i)', 'T2m']]
# Limitando a parte inferior do arquivo .csv
solar_tsdata = solar_tsdata.iloc[: 8760]
# obtendo a série histórica de irradiância 
irradiance_hourly_series = solar_tsdata['G(i)']
# Obtendo a histórica temperatura 
temperature_hourly_series = solar_tsdata['T2m']
# Obtendo o tamanho da série
Npoints = len(irradiance_hourly_series)
# criando um vetor de zero com o tamanho das série acima 
PVpwr_irradiance_hourly_series = np.zeros(Npoints)

# Parâmetros do sistema fotovoltaico
Np = 400 # Número de células em paralelo
Ns = 2000 # Número de célula em serie

# Efetuando os cálculos para temperatura e irradiâcia a cada hora do dia em um ano
for time in range(Npoints):
    T = temperature_hourly_series[time] + 20 + 273.15
    T += 25.00
    G = irradiance_hourly_series[time]
    # Chamando a função PVGenpwr passando os paramêtros irradiância, temperatura, número de placas e (tirar dúvida)
    Pmmp, Vmmp, Immp = pv(G, T, Np, Ns) # Pmmp vetor de potência, Vmmp vetor de tensão e Immp vetor de corrente.
    # Obtendo a potência máxima gerada pela usina
    PVpwr_irradiance_hourly_series[time] = Pmmp
    print(time)

# Criando um dataframe com a série da potência gerada pela usina
PVpwr_hourly_series_pd = pd.DataFrame(PVpwr_irradiance_hourly_series)
PVpwr_hourly_series_pd = PVpwr_hourly_series_pd.T # Tranposição da série de potência
PVpwr_hourly_series_pd.to_csv("C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\PVsystem_hourly_series.csv", sep = ';', index = False, header = None)

import numpy as np
import pandas as pd
from scipy.stats import weibull_min 

''' SCRIPT PARA GERACAO DE SERIES DE VENTO A PARTIR DO CRESESB
    SUPOSICAO: VENTO TEM DISTRIBUICAO DE WEIBULL COM FATOR DE FORMA k e FATOR
    DE ESCALA C:
    f(v)=(k/C)(v/C)^(k-1)exp(-(v/C)^k) onde v eh a velocidade do vento e 
    f a funcao densidade de probabilidade de v.
'''

# Definindo o número de pontos simulados e cenários
Npoints = 8760
Nscenarios = int(input("Insira a quantidade de cenário(s) desejado: ") or 11)

#  Exemplo:
#   Para uma localizacao {Latitude:22,900223°  S, Longitude:43,125608° O}
#   o valor de C e k para cada periodo do ano sao:
#       Periodo    |    C    |    k
#       Dez-Fev    |  5.07   |  1.82  
#       Mar-Mai    |  4.93   |  1.82
#       Jun-Ago    |  5.88   |  1.95
#       Set-Nov    |  5.22   |  1.90
#   Logo, pode-se adotar para scale e shape:
#       scale=[5.07;4.93;5.88;5.22]
#       shape=[1.82;1.82;1.95;1.90];

# Definindo parâmetros da distribuição da velocidade do vento
wind_hourly_series = np.zeros((Nscenarios, Npoints))
scale = np.array(input('digite os fatores de escala c para cada trimestre do ano: ') or [5.07, 4.93, 5.88, 5.22], dtype=float) 
shape = np.array(input('digite os fatores de forma k para cada trimestre do ano: ') or [1.82, 1.82, 1.95, 1.90], dtype=float) 

# Geração das séries temporais de Weilbull
dim1 = 1
dim2 = int(8760/4) # Total de horas por trimestre
for s in range(Nscenarios):
    for trimestre in range(4):
        inicio = dim2 * trimestre
        fim = dim2 * (trimestre + 1)
        a = scale[trimestre]
        b = shape[trimestre]
        wind_hourly_series[s, inicio: fim] = weibull_min.rvs(b, scale=a, size=dim2)

# Geração de Séries Temporais de Potência WTG
print('\nParametros da UG Eolica\n')
cut_in_speed = float(input('Velocidade de cut_in da turbina (m/s) [2.2]: ') or 2.2) 
cut_out_speed = float(input('Velocidade de cut_out da turbina (m/s) [25.0]: ') or 25.0)
nom_speed = float(input('Velocidade nominal da turbina (m/s) [12.5]: ') or 12.5)
nom_pwr = float(input('Potência nominal da turbina (W) [6000]: ') or 6000)
Nwtg = int(input('Número de turbinas eólicas [1]: ') or 1)

# Geração das Séries Temporais de potência da turbina eólica
WTGpwr_hourly_series = np.zeros_like(wind_hourly_series)
for s in range(Nscenarios):
    for time in range(Npoints):
        speed = wind_hourly_series[s, time]
        Pwtg = min(max(0, (speed - cut_in_speed) / (nom_speed - cut_in_speed)), 1) * nom_pwr * Nwtg
        WTGpwr_hourly_series[s, time] = Pwtg

# Salvar o DataFrame em um arquivo CSV, Excel ou outro formato
WTGpwr_hourly_series_df = pd.DataFrame(WTGpwr_hourly_series)
WTGpwr_hourly_series_df.to_csv("C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\WTGsystem_hourly_series.csv",
    sep=';',
    index = False,
    header = None
    )

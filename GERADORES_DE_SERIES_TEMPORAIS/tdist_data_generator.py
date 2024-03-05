import numpy as np
import pandas as pd

# Este script gera tarifas de energia para distribuidora e consumidores
# Premissas:
    # Periodização horaria
    # Hora zero - 1o. registo dos dados
    # Desconsidera feriados e finais de semana
    # Horario de Ponta: 18h - 20h59 (dias uteis de segunda a sexta)
    # Horario Intermediário: 16h - 17h59 e 21h - 21h59h
    # Horario Fora de Ponta: 22h - 15h59h
    # Fonte: https://www.reclameaqui.com.br/enel-distribuicao-rio/tarifa-branca_tXRUzcJG6p-KOBAL/
    # Valor Enel Março 21
        # PONTA = R$1.33333
        # INTERMEDIÁRIA = R$0.88020
        # FORA PONTA = R$0.57060


horas_ano = 8760 # total de horas
TDist_hourly_series = np.zeros(horas_ano)
horas_dia = 24

PONTA = 1.33333
INTERMEDIARIA = 0.88020
FORA_PONTA = 0.57060

t = 1

while t <= horas_ano:
    day = (t-1) // horas_dia # Obtendo o dia
    h = (t-1) % horas_dia # Obtendo a hora
    if 0<= h < 16:
        TDist_hourly_series[t-1] = FORA_PONTA
    elif 16 >= h < 18:
        TDist_hourly_series[t-1] = INTERMEDIARIA
    elif 18 >= h < 21:
        TDist_hourly_series[t-1] = PONTA
    elif 21 >= h < 22:
        TDist_hourly_series[t-1] = INTERMEDIARIA
    else:
        TDist_hourly_series[t-1] = FORA_PONTA
    t+=1


# Salvar o DataFrame em um arquivo CSV, Excel ou outro formato
TDist_hourly_series_df = pd.DataFrame(TDist_hourly_series.T)
TDist_hourly_series_df.to_csv("C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\SERIES_GERADAS\\TDist_hourly_series.csv",
    sep = ";",
    index = False,
    header = None
    )

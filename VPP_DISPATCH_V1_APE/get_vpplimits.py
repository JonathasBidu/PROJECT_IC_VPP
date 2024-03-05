from vppdata1_module import vpp_data as vpp
from carrega_projecoes import carrega_projecoes as cp
import numpy as np

"""
    Esta função constrói o vetor de limites para a VPP descrita em VPP data

    Parâmetros:
    - vpp_data: Dicionário contendo os parametros da VPP. possui os seguintes atributos:

        - Nt: número de instantes de simulação
        - Nbm: número de usinas biomassa
        - Ndl: número de cargas despacháveis
        - Nbat: número de baterias
        - Nwt: número de geradores eólicos
        - Npv: número de usinas solares
        - p_l: potência das cargas, dimensão ((Nl*Nt), 1)
        - p_pv: potência das UG solares FV, dimensão ((Npv*Nt), 1)
        - p_wt: potência das UG eólicas, dimensão ((Nwt*Nt), 1)
        - p_bm_min: potência mínima biomassa, dimensão (Nbm, 1)
        - p_bm_max: potência máxima biomassa, dimensão (Nbm, 1)
        - p_bm_rup: potência máxima ramp up biomassa, dimensão (Nbm, 1)
        - p_bm_rdown: potência máxima ramp down biomassa, dimensão (Nbm, 1)
        - eta_chg: rendimento carga bateria, dimensão (Nbat, 1)
        - eta_dch: rendimento descarga bateria, dimensão (Nbat, 1)
        - soc_min: SoC mínimo bateria, dimensão (Nbat, 1)
        - soc_max: SoC máximo bateria, dimensão (Nbat, 1)
        - p_bat_max: potência máxima carga/descarga bateria, dimensão (Nbat, 1)
        - p_dl_min: potência mínima despachável carga, dimensão (Ndl, 1)
        - p_dl_max: potência máxima despachável carga, dimensão (Ndl, 1)
        - tau_dl: compensação por corte, dimensão (Ndl, 1)
        - tau_pld: PLD, dimensão (Nt, 1)
        - tau_dist: tarifa distribuidora
        - kappa_pv: custo unitário ger. solar
        - kappa_wt: custo unitário ger. eólica
        - kappa_bm: custo unitário ger. biomassa
        - kappa_bm_start: custo unitário partida ger. biomassa
        - kappa_bat: custo baterias

    Retorna:
        - Uma tupla contendo dois vetores que limitam...
            - lb: vetor limite inferior das variáveis de decisão
            - ub: vetor limite superior das variáveis de decisão

"""

def get_vpplimits_v1(vpp_data):

    Nt = int(vpp_data['Nt']) # 24
    Nbm = int(vpp_data['Nbm']) # 2
    Ndl = int(vpp_data['Ndl']) # 2
    Nbat = int(vpp_data['Nbat']) # 1
    # Nbm = int(vpp_data['Nbm'])

    # Obtencao dos paramteros da VPP
    Nr = (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt)
    Ni = (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt)

    #  Criação lb e ub
    # nvars -> Qtd de variáveis
    nvars = Nr + Ni
    lb = np.zeros(nvars) 
    ub = np.ones(nvars) 

    # limtes de p_bm
    inicio = 0 ###################################################### Verificar se pode remover essa variável ##############
    # fim = fim + (vpp_data.Nbm * vpp_data.Nt); apenas para lembrar a indexação
    fim = 0
    for i in range(Nbm): # Nbm == 2
        for j in range(Nt): # Nt == 24 -> Nt * Nbm == 48
            lb[fim] = vpp_data['p_bm_min'][i]
            ub[fim] = vpp_data['p_bm_max'][i] # conferido e está correto
            fim += 1 # fim == 48

    # limtes de p_dl
    inicio = fim
    # fim = fim + (vpp_data.Ndl * vpp_data.Nt); apenas para lembrar a indexação
    fim = inicio
    for i in range(Ndl): # Ndl  == 2
        for j in range(Nt): # Nt == 24 -> Nt * Ndl == 48
            lb[fim] = vpp_data['p_dl_min'][i, j]
            ub[fim] = vpp_data['p_dl_max'][i, j]
            fim += 1 # fim == 96

    # limtes de p_chg
    inicio = fim
    # fim = fim + (vpp_data.Nbat * vpp_data.Nt); apenas para lembrar a indexação
    fim = inicio
    for i in range(Nbat): # Nbat == 1
        for j in range(Nt): # Nt == 24 -> Nt * Nbat == 24
            ub[fim] = vpp_data['p_bat_max'][i]
            fim += 1 # fim == 120
  
    # limtes de p_dch
    inicio = fim
    # fim = fim + (vpp_data.Nbat * vpp_data.Nt); apenas para lembrar a indexação
    fim = inicio
    for i in range(Nbat): # Nbat == 1
        for j in range(Nt): # Nt == 24 -> Nt * Nbat == 24
            ub[fim] = vpp_data['p_bat_max'][i]
            fim += 1 # fim == 144

    # limtes de soc
    inicio = fim
    # fim = fim + (vpp_data.Nbat * vpp_data.Nt); apenas para lembrar a indexação
    fim = inicio
    for i in range(Nbat): # Nbat == 1
        for j in range(Nt): # Nt == 24 -> Nt * Nbat == 24
            lb[fim] = vpp_data['soc_min'][i]
            ub[fim] = vpp_data['soc_max'][i]
            fim += 1 # fim == 168
            
    # limites de u_exp, i_imp, u_bm, u_dl, u_dch e u_dch lb = 0 e ub = 1
            
    return lb, ub


# Teste
# v = vpp()

# Nt = 24  # Número de pontos de dados na série temporal
# Nl = 5   # Número de cargas
# Ndl = 2  # Número de cargas de referência
# Npv = 10  # Número de sistemas fotovoltaicos
# Nwt = 8  # Número de sistemas de geração eólica

# p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = cp(Nt, Nl, Ndl, Npv, Nwt)

# v['Nt'] = Nt
# v['p_l'] = p_l
# v['p_pv'] = p_pv
# v['p_wt'] = p_wt
# v['p_dl_ref'] = p_dl_ref
# v['p_dl_min'] = p_dl_min
# v['p_dl_max'] = p_dl_max
# v['tau_pld'] = tau_pld
# v['tau_dist'] = tau_dist
# v['tau_dl'] = tau_dl


# lb, ub = get_vpplimits_v1(v)

# print(f'O vetor lb é do tipo {type(lb)} tem o shape = {lb.shape}')
# print(f'O vetor ub é do tipo {type(ub)} tem o shape = {ub.shape} \n')
# # print(f'lb -> {lb[94]} \n')
# # print(f'lb -> {lb[94]} \n')

# condicoes = []
# a = True
# for i in range(len(lb)):
#     condicoes.append(lb[i] <= ub[i])
#     print(f'{i}->{lb[i] <= ub[i]}')
#     if lb[i] > ub[i]:
#         print(f'lb -> {lb[i]} \n')
#         print(f'ub -> {ub[i]} \n')
#         break
# print("Condições de limite:")
# print(condicoes)

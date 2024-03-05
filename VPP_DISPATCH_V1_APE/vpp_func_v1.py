from decomp_vetor_v1 import decomp_vetor_v1
from vppdata1_module import vpp_data as vpp
import numpy as np

"""
    Descrição da Função:
    Esta função contém o cálculo da função objetivo do modelo da VPP, para uso em um ga(genetic algorithm | algoritmo genético).

    Parâmetros:
    - x: vetor de variáveis
    - vpp_data: estrutura de dicionário contendo os parâmetros da VPP. Possui os seguintes atributos:
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
        - fval: O lucro obtido na operação da VPP(Virtual Power Plant)
"""

def vpp_func_v1(x, vpp_data):

    Nt = vpp_data['Nt']
    Nbm = vpp_data['Nbm']
    Ndl = vpp_data['Ndl']
    Nl = vpp_data['Nl']
    Nbat = vpp_data['Nbat']
    Npv = vpp_data['Npv']
    Nwt = vpp_data['Nwt']
    # p_bm_min = vpp_data['p_bm_min']
    # p_bm_max = vpp_data['p_bm_max']
    # p_bm_rup = vpp_data['p_bm_rup']
    # p_bm_rdown = vpp_data['p_bm_rdown']
    # eta_chg = vpp_data['eta_chg']
    # eta_dch = vpp_data['eta_dch']
    # soc_min = vpp_data['soc_min']
    # soc_max = vpp_data['soc_max']
    # p_bat_max = vpp_data['p_bat_max']
    # p_dl_min = vpp_data['p_dl_min']
    # p_dl_max = vpp_data['p_dl_max']
    p_pv = vpp_data['p_pv']
    p_wt = vpp_data['p_wt']
    p_l = vpp_data['p_l']
    tau_pld = vpp_data['tau_pld']
    tau_dist = vpp_data['tau_dist']
    tau_dl = vpp_data['tau_dl']
    kappa_pv = vpp_data['kappa_pv']
    kappa_wt = vpp_data['kappa_wt']
    kappa_bm = vpp_data['kappa_bm']
    kappa_bat = vpp_data['kappa_bat']
    kappa_bm_start = vpp_data['kappa_bm_start']

    #  Separação das variaveis no vetor solução
    # p_exp, p_imp, p_bm, p_dl, p_chg, p_dch, soc, u_exp, u_imp, u_bm, u_dl, u_chg, u_dch = decomp_vetor(x, Nt, Nbm, Ndl, Nbat)

    p_bm, p_dl, p_chg, p_dch, soc, u_bm, u_dl, u_chg, u_dch = decomp_vetor_v1(x, Nt, Nbm, Ndl, Nbat)
    
    # Reshape vetores em matrizes
    p_bm = p_bm.reshape((Nt, Nbm))
    p_dl = p_dl.reshape((Nt, Ndl))
    p_chg = p_chg.reshape((Nt, Nbat))
    p_dch = p_dch.reshape((Nt, Nbat))
    soc = soc.reshape((Nt, Nbat))
    u_bm = u_bm.reshape((Nt, Nbm))
    u_dl = u_dl.reshape((Nt, Ndl))
    u_chg = u_chg.reshape((Nt, Nbat))
    u_dch = u_dch.reshape((Nt, Nbat))

    # Potência líquida
    p_liq = np.zeros(Nt)
    for t in range(Nt):
    # k = k + 1
        for i in range(Npv):
            p_liq[t] += p_pv[i, t]
        for i in range(Nwt):
            p_liq[t] += p_wt[i, t]
        for i in range(Nbm):
            p_liq[t] += p_bm[t, i] * u_bm[t, i]	
        for i in range(Nl):
            p_liq[t] -= p_l[i, t]
        for i in range(Ndl):
            p_liq[t] -= p_dl[t, i] * u_dl[t, i]
        for i in range(Nbat):            
            
            p_liq[t] -= p_chg[t, i] * u_chg[t, i] + p_dch[t, i] * u_dch[t, i]
    
    p_exp = np.maximum(0, p_liq) 
    p_imp = np.maximum(0, -p_liq)

    # Receita com excedente de energia
    R = 0
    for t in range(Nt):
        R += p_exp[t] * tau_pld[t] # conferido

    # Despesa com importação de energia com a comportação de energia
    D = 0
    
    # Importação de energia da distribuidora
    for t in range(Nt):
        D += p_imp[t] * tau_dist[t]

    # Custos de geração solar fotovoltaica
    Cpv = 0
    for t in range(Nt):
        for i in range(Npv):
            Cpv += p_pv[i, t] * kappa_pv[i] # conferido (ok!)

    # Custos de geração Eólica
    Cwt = 0
    for t in range(Nt):
        for i in range(Nwt):
            Cwt += p_wt[i, t] * kappa_wt[i] # conferido (ok!)

    # Custos de geração biomassa (custo linear)
    Cbm = 0
    for t in range(Nt):
        for i in range(Nbm):
            Cbm += p_bm[t, i] * u_bm[t, i] * kappa_bm[i] # conferido

    #  custo de partida
    for t in range(1, Nt):
        for i in range(Nbm):
            Cbm += (u_bm[t, i] - u_bm[t - 1, i]) * kappa_bm_start[i]

    # Custo de controle carga despachada
    Cdl = 0
    for t in range(Nt):
        for i in range(Ndl):
            Cdl += p_dl[t, i] * u_dl[t, i] * tau_dl[t]

    # Custo da bateria
    Cbat = 0
    for t in range(Nt):
        for i in range(Nbat):
            Cbat += ((p_chg[t, i] * u_chg[t, i] + p_dch[t, i] * u_dch[t, i]) * kappa_bat[i])

    # Despesa total
    D = D + Cpv + Cwt + Cbm + Cdl + Cbat
    fval = R - D
    
    return fval



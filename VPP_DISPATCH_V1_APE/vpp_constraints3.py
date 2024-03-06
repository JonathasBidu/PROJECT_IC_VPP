import numpy as np
from decomp_vetor_v1 import decomp_vetor_v1
"""
    Descrição do script
    Este script contém as restrições não lineares do modelo da VPP, para o uso do ga.

    Paramêtros:
    - x: vetor de variáveis
    - vpp_data: Dicionário contendo os parâmetros da VPP, que por sua vez possuí os seguintes atributos;
        Nt - número de instantes de simulação
        Nbm - número de usinas biomassa
        Ndl - número de cargas despachaveis
        Nbat - número de baterias
        Nwt - número de geradores eólicos
        Npv - número de usinas solares
        p_l - potência das cargas, dimensão ((Nl*Nt), 1)
        p_dl - potência das cargas despachaveis, dimensao ((Ndl*Nt), 1)
        p_pv - potência das UG solares FV, dimensão ((Npv*Nt), 1)
        p_wt - potência das UG eóliacas, dimensão ((Nwt*Nt), 1)
        p_bm_min - pot. mínima biomassa, dimensão (Nbm, 1)
        p_bm_max - pot. máxima biomassa, dimensão (Nbm, 1)
        p_bm_rup - pot. máxima ramp up biomassa, dimensão (Nbm, 1)
        p_bm_rdown  - pot. máxima ramp down biomassa, dimensão (Nbm, 1)
        eta_chg - rendimento carga bateria, dimensão (Nbat, 1)
        eta_dch - rendimento descarga bateria, dimensão (Nbat, 1)
        soc_min - SoC mínimo bateria, dimensão (Nbat, 1)
        soc_max - SoC máximo bateria, dimensão (Nbat, 1)
        p_bat_max  - pot. máxima carga/descarga bateria, dimensão (Nbat, 1)
        p_dl_min - pot. mínima despachavel carga, dimensão (Ndl, 1)
        p_dl_max - pot. máxima despachavel carga, dimensão (Ndl, 1)
        tau_pld  - PLD, dimensão (Nt, 1)
        tau_dist - tarifa distribuidora, dimensao (Nt, 1)
        tau_dl - compensacao por corte, dimensao (Nt, 1)
        kappa_pv - custo unitário ger. solar
        kappa_wt - custo unitário ger. eólica
        kappa_bm - custo unitário ger. biomassa
        kappa_bm_start - custo unitário partida ger. biomassa

         Retorna:
            - Tuple - Uma tupla contendo duas listas;
                - c: Por ora, uma lista vazia
                - ceq: uma lista que cotém;
                    - c_bm:
                    - c_bat:
                    - c_dl:
                    - c_ie:
                    - c_pwrbal: 

"""

def vpp_constraints3(x, vpp_data):
    Nt = vpp_data['Nt']
    Nbm = vpp_data['Nbm']
    # Nl = vpp_data['Ndl']
    Ndl = vpp_data['Ndl']
    Nbat = vpp_data['Nbat']
    # Npv = vpp_data['Npv']
    # Nwt = vpp_data['Nwt']
    p_bm_min = vpp_data['p_bm_min']
    p_bm_max = vpp_data['p_bm_max']
    p_bm_rup = vpp_data['p_bm_rup']
    p_bm_rdown = vpp_data['p_bm_rdown']
    eta_chg = vpp_data['eta_chg']    
    eta_dch = vpp_data['eta_dch']
    # soc_min = vpp_data['soc_min']    
    # soc_max = vpp_data['soc_max']    
    p_bat_max = vpp_data['p_bat_max']
    p_dl_min = vpp_data['p_dl_min']
    p_dl_max = vpp_data['p_dl_max']
    # tau_pdl = vpp_data['tau_pdl']
    # tau_dist = vpp_data['tau_dist']
    # p_pv = vpp_data['p_pv']
    # p_wt = vpp_data['p_wt']
    # p_l = vpp_data['p_l']
    # tau_dl = vpp_data['tau_dl']
    # kappa_pv = vpp_data['kappa_pv']
    # kappa_wt = vpp_data['kappa_wt']
    # kappa_bm = vpp_data['kappa_bm']
    # kappa_bm_start = vpp_data['kappa_bm_start']
    # kappa_bm_start = vpp_data['kappa_bat']

    # Separação de variáveis do vetor solução
    p_bm, p_dl, p_chg, p_dch, soc,u_bm, u_dl, u_chg, u_dch = decomp_vetor_v1(x, Nt, Nbm, Ndl, Nbat)

    ###################### TIRAR DÚVIDA POIS, ESSE DESEMPACOTAMENTO NÃO CONDIZ COM O RETORNO DA FUNÇÃO ACIMA ##################
    # reshape vetores em matrizes     
    p_bm = p_bm.reshape((Nbm, Nt))
    p_dl = p_dl.reshape((Ndl, Nt))
    p_chg = p_chg.reshape((Nbat, Nt))
    p_dch = p_dch.reshape((Nbat, Nt))
    soc = soc.reshape((Nbat, Nt))
    u_bm = u_bm.reshape((Nbm, Nt))
    u_dl = u_dl.reshape((Ndl, Nt))
    u_chg = u_chg.reshape((Nbat, Nt))
    u_dch = u_dch.reshape((Nbat, Nt))

    # Restricoes da biomassa
    Nbmc = (Nt * Nbm) + (Nt * Nbm) + ((Nt - 1) * Nbm) + ((Nt - 1) * Nbm)
    c_bm = np.zeros(Nbmc)
    k = 0

    # p_bm_max
    for i in range(Nbm):
        for t in range(Nt):
            c_bm[k] = p_bm[i, t] - p_bm_max[i] * u_bm[i, t]
            k += 1

    # p_bm_min
    for i in range(Nbm):
        for t in range(Nt):
            c_bm[k] = p_bm_min[i, t] * u_bm[i, t] - p_bm[i, t]
            k += 1

    # p_bm_rup
    for i in range(Nbm):
        for t in range(1, Nt):
            c_bm[k] = p_bm[i, t] - p_bm[i, t - 1] - p_bm_rup[i]
            k += 1

    # p_bm_rdown
    for i in range(Nbm):
        for t in range(1, Nt):
            c_bm[k] = p_bm[i, t] - p_bm[i, t - 1] - p_bm_rdown[i]
            k += 1

    # Restrições da bateria
    Nbatc = ((Nt - 1) * Nbat) + ((Nt - 1) * Nbat) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Nbat) # + (Nt * Nbat) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Nbat)
    c_bat = np.zeros(Nbatc)

    # soc balanço +
    for i in range(Nbat):
        for t in range(1, Nt):
            c_bat[k] = soc[i, t] - soc[i, t - 1]
            c_bat[k] = c_bat[k] - p_chg[i, t] * eta_chg[i]
            c_bat[k] = c_bat[k] - p_dch[i, t] / eta_chg[i]
            k += 1

    # soc balanço -
    shift = ((Nt - 1) * Nbat)
    for i in range(Nbat):
        for t in range(1, Nt):
            c_bat[k] = - c_bat[k - shift]
            k += 1

    # limites máximo carga
    for i in range(Nbat):
        for t in range(Nt):
            c_bat[k] = p_chg[i, t] - p_bat_max[i] * u_chg[i, t]
            k += 1

    # limites mínimo descarga
    for i in range(Nbat):
        for t in range(Nt):
            c_bat[k] = p_dch[i, t] - p_bat_max[i] * u_dch[i, t]
            k += 1

    # status de carga/descarga
    for i in range(Nbat):
        for t in range(Nt):
            c_bat[k] = u_chg[i, t] + u_dch[i, t] - 1
            k += 1

    # Restrições das cargas despachaveis 
    Ndlc = (Nt * Ndl) + (Nt * Ndl)
    c_dl = np.zeros(Ndlc)
    k = 0 

    # p_dl_max
    for i in range(Ndl):
        for t in range(Nt):
            c_dl[k] = p_dl[i, t] * p_dl_max[i, t] * u_dl[i, t]
            k += 1

    # p_dl_min
    for i in range(Ndl):
        for t in range(Nt):
            c_dl[k] = p_dl_min[i, t] * u_dl[i, t] - p_dl[i, t]
            k += 1

    # Construção do vetor de restrições

    c = []
    ceq = [c_bm, c_bat , c_dl] #, c_ie, c_pwrbal]
    return c, ceq
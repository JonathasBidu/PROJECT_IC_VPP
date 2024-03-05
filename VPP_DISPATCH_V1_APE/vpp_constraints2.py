import numpy as np
from VPP_DISPATCH_V1_APE.vppdata1_module import vpp_data
from decomp_vetor_v1 import decomp_vetor_v1
"""
    Descrição do script
    Este script contém as restrições não lineares do modelo da VPP, para o uso do ga.

    Paramêtros:
    - x: 
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
def vpp_constraints2(x, vpp_data):

    Nt = vpp_data['Nt'] # Não há esse dado em VPPDATA1
    Nbm = vpp_data['Nbm']
    Nl = vpp_data['Nl']
    Ndl = vpp_data['Ndl']
    Nbat = vpp_data['Nbat']
    Npv = vpp_data['Npv']
    Nwt = vpp_data['Nwt']
    p_bm_min = vpp_data['p_bm_min']
    p_bm_max = vpp_data['p_bm_max']
    p_bm_rup = vpp_data['p_bm_rup']
    p_bm_rdown = vpp_data['p_bm_rdown']
    eta_chg = vpp_data['eta_chg']
    eta_dch = vpp_data['eta_dch']
    # soc_min = vpp_data['soc_min']
    # soc_max = vpp_data['soc_max']
    p_bat_max = vpp_data['p_bat_max']
    p_dl_min = vpp_data['p_dl_min'] # Não tem esse dado em VPPDATA1
    p_dl_max = vpp_data['p_dl_max'] # Não tem esse dado em VPPDATA1
    # tau_pld = vpp_data['tau_pld']
    # tau_dist = vpp_data['tau_dist']
    p_pv = vpp_data['p_pv'] # Não tem esse dado em VPPDATA1
    p_wt = vpp_data['p_wt'] # Não tem esse dado em VPPDATA1
    p_l = vpp_data['p_l'] # Não tem esse dado em VPPDATA1
    # tau_dl = vpp_data['tau_dl']
    # kappa_pv = vpp_data['kappa_pv']
    # kappa_wt = vpp_data['kappa_wt']
    # kappa_bm = vpp_data['kappa_bm']
    # kappa_bm_start = vpp_data['kappa_bm_start']
    # kappa_bm_start = vpp_data['kappa_bat']

    # separacao das variaveis no vetor solucao
    ################## TIRAR DÚVIDA, NO SCRIPT TEM UMA FUNÇÃO decomp_vetor e não decomp_vetor_v1 #############################
    p_exp, p_imp, p_bm, p_dl, p_chg, p_dch, soc, u_exp, u_imp, u_bm, u_dl, u_chg, u_dch = decomp_vetor_v1(x, Nt, Nbm,Ndl, Nbat)

    ###################### TIRAR DÚVIDA POIS, ESSE DESEMPACOTAMENTO NÃO CONDIZ COM O RETORNO DA FUNÇÃO ACIMA ##################
    # reshape vvetores em matrizes
    p_bm = p_bm.reshape((Nt, Nbm))
    p_dl = p_dl.reshape((Nt, Ndl))
    p_chg = p_chg.reshape((Nt, Nbat))
    p_dch = p_dch.reshape((Nt, Nbat))
    soc = soc.reshape((Nt, Nbat))
    u_bm = u_bm.reshape((Nt, Nbm))
    u_dl = u_dl.reshape((Nt, Ndl))
    u_chg = u_chg.reshape((Nt, Nbat))
    u_dch = u_dch.reshape((Nt, Nbat))

    # Restricoes da biomassa
    Nbmc = (Nt * Nbm) + (Nt * Nbm) + ((Nt - 1) * Nbm) + ((Nt - 1) * Nbm)
    c_bm = np.zeros(Nbmc)
    k = 0

    # p_bm_max
    for i in range(1, Nbm):
        for t in range(1, Nt):
            k += 1
            c_bm[k] = p_bm[i, t] - p_bat_max[i] * u_bm[i, t]

    # p_bm_min
    for i in range(1, Nbm):
        for t in range(1, Nt):
            k += 1
            c_bm[k] = p_bm_min[i] * u_bm[i, t] - p_bm[i, t]

    # p_bm_rup
    for i in range(1, Nbm):
        for t in range(2, Nt):
            k += 1
            c_bm[k] = p_bm[i, t] - p_bm[i, t - 1] - p_bm_rup[i]

    # p_bm_rdown
    for i in range(1, Nbm):
        for t in range(2, Nt):
            k += 1
            c_bm[k] = p_bm[i, t] - p_bm[i, t - 1] - p_bm_rdown[i]

    # Restricoes da bateria
    Nbatc = ((Nt - 1) * Nbat) + ((Nt - 1) * Nbat) + (Nt * Nbat) + (Nt * Nbat) + (Nt*Nbat) # + (Nt*Nbat) + (Nt*Nbat) + (Nt*Nbat) + (Nt*Nbat)

    c_bat = np.zeros(Nbatc)
    k = 0 

    # soc balanço +
    for i in range(1, Nbat):
        for t in range(2, Nt):
            k += 1
            c_bat[k] = soc[i, t] - soc[i, t - 1]
            c_bat[k] = c_bat[k] - p_chg[i, t] * eta_chg[i]
            c_bat[k] = c_bat[k] + p_dch[i, t] / eta_dch[i]

    # soc balanço -
    shift = ((Nt - 1) * Nbat)
    for i in range(1, Nbat):
        for t in range(2, Nt):
            k += 1
            c_bat[k] = - c_bat[k - shift]

    # limites mínimo soc
    # for i in range(1, Nbat):
    #     for t in range(1, Nt):
    #         k += 1
    #         c_bat[k] = soc_min[i] - soc[i, t]
            
    # limites máximo soc
    # for i in range(1, Nbat):
    #     for t in range(1, Nt):
    #         k += 1
    #         c_bat[k] = soc[i, t] - soc_max[i]
    
    # limites mínimo carga
    # for i in range(1, Nbat):
    #     for t in range(1, Nt):
    #         k += 1
    #         c_bat[k] = - p_dch[i, t]
            
    # limites máximo carga
    # for i in range(1, Nbat):
    #     for t in range(1, Nt):
    #         k += 1
    #         c_bat[k] = p_chg[i, t] - p_bat_max[i] * u_chg[i, t]
            
    # limites máximo descarga
    # for i in range(1, Nbat):
    #     for t in range(1, Nt):
    #         k += 1
    #         c_bat[k] = p_dch[i, t] - p_bat_max[i] * u_dch[i, t]

    # status de carga/descarga
    # for i in range(1, Nbat):
    #     for t in range(1, Nt):
    #         k += 1
    #         c_bat[k] = u_chg[i, t] + u_dch[i, t] - 1
            
    # Restrições das cargas despachaveis
    Ndlc = (Nt * Ndl) + (Nt * Ndl)
    c_dl = np.zeros(Ndlc)
    k = 0

    # p_dl_max
    for i in range(1, Ndl):
        for t in range(1, Nt):
            k += 1
            c_dl[k] = p_dl[i, t] - p_dl_max[i, t] * u_dl[i, t]

    # p_dl_min
    for i in range(1, Ndl):
        for t in range(1, Nt):
            k += 1
            c_dl[k] = p_dl_min[i, t] * u_dl[i, t] - p_dl[i, t]
    
    # Restrições de importação/exportação
    Nie = Nt + Nt + Nt
    c_ie = np.zeros(Nie)
    k = 0

    # min importação
    # for t in range(Nt):
    #     k += 1
    #     c_ie[k] = - p_imp[t]
    
    # min exportacao
    # for t in range(Nt):
    #     k += 1
    #     c_ie[k] = - p_exp[t]

    M = 1e10
    # max importação
    for t in range(Nt):
        k += 1
        c_ie[k] = p_imp[t] - M * u_imp[t]
    
    # max exportação
    for t in range(Nt):
        k += 1
        c_ie[k] = p_exp[t] - M * u_exp[t]

    # estado importação exportação
    for t in range(Nt):
        k += 1
        c_ie[k] = u_exp[t] + u_imp[t] - 1

    # Restrições de balanco de energia
    Npwrbal = Nt + Nt
    c_pwrbal = np.zeros(Npwrbal)
    # k = 0
    # balanco potência +
    for t in range(Nt):
        k += 1
        for i in range(Npv):
            c_pwrbal[t] = c_pwrbal[t] + p_pv[i, t]
        for i in range(Nwt):
            c_pwrbal[t] = c_pwrbal[t] + p_wt[i, t]
        for i in range(Nbm):
            c_pwrbal[t] = c_pwrbal[t] + p_bm[i, t]
        for i in range(Nl):
            c_pwrbal[t] = c_pwrbal[t] - p_l[i, t]
        for i in range(Ndl):
            c_pwrbal[t] = c_pwrbal[t] - p_dl[i, t]
        for i in range(Nbat):
            c_pwrbal[t] = c_pwrbal[t] - p_chg[i, t] + p_dch[i, t]
        
        c_pwrbal[t] = c_pwrbal[t] - p_imp[t] + p_exp[t]

    # balanço potência -
    shift = Nt
    for i in range(1, Nt):
        # k += 1
        c_pwrbal[t + shift] = - c_pwrbal[t]

    # Construção do vetor de restrições
    c = []
    ceq = [c_bm, c_bat, c_dl, c_ie, c_pwrbal]
    return c, ceq

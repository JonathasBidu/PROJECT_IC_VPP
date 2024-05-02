import numpy as np
from decomp_vetor_v1 import decomp_vetor_v1

'''
    Descricao do script
    script contém as restricções não lineares do modelo da VPP, para uso do ga.

    Parâmetros:
    - x: vetor de variáveis 
    - vpp_data: Dicionário contendo os parametros da VPP. possui os seguintes atributos:
    
        Nt - numero de instantes de simulacao
        Nbm - numero de usinas biomassa
        Ndl - numero de cargas despachaveis
        Nbat - numero de baterias
        Nwt - numero de geradores eolicos
        Npv - numero de usinas solares
        p_l - potencia das cargas, dimensao (Nl*Nt) x  1     
        p_dl - potencia das cargas despachaveis, dimensao (Ndl*Nt) x 1
        p_pv - potencia das UG solares FV, dimensao (Npv*Nt) x
        p_wt - potencia das UG eóliacas, dimensao (Nwt*Nt) x 1
        p_bm_min - pot. minima biomassa, dimensao Nbm x 1
        p_bm_max - pot. maxima biomassa, dimensao Nbm x 1
        p_bm_rup - pot. maxima ramp up biomassa, dimensao Nbm x 1
        p_bm_rdown  - pot. maxima ramp down biomassa, dimensao Nbm x 1
        eta_chg - rendimento carga bateria, dimensao Nbat x 1
        eta_dch - rendimento descarga bateria, dimensao Nbat x 1
        soc_min - SoC minimo bateria, dimensao Nbat x 1
        soc_max - SoC maximo bateria, dimensao Nbat x 1
        p_bat_max  - pot. maxima carga/descarga bateria, dimensao Nbat x 1
        p_dl_min - pot. minima despachavel carga, dimensao Ndl x 1
        p_dl_max - pot. maxima despachavel carga, dimensao Ndl x 1
        tau_pld  - PLD, dimensao Nt x 1
        tau_dist - tarifa distribuidora, dimensao Nt x 1
        tau_dl - compensacao por corte, dimensao Nt x 1
        kappa_pv - custo unitario ger. solar
        kappa_wt - custo unitario ger. eolica
        kappa_bm - custo unitario ger. biomassa
        kappa_bm_start - custo unitario partida ger. biomassa 

    Retorna:
    - Tuple - Uma tupla contendo duas listas de restrições;
        - c: Por ora, uma lista vazia
        - ceq: uma lista que cotém;
            - c_bm:
            - c_bat:
            - c_dl:  
'''

def vpp_constraints_v1(x, vpp_data: dict) -> np.array:

    # Obtenção dos parâmetros individuais
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
    # tau_pld = vpp_data['tau_pld']
    # tau_dist = vpp_data['tau_dist']
    # p_pv = vpp_data['p_pv']
    # p_wt = vpp_data['p_wt']
    # p_l = vpp_data['p_l']
    # tau_dl = vpp_data['tau_dl']
    # kappa_pv = vpp_data['kappa_pv']
    # kappa_wt = vpp_data['kappa_wt']
    # kappa_bm = vpp_data[kappa_b]
    # kappa_bm_start = vpp_data['kappa_bm_start']
    # kappa_bm_start = vpp_data['kappa_bat']

    # Separção das variáveis no vetor solução
    p_bm, p_dl, p_chg, p_dch, soc, u_bm, u_dl, u_chg, u_dch = decomp_vetor_v1(x, Nt, Nbm, Ndl, Nbat)

    # reshape de vetrore em matrizes
    p_bm = p_bm.reshape((Nbm, Nt)) # Reajuste da dimensão da matriz
    p_dl = p_dl.reshape((Ndl, Nt))
    p_chg = p_chg.reshape((Nbat, Nt))
    p_dch = p_dch.reshape((Nbat, Nt))
    soc = soc.reshape((Nbat, Nt))
    u_bm = u_bm.reshape((Nbm, Nt))
    u_dl = u_dl.reshape((Ndl, Nt))
    u_chg = u_chg.reshape((Nbat, Nt))
    u_dch = u_dch.reshape((Nbat, Nt))
    # u_bm = np.float64(u_bm > 0.5).reshape((Nbm, Nt))
    # u_dl = np.float64(u_dl > 0.5).reshape((Ndl, Nt))
    # u_chg = np.float64(u_chg > 0.5).reshape((Nbat, Nt))
    # u_dch = np.float64(u_dch > 0.5).reshape((Nbat, Nt))

    # Restrições da biomassa
    Nbmc = (Nt * Nbm) + (Nt * Nbm) + ((Nt - 1) * Nbm) + ((Nt - 1) * Nbm)
    c_bm = np.zeros(Nbmc)

    k = 0
    # p_bm_max
    for i in range(Nbm):
        for t in range(Nt):
            c_bm[k] = p_bm[i, t] - p_bm_max[i] * u_bm[i, t] # conferido (ok)
            k += 1

    # p_bm_min
    for i in range(Nbm):
        for t in range(Nt):
            c_bm[k] = p_bm_min[i] * u_bm[i, t] - p_bm[i, t] # conferido (ok)
            k += 1  

    # p_bm_rup
    for i in range(Nbm):
        for t in range(1, Nt):
            c_bm[k] =  p_bm[i, t] - p_bm[i, t - 1] - p_bm_rup[i] # conferido (ok)
            k += 1  

    # p_bm_rdown
    for i in range(Nbm):
        for t in range(1, Nt):
            c_bm[k] = p_bm[i, t - 1] - p_bm[i, t] - p_bm_rdown[i] # conferido (ok) verificado com professor
            k += 1

    # Restricoes da bateria
    Nbatc = + ((Nt - 1) * Nbat) + ((Nt - 1) * Nbat) + (Nt*Nbat) + (Nt*Nbat) + (Nt*Nbat)  
    c_bat = np.zeros(Nbatc)
    k = 0
    
    # soc balanço +
    for i in range(Nbat):
        for t in range(1, Nt):
            c_bat[k] = soc[i, t] - soc[i, t - 1] - p_chg[i, t] * eta_chg[i] + p_dch[i, t] / eta_dch[i]
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
            c_bat[k] = p_chg[i, t] - p_bat_max[i] * u_chg[i, t] # conferido (ok)
            k += 1
                
    # limites máximo descarga
    for i in range(Nbat):
        for t in range(Nt):
            c_bat[k] = p_dch[i, t] - p_bat_max[i] * u_dch[i, t] # conferido (ok)
            k += 1
 
    # limites de simultaneidade de carga e descarga
    for i in range(Nbat):
        for t in range(Nt):
            c_bat[k] = u_chg[i, t] + u_dch[i, t] - 1 # conferido (ok)
            k += 1

    # restrições das cargas despachaveis
    Ndlc = (Nt*Ndl) + (Nt*Ndl)
    c_dl = np.zeros(Ndlc)
    k = 0 

    # p_dl_max
    for i in range(Ndl):
        for t in range(Nt):
            c_dl[k] = p_dl[i, t] - p_dl_max[i, t] * u_dl[i, t]
            k += 1

    # p_dl_min
    for i in range(Ndl):
        for t in range(Nt):
            c_dl[k] = p_dl_min[i, t] * u_dl[i, t] - p_dl[i, t] 
            k += 1 
   
    # Construção de restrições:
            
    # Restrições de igualdade 
    c_eq = [] 

    # Restrições de desigualdade
    # c_ineq = c_bm
    c_ineq = np.concatenate((c_bm, c_bat, c_dl))
   
    return c_ineq  
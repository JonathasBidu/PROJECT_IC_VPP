import matplotlib.pyplot as plt
import numpy as np


def vpp_plot(vpp_data: dict)-> None:

    Nt = vpp_data['Nt']
    Nbm = vpp_data['Nbm']
    Ndl = vpp_data['Ndl']
    Npv = vpp_data['Npv']
    Nwt = vpp_data['Nwt']
    Nbat = vpp_data['Nbat']
    t = np.arange(1, Nt + 1)

    p_bm = vpp_data['p_bm']
    p_bm_max = vpp_data['p_bm_max']
    p_bm_min = vpp_data['p_bm_min']


    for i in range(Nbm):

        # Biomassa
        plt.figure(figsize = (10, 4))
        plt.plot(t, np.ones(Nt) * p_bm_min[i], 'b--')
        plt.plot(t, np.ones(Nt) * p_bm_max[i], 'b--')
        plt.plot(t, p_bm[i], 'r')

        title_name = f'Usina de Biomassa {i + 1}'
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência')
        plt.legend(['min', 'max', 'p'])
        plt.xlim(0, Nt)
        plt.xticks(np.arange(0, Nt + 2, 5))
        plt.ylim(p_bm_min[i], p_bm_max[i] + 0.1)
        plt.yticks(np.arange(0, p_bm_max[i] + 0.5, 0.5))
        plt.show()

    # Baterias
    p_dch = vpp_data['p_dch']
    p_chg = vpp_data['p_chg']
    u_dch = vpp_data['u_dch']
    u_chg = vpp_data['u_chg']
    soc = vpp_data['soc']
    soc_min = vpp_data['soc_min']
    soc_max = vpp_data['soc_max']
    p_bat_max = vpp_data['p_bat_max']

    for i in range(Nbat):

        plt.figure(figsize = (10, 4))
        plt.plot(t, p_bat_max[i] * np.ones(Nt), 'b--')
        plt.step(t, p_chg[i,:] * u_chg[i,:], 'r')

        title_name = f'Carga Bateria {i + 1}'
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência')
        plt.xlim(0, Nt+1)
        plt.xticks(np.arange(0, Nt + 2, 5))
        plt.ylim(0, p_bat_max[i] + 0.1)
        plt.yticks(np.arange(0, p_bat_max[i], 0.5))
        plt.show()

        plt.figure(figsize = (10, 4))
        plt.plot(t, p_bat_max[i] * np.ones(Nt), 'b--')
        plt.step(t, p_dch[i,:] * u_dch[i,:], 'r')

        title_name = f'Descarga Bateria {i + 1}'
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência')
        plt.xlim(0, Nt+1)
        plt.xticks(np.arange(0, Nt + 2, 5))
        plt.ylim(0, p_bat_max[i] + 0.1)
        plt.yticks(np.arange(0, p_bat_max[i], 0.5))
        plt.show()

        plt.figure(figsize = (10, 4))
        plt.plot(t, soc_min[i] * np.ones(Nt) , 'b--')
        plt.plot(t, soc_max[i] * np.ones(Nt) , 'b--')
        plt.step(t, soc[i,:], 'r')
        
        title_name = f'Soc Bateria {i + 1}'
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Carga')
        plt.xlim(0, Nt+1)
        plt.xticks(np.arange(0, Nt + 2, 5))
        plt.ylim(soc_min[i] - 0.005, soc_max[i] + 0.005)
        plt.yticks(np.arange(soc_min[i], soc_max[i], 0.2))
        plt.show()

    # Cargas despachaveis        
    p_dl = vpp_data['p_dl']
    p_dl_ref = vpp_data['p_dl_ref']
    p_dl_min = vpp_data['p_dl_min']
    p_dl_max = vpp_data['p_dl_max']

    # upper = np.max(p_dl_max)
    # lower = np.min(p_dl_min)
    # print(f'upper == {upper}')
    # print(f'lower == {lower}')

    for i in range(Ndl):

        plt.figure(figsize = (10, 4))
        plt.plot(t, p_dl_ref[i,:], 'r')
        plt.plot(t, p_dl_min[i,:], 'b--')
        plt.plot(t, p_dl_max[i,:], 'b--')
        plt.plot(t, p_dl[i,:], 'k')

        title_name = f'Cargas despachaveis {i + 1}'
        plt.title(title_name)
        plt.xlabel('Potência')
        plt.ylabel('Carga')
        plt.xlim(0, Nt+1)
        plt.xticks(np.arange(0, Nt + 2, 5))
        plt.show()

    # FV
    p_pv = vpp_data['p_pv']

    for i in range(Npv):

        plt.figure(figsize = (10, 4))
        plt.plot(t, p_pv[i], 'r')

        title_name = f'Usina Solar FV {i + 1}'
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.xlim(0, Nt+1)
        plt.show()

    # Wt
    p_wt = vpp_data['p_wt']

    for i in range(Nwt):

        plt.figure(figsize = (10, 4))
        plt.plot(t, p_wt[i], 'r')

        title_name = f'Usina Eólica {i + 1}'
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.show()

    # Potência Líquida
    p_liq = np.zeros(Nt)
    Nl = vpp_data['Nl']
    p_l = vpp_data['p_l']
    u_dl = vpp_data['u_dl']

    for t in range(Nt):

        for i in range(Npv):
            p_liq[t] += p_pv[i, t]
        for i in range(Nwt):
            p_liq[t] += p_wt[i, t]
        for i in range(Nbm):
            p_liq[t] += p_bm[i, t]
        for i in range(Nl):
            p_liq[t] -= p_l[i, t]
        for i in range(Ndl):
            p_liq[t] -= p_dl[i, t] * u_dl[i, t]
        for i in range(Nbat):
            p_liq[t] -= p_chg[i, t] * u_chg[i, t] + p_dch[i, t] * u_dch[i, t]

    p_exp = np.maximum(0, p_liq)
    p_imp = np.maximum(0, -p_liq)
    t = np.arange(1, Nt + 1)

    # Potência de exportação
    plt.figure(figsize = (10, 4))
    plt.plot(t, p_exp, 'r')

    title_name = f'Exportação de potência'
    plt.title(title_name)
    plt.xlabel('hora')
    plt.ylabel('Potência em MW')
    plt.show()

    # Potência de importação
    plt.figure(figsize = (10, 4))
    plt.plot(t, p_imp, 'r')

    title_name = f'Importação de potência'
    plt.title(title_name)
    plt.xlabel('hora')
    plt.ylabel('Potência em MW')
    plt.show()

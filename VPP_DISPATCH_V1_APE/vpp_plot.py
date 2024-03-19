import numpy as np
import matplotlib.pyplot as plt

def vpp_plot2(vpp_data):

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

    # Biomassa
    for i in range(Nbm):
        plt.figure()
        # print(vpp_data['p_bm_max'][i])
        # print(t, t.shape)
        # print(np.ones(p_bm.shape[1]) * vpp_data['p_bm_max'][i])
        plt.plot(t, np.ones(p_bm.shape[1]) * p_bm_max[i], 'b--')
        plt.plot(t, np.ones(p_bm.shape[1]) * p_bm_min[i], 'b--')
        plt.plot(t, p_bm[i], 'r')

        title_name = f'Usina de Biomassa {i+1}'
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência')
        plt.legend(['max', 'min', 'p'])
        plt.xlim(0, Nt)
        plt.xticks(np.arange(0, Nt+1, 1))
        plt.show()

    # Baterias
    p_dch = vpp_data['p_dch']
    p_chg = vpp_data['p_chg']
    u_dch = vpp_data['u_dch']
    u_chg = vpp_data['u_chg']
    p_bat_max = vpp_data['p_bat_max']

    for i in range(Nbat):
    
        plt.figure()
        plt.plot(t, p_chg[i] * u_chg[i], 'r')
        plt.plot(t, p_dch[i] * u_dch[i], 'k')
        plt.plot(t, np.ones(Nt) * p_bat_max, 'b--')

        title_name = f'Bateria {i+1}'
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Carga/Descarga')
        plt.legend(['carga', 'descarga', 'max'])
        plt.xlim(0, Nt)
        plt.xticks(np.arange(0, Nt+1, 1))
        plt.show()

    soc = vpp_data['soc']
    soc_max = vpp_data['soc_max']
    soc_min = vpp_data['soc_min']
        
    for i in range(Nbat):

        plt.figure()
        plt.plot(t, soc_min[i] * np.ones(Nt), 'b--')
        plt.plot(t, soc_max[i] * np.ones(Nt), 'b--')
        plt.plot(t, soc[i], 'r')

        title_name = f'Soc Bateria {i+1}'
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Carga')
        plt.legend(['min', 'max', 'Soc'])
        plt.xlim(0, Nt)
        plt.xticks(np.arange(0, Nt+1, 1))
        plt.show()
   

    # Cargas despachaveis
    p_dl_ref = vpp_data['p_dl_ref']
    p_dl_min = vpp_data['p_dl_min']
    p_dl_max = vpp_data['p_dl_max']
    p_dl = vpp_data['p_dl']

    for i in range(Ndl):

        plt.figure()
        plt.plot(t, p_dl_ref[i], 'r')
        plt.plot(t, p_dl_min[i], 'b--')
        plt.plot(t, p_dl_max[i], 'b--')
        plt.plot(t, p_dl[i], 'k')

        title_name = f'Cargas despachaveis {i+1}'
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência MW')
        plt.legend(['ref','min', 'max', 'desp.'])
        plt.xlim(0, Nt)
        plt.xticks(np.arange(0, Nt+1, 1))
        plt.show()

    # FV e WT
    p_pv = vpp_data['p_pv']

    for i in range(Npv):

        plt.figure()
        plt.plot(t, p_pv[i], 'r')

        title_name = f'Usina Solar FV {i+1}'
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência MW')
        plt.xlim(0, Nt)
        plt.xticks(np.arange(0, Nt+1, 1))
        plt.show()

    p_wt = vpp_data['p_wt']

    for i in range(Nwt):

        plt.figure()
        plt.plot(t, p_wt[i], 'r')

        title_name = f'Usina Eólica {i+1}'
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência MW')
        plt.xlim(0, Nt)
        plt.xticks(np.arange(0, Nt+1, 1))
        plt.show()
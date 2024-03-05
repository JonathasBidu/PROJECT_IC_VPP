import numpy as np
import matplotlib.pyplot as plt

def vpp_plot2(vpp_data):


    Nt = vpp_data['Nt'] + 1
    Nbm = vpp_data['Nbm']
    t = np.arange(Nt)
    print("Comprimento de t:", len(t))

    # # Biomassa
    # for i in range(Nbm):
    #     plt.figure()
    #     plt.subplot(Nbm, i, i +1)
    #     plt.plot(t, np.full(Nt, vpp_data['p_bm_min'][i]), 'b--',
    #              t, np.full(Nt, vpp_data['p_bm_max'][i]), 'b--',
    #              t, vpp_data['p_bm'][i], 'r')
    #     plt.title(f"Usina biomassa {i+1}")
    #     plt.ylabel('Potencia')
    #     plt.xlabel('hora')
    #     plt.legend(['min', 'max', 'p'])

    for i in range(vpp_data['Nbm']):
        print(f"Comprimento de p_bm_min[{i}]:", len(vpp_data['p_bm_min']))
        print(f"Comprimento de p_bm_max[{i}]:", len(vpp_data['p_bm_max']))
        plt.figure()
        plt.subplot(vpp_data['Nbm'], 1, i+1)
        plt.plot(t, np.full(vpp_data['Nt'], vpp_data['p_bm_min'][i]), 'b--',
                 t, np.full(vpp_data['Nt'], vpp_data['p_bm_max'][i]), 'b--',
                 t, vpp_data['p_bm'][i], 'r')
        plt.title(f"Usina biomassa {i+1}")
        plt.ylabel('Potencia')
        plt.xlabel('hora')
        plt.legend(['min', 'max', 'p'])
    
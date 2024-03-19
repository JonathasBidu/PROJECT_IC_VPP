import numpy as np
import matplotlib.pyplot as plt

def vpp_plot2(vpp_data):

    Nt = vpp_data['Nt']
    Nbm = vpp_data['Nbm']
    t = np.arange(1, Nt + 1)

    p_bm = vpp_data['p_bm']

    # Biomassa
    for i in range(Nbm):
        plt.figure()
        print(vpp_data['p_bm_max'][i])
        print(t, t.shape)
        print(np.ones(p_bm.shape[1]) * vpp_data['p_bm_max'][i])
        plt.plot(t, np.ones(p_bm.shape[1]) * vpp_data['p_bm_max'][i], 'g--')
        plt.plot(t, np.ones(p_bm.shape[1]) * vpp_data['p_bm_min'][i], 'b--')
        plt.plot(t, p_bm[i], 'r')

        title_name = f'Usina de Biomassa {i+1}'
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência')
        plt.legend(['max', 'min', 'p'])
        plt.xlim(0, Nt)
        plt.xticks(np.arange(0, Nt+1, 1))

        plt.show()
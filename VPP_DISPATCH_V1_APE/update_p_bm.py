import numpy as np
''' Essa função visa atualizar limites máximos e mínimos das potências das Usinas de biomassa através de uma curva de duração das cargas,por fim, por questões de visualização um gráfico é exibido na tela do usuário'''

def update(Nt, p_l, p_dl_ref, p_pv, p_wt):

    import matplotlib.pyplot as plt
    
    # data = vpp_data()

    # Cargas despachaveis e não despachaveis
    x_1 = np.concatenate((p_l, p_dl_ref), axis = 0) # empilhando as duas matrizes e transformando_as em uma matriz ((Nl+Ndl5)=5, Nt=24)
    x_2 = np.concatenate((p_pv, p_wt), axis = 0)
    x_1 = np.sum(x_1, axis = 0) # Somando as colunas e tornando a matriz acima em uma nova matriz (1, 24)
    x_2 = np.sum(x_2, axis = 0)
    d_1 = np.zeros(Nt) # Nl = 3, Nt = 24, Ndl = 2, criando um vetor de zeros (24,)
    d_2 = np.zeros(Nt) # Npv = 3, Nt = 24, Nwt = 3

    # iniciando uma variável contadora
    pos = 0
    for xi in x_1:
        d_1[pos] = np.sum(x_1 >= xi)
        pos += 1

    # cargas das usinas

    pos = 0
    for xi in x_2:
        d_2[pos] = np.sum(x_2 >= xi)
        pos += 1

    idx_1 = np.argsort(d_1)
    d_ord_1 = np.sort(d_1)
    idx_2 = np.argsort(d_2)
    d_ord_2 = np.sort(d_2)

    r_up = max(x_1) #+ max(x_1) * 0.2
    r_down = min(x_1) #- min(x_1) * 0.2
    mod_x_1 = (max(x_1) - min(x_1)) / 2 + min(x_1)
    # print(f'{r_up:.2f}')
    # print(f'{r_down:.2f}')

    plt.figure(figsize = (10, 5))
    plt.plot(d_ord_1, x_1[idx_1])
    plt.plot(d_ord_2, x_2[idx_2])
    plt.axhline(r_up, color = 'r', linestyle = '-.')
    plt.axhline(r_down, color = 'm', linestyle = '-.')
    plt.axhline(mod_x_1, color = 'k', linestyle = '--')
    plt.title('Gráfico de duração de cargas')
    plt.xlabel('duração')
    plt.ylabel('Cargas')
    plt.legend(['desp', 'ger','p_bm_max', 'p_bm_min', 'módulo'])
    plt.tight_layout()
    # plt.grid(True)
    plt.show()

    return r_up, r_down

# Exemplo de uso

# from carrega_projecoes import carrega_projecoes
# from vppdata1_module import vpp_data

# data = vpp_data()

# Nt = 24  # Número de pontos de dados na série temporal
# Nl = data['Nl']   # Número de cargas
# Ndl = data['Ndl'] # Número de cargas de referência
# Npv = data['Npv']  # Número de sistemas fotovoltaicos
# Nwt = data['Nwt']  # Número de sistemas de geração eólica

# p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = carrega_projecoes(Nt, Nl, Ndl, Npv, Nwt)

# a, b = update(Nt, p_l, p_dl_max, p_pv, p_wt)

# print(f'P_bm_max == {a:.2f}')
# print(f'P_bm_min == {b:.2f}')
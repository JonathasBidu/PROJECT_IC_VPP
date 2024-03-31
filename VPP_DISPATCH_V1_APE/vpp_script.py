import numpy as np
from vpp_plot import vpp_plot
from vpp_create import vpp_create
from carrega_projecoes import carrega_projecoes
from vpp_dispatch_v1_module import vpp_dispatch_v1

#  Descricao do Script
# Este script realiza a leitura dos parâmetros da vpp, as projeções de
# carga, geração e preço, e os instantes a frente para a programação da 
# vpp. Ao final desse processo, o script realiza a programação da vpp.

# Carregamento da vpp
vpp_data = vpp_create()

# Número de instantes a serem programados
while True:
    Nt = input('No. de horas a frente: ')
    print(' ')
    if Nt.isnumeric() and int(Nt) > 0:
        vpp_data['Nt'] = int(Nt)
        break
    else:
        print('Erro: informar um número inteiro e não-negativo')

Nt = int(vpp_data['Nt'])
Nl = int(vpp_data['Nl'])
Ndl = int(vpp_data['Ndl'])
Npv = int(vpp_data['Npv'])
Nwt = int(vpp_data['Nwt'])
Nbm = int(vpp_data['Nbm'])
Nbat = int(vpp_data['Nbat'])

# Carregamento das projeções de cargas, geração FV/Eólica e PLD
vpp_data['p_l'], vpp_data['p_pv'], vpp_data['p_wt'], vpp_data['p_dl_ref'], vpp_data['p_dl_min'], vpp_data['p_dl_max'], vpp_data['tau_pld'], vpp_data['tau_dist'], vpp_data['tau_dl'] = carrega_projecoes(Nt, Nl, Ndl , Npv , Nwt)

results, x = vpp_dispatch_v1(vpp_data)
vpp_data['p_bm'] = results['p_bm']
vpp_data['p_dl'] = results['p_dl']
vpp_data['p_chg'] = results['p_chg']
vpp_data['p_dch'] = results['p_dch']
vpp_data['soc'] = results['soc']
vpp_data['u_bm'] = results['u_bm'] 
vpp_data['u_dl'] = results['u_dl'] 
vpp_data['u_chg'] = results['u_chg']
vpp_data['u_dch'] = results['u_dch']

vpp_plot(vpp_data)

soma_p_bm = np.sum(vpp_data['p_bm'])
soma_p_pv = np.sum(vpp_data['p_pv'])
soma_p_wt = np.sum(vpp_data['p_wt'])
soma_p_dl = np.sum(vpp_data['p_dl'])
soma_p_l = np.sum(vpp_data['p_l'])

soma_ger = soma_p_bm + soma_p_pv + soma_p_wt
soma_carga = soma_p_dl + soma_p_l

print('')
print(f'A soma das cargas dos geradores é {soma_ger}')
print(f'A soma das cargas é {soma_carga}')
if soma_ger > soma_carga:
    print(f'A soma dos geradores é maior do que a soma das cargas\n')
else:
    print(f'A soma dos geradores NÃO é maior do que a soma das cargas\n')

from vpp_plot2 import vpp_plot2
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

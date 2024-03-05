import numpy as np
from pathlib import Path
from vppdata1_module import vpp_data as vpp # teste

# Esta função carrega os dados característicos de uma VPP cujo os dados sao:

#     Nt - número de instantes de simulação
#     Ndl - número de cargas despacháveis
#     Nbm - número de usinas biomassa
#     Nl - número de cargas não despacháveis
#     Nbat - número de baterias
#     Nwt - número de geradores eólicos
#     Npv - número de usinas solares
#     p_l - potência das cargas, dimensão ((Nl*Nt), 1)
#     p_dl - potência das cargas despachaveis, dimensão ((Ndl*Nt), 1)
#     p_pv - potência das UG solares FV, dimensão ((Npv*Nt), 1)
#     p_wt - potência das UG eólicas, dimensão ((Nwt*Nt), 1)
#     p_bm_min - pot. mínima biomassa, dimensao (Nbm, 1)
#     p_bm_max - pot. máxima biomassa, dimensão (Nbm, 1)
#     p_bm_rup - pot. máxima ramp up biomassa, dimensão (Nbm, 1)
#     p_bm_rdown  - pot. máxima ramp down biomassa, dimensão (Nbm, 1)
#     eta_chg - rendimento carga bateria, dimensão (Nbat, 1)
#     eta_dch - rendimento descarga bateria, dimensão (Nbat, 1)
#     soc_min - SoC mínimo bateria, dimensão (Nbat, 1)
#     soc_max - SoC máximo bateria, dimensão (Nbat, 1)
#     p_bat_max  - pot. máxima carga/descarga bateria, dimensão (Nbat, 1)
#     p_dl_min - pot. mínima despachável carga, dimensão (Ndl, 1)
#     p_dl_max - pot. máxima despachável carga, dimensão (Ndl, 1)
#     tau_pld  - PLD, dimensão (Nt, 1)
#     tau_dist - tarifa distribuidora, dimensão (Nt, 1)
#     tau_dl - compensacao por corte, dimensão (Nt, 1)
#     kappa_pv - custo unitário ger. solar
#     kappa_wt - custo unitário ger. eólica
#     kappa_bm - custo unitário ger. biomassa
#     kappa_bm_start - custo unitário partida ger. biomassa
#     kappa_bat - custo unitário bateria
#  argumentos de entrada
# filename - Arquivo de entrada contendo os atributos da VPP(opcional)
#  argumentos de saída:
# vpp_data - estrutura de dicionário contendo os atributos da VPP





def vpp_create() -> dict:
    
    # Caminho para o arquivo que contém os dados da vpp_data
    file = Path(__file__).parent / 'vppdata1_module.py'       
    if file.is_file(): # Verificando se o caminho existe
        # Caminho para o CSV que contém os atirbutos do VPP
        # path = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\\PROJETO_VPP\\VPP_DISPATCH_V1_APE\\VPPDATA1.csv"
        # # Obtendo os atributos da VPP
        # vpp_data_df = pd.read_csv(path, sep = ';') # vpp em formato de DataFarme
        # keys = vpp_data_df.iloc[: , 1]
        # values = vpp_data_df.iloc[: , 2]
        # vpp_data = dict(zip(vpp_data_df.iloc[ : , 1],i for i in vpp_data_df.iloc[ : , 2])) # vpp em forma de dicionário

        print("VPP carregada com sucesso do arquivo \n")
        vpp_data = vpp()

    else:
        vpp_data = {}

        # UTE Biomassa
        print("Parâmetros das UTE Biomassa \n")
        while True:
            Nbm = input('No. de UTE Biomassa: ')
            try:
                Nbm = int(Nbm)
                if Nbm > 0:
                    vpp_data['Nbm'] = int(Nbm)
                    break
                else:
                    print("Informar um número inteiro e não negativo")
            except ValueError:
                 print("Informe um valor numérico válido")
    
    
        if vpp_data['Nbm'] > 0:
            vpp_data['p_bm_min'] = np.zeros(vpp_data['Nbm'])
            vpp_data['p_bm_max'] = np.zeros(vpp_data['Nbm'])
            vpp_data['p_bm_rup'] = np.zeros(vpp_data['Nbm'])
            vpp_data['p_bm_rdown'] = np.zeros(vpp_data['Nbm'])
            vpp_data['kappa_bm'] = np.zeros(vpp_data['Nbm'])
            vpp_data['kappa_bm_start'] = np.zeros(vpp_data['Nbm'])
    
            # Inserindo as potências mínimas das usinas
            for i in range(vpp_data['Nbm']):                
                while True:
                    pot_min = input(f'Potência mínima da usina {i + 1} em (kW): ')
                    try:
                        pot_min = float(pot_min)
                        if pot_min >= 0:
                            vpp_data['p_bm_min'][i] = pot_min
                            break
                        else:
                            print("Informar um número não negativo")
                    except ValueError:
                        print("Informe um valor numérico válido")

            # Inserindo as potências máximas das usinas
            for i in range(vpp_data['Nbm']):
                while True:
                    pot_max = input(f'Potência máxima da usina {i + 1} em (kW): ')
                    try:
                        pot_max = float(pot_max)
                        if pot_max >= 0:
                            vpp_data['p_bm_max'][i] = pot_max
                            break
                        else:
                            print("Erro: geradores devem ter potência não negativa")
                    except ValueError:
                        print("Informe um valor numérico válido")
    
            # Inserindo Ramp up das usinas
            for i in range(vpp_data['Nbm']):
                while True:
                    rup = input(f'Ramp up da usina {i + 1} em (kW): ')
                    try:
                        rup = float(rup)
                        if rup >= 0:
                            vpp_data['p_bm_rup'][i] = rup
                            break
                        else:
                            print("Erro: geradores devem ter Ramp up não negativo")
                    except ValueError:
                            print("Informe um valor numérico válido")
    
            # Inserindo Ramp down das usinas
            for i in range(vpp_data['Nbm']):
                while True:
                    rdown = input(f'Ramp down da usina {i + 1} em (kW): ')
                    try:
                        rdown = float(rdown)
                        if rdown >= 0:
                            vpp_data['p_bm_rdown'][i] = rdown
                            break
                        else:
                            print("Erro: especificar ramp down de todas as usinas")
                    except ValueError:
                        print("Informe um valor numérico válido")
            
            # Inserindo os custo das usinas 
            for i in range(vpp_data['Nbm']):
                while True:
                    kappa_bm = input(f'Custo de geração da usina {i + 1} em ($/kWh): ')
                    try:
                        kappa_bm = float(kappa_bm)
                        if kappa_bm >= 0:
                            vpp_data['kappa_bm'][i] = kappa_bm
                            break
                        else:
                            print("Erro: especificar custo de geração de todas as usinas")
                    except ValueError:
                        print("Informe um valor numérico válido")
    
            # Inserindo os custo Start-up das usinas 
            for i in range(vpp_data['Nbm']):
                while True:
                    kappa_bm_start = input(f'Custo de start-up da usina {i + 1} em ($/kWh) :')
                    try:
                        kappa_bm_start = float(kappa_bm_start)
                        if kappa_bm_start >= 0:
                            vpp_data['kappa_bm_start'][i] = kappa_bm_start
                            break
                        else:
                            print("Erro: especificar custo start-up de todas as usinas")
                    except ValueError:
                        print("Informe um valor numérico válido")
                    
                    
        # Usinas FV
        print('\n Paramêtros das Usinas FV \n')
        while True:
            Npv = input('No. de Usinas FV: ')
            try:
                Npv = int(Npv)
                if Npv > 0:
                    vpp_data['Npv'] = int(Npv)
                    break
                else:
                    print("Informar um número inteiro e não negativo")
            except ValueError:
                print("Informe um valor numérico válido")
    
        if vpp_data['Npv'] > 0:
            vpp_data['kappa_pv'] = np.zeros(vpp_data['Npv'])
    
            for i in range(vpp_data['Npv']):
                while True:
                    kappa_pv = input(f'Custo de geração da usina {i + 1} ($/kWh): ')
                    try:
                        kappa_pv = float(kappa_pv)
                        if kappa_pv >= 0:
                            vpp_data['kappa_pv'][i] = kappa_pv
                            break
                        else:
                            print('Erro: especificar custo de geração de todas as usinas')
                    except ValueError: 
                        print("Informe um valor numérico válido")
                        
        # Usinas Eólicas
        print('\n Paramêtros das Usinas Eólica \n')
        while True:
            Nwt = input('No. de Usinas Eólica: ')
            try:
                Nwt = int(Nwt)
                if Nwt > 0:
                    vpp_data['Nwt'] = int(Nwt)
                    break
                else:
                    print("Informar um número inteiro e não negativo")
            except ValueError:
                print("Informe um valor numérico válido")
    
        if vpp_data['Nwt'] > 0:
            vpp_data['kappa_wt'] = np.zeros(vpp_data['Nwt'])
    
            # Obtendo os custos de geração das usinas Eólicas
            for i in range(vpp_data['Nwt']):
                while True:
                    kappa_wt = input(f'Custo de geração das usinas {i + 1} ($/kWh): ')
                    try:
                        kappa_wt = float(kappa_wt)
                        if kappa_wt >= 0:
                            vpp_data['kappa_wt'][i] = kappa_wt
                            break
                        else:
                            print('Erro: especificar custo de geração de todas as usinas')
                    except ValueError:
                        print('Informe um valor numérico válido')
    
        # Sistemas de Armazenamento Elétrico
        print('\n Parâmetros dos Sistemas de Armazenamento de Energia \n')
        while True:
            Nbat = input('No. de Sistemas de Armazenamento de Energia: ')
            try:
                Nbat = int(Nbat)
                if Nbat > 0:
                    vpp_data['Nbat'] = int(Nbat)
                    break
                else:
                    print("Erro: informar um inteiro não-negativo")
            except ValueError:
                print("Informe um valor numérico válido")
    
        if vpp_data['Nbat'] > 0:
            vpp_data['eta_chg'] = np.zeros(vpp_data['Nbat'])
            vpp_data['eta_dch'] = np.zeros(vpp_data['Nbat'])
            vpp_data['soc_min'] = np.zeros(vpp_data['Nbat'])
            vpp_data['soc_max'] = np.zeros(vpp_data['Nbat'])
            vpp_data['p_bat_max'] = np.zeros(vpp_data['Nbat'])
            vpp_data['kappa_bat'] = np.zeros(vpp_data['Nbat'])
    
    
            # Obtendo o Rendimento na fase de carga
            for i in range(vpp_data['Nbat']):
                while True:
                    eta_chg = input('Rendimento na fase de carga: ')
                    try:
                        eta_chg = float(eta_chg)
                        if eta_chg >= 0:
                            vpp_data['eta_chg'][i] = eta_chg
                            break
                        else:
                            print('Erro: indicar rend. na carga de todos os armazenadores')
                    except ValueError:
                        print('Informe um valor numérico válido')
                    
            # Obtendo o Rendimento na fase de descarga
            for i in range(vpp_data['Nbat']):
                while True:
                    eta_dch = input('Rendimento na fase de carga: ')
                    try:
                        eta_dch = float(eta_dch)
                        if eta_dch >= 0:
                            vpp_data['eta_dch'][i] = eta_dch
                            break
                        else:
                            print('Erro: indicar rend. na descarga de todos os armazenadores')
                    except ValueError:
                        print('Informe um valor numérico válido')
    
            # Obtendo o Estado mínimo de carga
            for i in range(vpp_data['Nbat']):
                while True:
                    soc_min = input('Estado de carga mínima dos armazenadores (kWh): ')
                    try:
                        soc_min = float(soc_min)
                        if soc_min >= 0 :
                            vpp_data['soc_min'][i] = soc_min
                            break
                        else:
                            print('Erro: indicar est. de carga de todos os armazenadores')
                    except ValueError:
                        print('Informe um valor numérico válido')
        
            # Obtendo o Estado máximo de carga
            for i in range(vpp_data['Nbat']):
                while True:
                    soc_max = input('Estado de carga máximo dos armazenadores (kWh): ')
                    try:
                        soc_max = float(soc_max)
                        if soc_max >= 0 :
                            vpp_data['soc_max'][i] = soc_max
                            break
                        else:
                            print('Erro: indicar est. de carga de todos os armazenadores')
                    except ValueError:
                        print('Informe um valor numérico válido')
    
            # Obtendo a potência máxima dos armazenadores
            for i in range(vpp_data['Nbat']):
                while True:
                    p_bat_max = input('Potência máxima dos armazenadores(kW): ')
                    try:
                        p_bat_max = float(p_bat_max)
                        if p_bat_max >= 0 :
                            vpp_data['p_bat_max'][i] = p_bat_max
                            break
                        else:
                            print('Erro: indicar potência max. de todos os armazenadores')
                    except ValueError:
                        print('Informe um valor numérico válido')
                
            # Obtendo o custo de armazenamento
            for i in range(vpp_data['Nbat']):
                while True:
                    kappa_bat = input('Custo de armazenamento($/kWh): ')
                    try:
                        kappa_bat = float(kappa_bat)
                        if kappa_bat >= 0 :
                            vpp_data['kappa_bat'][i] = kappa_bat
                            break
                        else:
                            print('Erro: especificar custo de armaz. de todas os armazenadores')
                    except ValueError:
                        print('Informe um valor numérico válido')
                
    
        # Cargas Despacháveis
        print('\n Parâmetros das Cargas Despacháveis \n')
        while True:
            Ndl = input('No. de Cargas Despachaveis: ')
            try:
                Ndl = int(Ndl)
                if Ndl > 0:
                    vpp_data['Ndl'] = int(Ndl)
                    break
                else:
                    print("Erro: informar um inteiro não-negativo")
            except ValueError:
                print("Informe um valor numérico válido")
            
        if vpp_data['Ndl'] > 0:
            vpp_data['p_dl_min'] = np.zeros(vpp_data['Ndl'])
            vpp_data['p_dl_max'] = np.zeros(vpp_data['Ndl'])
            vpp_data['tau_dl'] = np.zeros(vpp_data['Ndl'])
    
            # Obtendo a potência mínima das cargas despacháveis
            for i in range(vpp_data['Ndl']):
                while True:
                    p_dl_min = input('Potência mínima das cargas despacháveis (kW):')
                    try:
                        p_dl_min = float(p_dl_min)
                        if p_dl_min >= 0:
                            vpp_data['p_dl_min'] = p_dl_min
                            break
                        else:
                            print('Erro: especificar a potência mínima das cargas desp.')
                    except ValueError:
                        print('Informe um valor numérico válido')
    
            # Obtendo a potência máxima das cargas despacháveis
            for i in range(vpp_data['Ndl']):
                while True:
                    p_dl_max = input('Potência máxima das cargas despacháveis (kW):')
                    try:
                        p_dl_max = float(p_dl_max)
                        if p_dl_max >= 0:
                            vpp_data['p_dl_max'] = p_dl_max
                            break
                        else:
                            print('Erro: especificar a potência máxima das cargas desp.')
                    except ValueError:
                        print('Informe um valor numérico válido')
                            
            # Obtendo a compensação das cargas despacháveis
            for i in range(vpp_data['Ndl']):
                while True:
                    tau_dl = input('Compensacao cargas despachaveis ($/kWh):')
                    try:
                        tau_dl = float(tau_dl)
                        if tau_dl >= 0:
                            vpp_data['tau_dl'] = tau_dl
                            break
                        else:
                            print('Erro: especificar compensação de todas as cargas desp.')
                    except ValueError:
                        print('Informe um valor numérico válido')
                            
        # Preços distribuidora
        print('\n Tarifa distribuidora \n')
        while True:
            tau_dist = input('Preço Distribuidora($/kWh): ')
            try:
                tau_dist = float(tau_dist)
                if tau_dist > 0:
                    vpp_data['tau_dist'] = float(tau_dist)
                    break
                else:
                    print("Erro: informar um inteiro não-negativo")
            except ValueError:
                print("Informe um valor numérico válido")
        
    # Parâmetros da VPP
    # p_bm_min = vpp_data['p_bm_min']
    # p_bm_max = vpp_data['p_bm_max']
    # p_bm_rup = vpp_data['p_bm_rup']
    # p_bm_rdown = vpp_data['p_bm_rdown']
    
    # eta_chg = vpp_data['eta_chg']
    # eta_dch = vpp_data['eta_dch']
    # soc_min = vpp_data['soc_min']
    # soc_max = vpp_data['soc_max']
    # p_bat_max = vpp_data['p_bat_max']
    
    # p_dl_min = vpp_data['p_dl_min']
    # p_dl_max = vpp_data['p_dl_max']
    # tau_dl = vpp_data['tau_dl']

    # tau_pld = vpp_data['tau_pld']
    # tau_dist = vpp_data['tau_dist']
    
    # kappa_bat = vpp_data[kappa_bat]
    # kappa_pv = vpp_data[kappa_pv]
    # kappa_wt = vpp_data[kappa_wt]
    # kappa_bm = vpp_data[kappa_bm]
    # kappa_bm_start = vpp_data[kappa_bm_start]
                
    # Obtenção dos parâmetros individuais
    # vpp_data['Nt'] = None

    # Obtendo o Número de cargas despacháveis
    # while True:
    #     Ndl = input('No. de Cargas Despacháveis: ')
    #     if Ndl.isnumeric() and int(Ndl) > 0:
    #         vpp_data['Ndl'] = int(Ndl)
    #         break
    #     else:
    #         print('Erro: informar um inteiro não-negativo')

    # # Obtendo o Número de baterias
    # while True:
    #     Nbat = input('No. de baterias: ')
    #     if Nbat.isnumeric() and int(Nbat) > 0:
    #         vpp_data['Nbat'] = int(Nbat)
    #         break
    #     else:
    #         print('Erro: informar um inteiro não-negativo')
    
    # # Obtendo o Número de Usinas FV
    # while True:
    #     Npv = input('No. de Usinas FV: ')
    #     if Npv.isnumeric() and int(Npv) > 0:
    #         vpp_data['Npv'] = int(Npv)
    #         break
    #     else:
    #         print('Erro: informar um inteiro não-negativo')
            
    # # Obtendo o Número de Usinas Eólicas
    # while True:
    #     Nwt = input('No. de Usinas FV: ')
    #     if Nwt.isnumeric() and int(Nwt) > 0:
    #         vpp_data['Nwt'] = int(Nwt)
    #         break
    #     else:
    #         print('Erro: informar um inteiro não-negativo')

   
    return vpp_data    

# v = vpp_create()
# print(v)
# size = len(v)
# keys = list(v.keys())
# values = list(v.values())
# for i in range(size):
#     print(keys[i],' = ', values[i])
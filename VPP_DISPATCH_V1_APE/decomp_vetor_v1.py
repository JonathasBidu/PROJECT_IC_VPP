import numpy as np
"""
    Esta função decompõe o vetor de variáveis de controle em suas componentes constituintes.

    Parâmetros:
        - x: Vetor de entrada de variáveis de controle que possui a forma x = [xr, xi]
            - xr: vetor de variáveis reais, que por sua vez tem forma xr = [p_bm, p_dl, p_chg, p_dch, soc]
                Em cada subvetor, as potências são arranjadas por instante e por usina. Por exemplo, se Nt = 3 e Nbm = 2 entao: 
                p_bm = [p_bm_1_1, p_bm_1_2, p_bm_1_3, p_bm_2_1, p_bm_2_2, p_bm_2_3] onde p_bm_i_j representa a potencia da UTE Biomassa i no instante(hora) j.

            - xi: vetor de variáveis inteiras, que possuí a forma x = [u_bm, u_dl, u_chg, u_dch]
                Em cada subvetor, as potências são arranjadas por instante e por usina. Por exemplo, se Nt = 3 e Nbm = 2 entao: 
                u_bm = [u_bm_1_1, u_bm_1_2, u_bm_1_3, u_bm_2_1, u_bm_2_2, u_bm_2_3] onde u_bm_i_j representa o status da UTE Biomassa i no instante(hora) j.

        - Nt: Número de instantes de tempo
        - Nbm: Número de unidades UTEs (biomassa)
        - Ndl: Número de cargas despacháveis
        - Nbat: Número de baterias

    Retorna:
        - p_bm: Vetor de potência das UTEs de biomassa, forma (Nbm * Nt, 1)
        - p_dl: Vetor de potência da carga despachável, forma (Ndl * Nt, 1)
        - p_chg: Vetor de potência de carga da bateria, forma (Nbat * Nt, 1)
        - p_dch: Vetor de potência de descarga da bateria, forma (Nbat * Nt, 1)
        - soc: Vetor de estado de carga da bateria, forma (Nbat * Nt, 1)
        - u_bm: Vetor de status da unidade de biomassa, forma (Nbm * Nt, 1)
        - u_dl: Vetor de status da carga despachável, forma (Ndl * Nt, 1)
        - u_chg: Vetor de status de carga da bateria, forma (Nbat * Nt, 1)
        - u_dch: Vetor de status de descarga da bateria, forma (Nbat * Nt, 1)
"""

def decomp_vetor_v1(x, Nt: int, Nbm: int, Ndl: int, Nbat: int)-> tuple:

    # separacao entre xr e xi
    Nr = (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt)
    Ni = (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt)
  
    inicio = 0
    fim = Nr
    xr = np.array(x[inicio: fim])
    inicio = fim
    fim = fim + Ni
    xi = np.array(x[inicio: fim])

    # obtenção de p_bm
    inicio = 0
    fim = (Nbm * Nt)
    p_bm = xr[inicio: fim]

    # obtenção de p_dl
    inicio = fim
    fim = fim + (Ndl * Nt)
    p_dl = xr[inicio: fim]

    # obtenção de p_chg
    inicio = fim
    fim = fim + (Nbat * Nt)
    p_chg = xr[inicio: fim]

    # obtenção de p_dch
    inicio = fim
    fim = fim + (Nbat * Nt)
    p_dch = xr[inicio: fim]

    # obtenção de soc
    inicio = fim
    fim = fim + (Nbat * Nt)
    soc = xr[inicio: fim]

    # obtenção de u_bm
    inicio =  0
    fim = (Nbm * Nt)
    u_bm = xi[inicio: fim]

    # obtenção de u_dl
    inicio = fim
    fim = fim + (Ndl * Nt)
    u_dl = xi[inicio: fim]

    # obtenção de u_chg
    inicio = fim 
    fim = fim + (Nbat * Nt)
    u_chg = xi[inicio:fim]

    # obtenção de u_dch
    inicio = fim
    fim = fim + (Nbat * Nt) + 1
    u_dch = (xi[inicio: fim])

    u_bm = np.float64(u_bm > 0)
    u_dl = np.float64(u_dl > 0)
    u_chg = np.float64(u_chg > 0)
    u_dch = np.float64(u_dch > 0)

    return p_bm, p_dl, p_chg, p_dch, soc, u_bm, u_dl, u_chg, u_dch


# Array de teste:
# Nt = 2 # Número de instantes de tempo a frente
# Nbm = 2 # Número de usinas de biomassa
# Ndl = 3 # Número de cargas despacháveis
# Nbat = 4 # Número de bateria
# Nr = Nt + Nt + (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt)
# Ni = Nt + Nt + (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt)

# Nr = (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt)
# Ni = (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt)
# # print(Nr)
# # print(Ni)
# x = np.array(range(0, Nr + Ni))
# # print(f'O tamnho de x é {len(x)}')
# p_bm, p_dl, p_chg, p_dch, soc, u_bm, u_dl, u_chg, u_dch = decomp_vetor_v1(x, Nt, Nbm, Ndl, Nbat)

# xr = np.concatenate((p_bm, p_dl, p_chg, p_dch, soc, u_bm, u_dl, u_chg, u_dch))
# print(xr, f' o tipo é {type(xr)} e o  seu shape é {xr.shape}','\n')
# print(p_bm, f' o tipo de p_bm é {type(p_bm)} e o  seu shape é {p_bm.shape}','\n')
# print(p_dl, f' o tipo é p_dl{type(p_dl)} e o  seu shape é {p_dl.shape}','\n')
# print(p_chg, f' o tipo é p_chg{type(p_chg)} e o  seu shape é {p_chg.shape}','\n')
# print(p_dch, f' o tipo é p_dch{type(p_dch)} e o  seu shape é {p_dch.shape}','\n')
# print(soc, f' o tipo é soc{type(soc)} e o  seu shape é {soc.shape}','\n')
# print(u_bm, f' o tipo é u_bm{type(u_bm)} e o  seu shape é {u_bm.shape}','\n')
# print(u_dl, f' o tipo é u_dl{type(u_dl)} e o  seu shape é {u_dl.shape}','\n')
# print(u_chg, f' o tipo é u_chg{type(u_chg)} e o  seu shape é {u_chg.shape}','\n')
# print(u_dch, f' o tipo é u_dch{type(u_dch)} e o  seu shape é {u_dch.shape}','\n')

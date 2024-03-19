import numpy as np
from vpp_func_v1 import vpp_func_v1
from vpp_constraints_v1 import vpp_constraints_v1
from get_vpplimits import get_vpplimits_v1
from decomp_vetor_v1 import decomp_vetor_v1
from pymoo.core.problem import ElementwiseProblem, Problem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.algorithms.soo.nonconvex.pattern import PatternSearch
from pymoo.optimize import minimize

from pymoo.config import Config
Config.warnings['not_compiled'] = False

""" Descrição da função:
    Esta função realiza o despacho de uma VPP utilizando um algoritmo genético com base em cenários de geração FV, Eólica e de Consumo, a VPP busca definir a melhor composição de geração biomassa, armazenamento e cargas despacháveis que maximiza o retorno financeiro.

    Parâmetros:
        - vpp_data: estrutura de dicionário contendo os dados de geradores, cargas e armazenadores da VPP.

    Retorna:
        - Lucro: Lucro obtido no despacho da usina
        - p_exp: vetor de potência exportadas, dimensão (Nt, 1)
        - p_imp: vetor de potência importada, dimensão (Nt, 1)
        - p_bm: vetor de potência das UTEs biomassa, dimensão ((Nbm * Nt), 1)
        - p_dl: vetor de potência das cargas despacháveis, dimensão ((Ndl * Nt), 1)
        - p_chg: vetor de potência de carga das baterias, dimensão ((Nbat * Nt), 1)
        - p_dch: vetor de pot. de descarga das bateria, dimensão ((Nbat * Nt), 1)
        - soc: vetor de status de carga das baterias, dimensão ((Nbat * Nt), 1)
        - u_exp: vetor de status de potência exportadas, dimensão (Nt, 1)
        - u_imp: vetor de status de potência importada, dimensão (Nt, 1)
        - u_bm: vetor de status das UTEs biomassa, dimensão ((Nbm * Nt), 1)
        - u_dl: vetor de status das cargas despacháveis, dimensão ((Ndl * Nt), 1)
        - u_chg: vetor de status de carga das baterias, dimensão ((Nbat * Nt), 1)
        - u_dch: vetor de status de descarga das bateria, dimensão ((Nbat * Nt), 1)
"""

# Otimização utilizando ga
def vpp_dispatch_v1(vpp_data):

    Nt = vpp_data['Nt']
    Nbm = vpp_data['Nbm']
    Ndl = vpp_data['Ndl']
    Nbat = vpp_data['Nbat']
       
    # Definição das variáveis inteiras e do número de variáveis
    Nr = (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt)
    Ni = (Nbm * Nt) + (Ndl * Nt) + (Nbat * Nt) + (Nbat * Nt)
    
    # Número de variáveis
    nvars = Nr + Ni
    intcon = np.arange(Nr + 1, nvars + 1)

    # Obtendo a quantidade de inequações
    Nbmc = (Nt * Nbm) + (Nt * Nbm) + ((Nt - 1) * Nbm) + ((Nt - 1) * Nbm)                # Quantidade de restrições das UTEs de biomassa
    Nbatc = ((Nt - 1) * Nbat) + (Nt*Nbat) + (Nt*Nbat) + (Nt*Nbat) + ((Nt - 1) * Nbat)   # Quantidade de restrições das baterias
    Ndlc = (Nt*Ndl) + (Nt*Ndl)                                                          # Quantidade de restrições das cargas despachaveis
    n_constr_ieq = Nbmc + Ndlc + Nbatc                                                  # Quantidade total de restrições

    class MyProblem(ElementwiseProblem):

        def __init__(self, vpp_data, **kwargs):
            super().__init__(vpp_data, **kwargs)
            self.data = vpp_data

        def _evaluate(self, x, out, *args, **kwargs):

            out['F'] = np.array([ -vpp_func_v1(x, self.data)])
            out['G'] = vpp_constraints_v1(x, self.data)
            
    lb, ub = get_vpplimits_v1(vpp_data)
 
    problem = MyProblem(vpp_data,
                        n_var = nvars,
                        n_obj = 1,
                        n_ieq_constr = n_constr_ieq,
                        xl = lb,
                        xu = ub
                        )
    
    from pymoo.operators.sampling.rnd import FloatRandomSampling, BinaryRandomSampling, IntegerRandomSampling, PermutationRandomSampling
    from pymoo.operators.selection.rnd import RandomSelection
    from pymoo.operators.selection.tournament import TournamentSelection, compare
    from pymoo.operators.crossover.ux import UniformCrossover
    from pymoo.operators.crossover.dex import DEX
    from pymoo.operators.crossover.hux import HalfUniformCrossover
    from pymoo.operators.crossover.pcx import ParentCentricCrossover
    from pymoo.operators.crossover.expx import ExponentialCrossover
    from pymoo.operators.crossover.sbx import SimulatedBinaryCrossover
    from pymoo.operators.crossover.pntx import PointCrossover, TwoPointCrossover, SinglePointCrossover
    from pymoo.operators.mutation.rm import ChoiceRandomMutation
    from pymoo.operators.mutation.pm import PolynomialMutation
    from pymoo.operators.survival.rank_and_crowding import RankAndCrowding

    # algorithm = GA(pop_size = 100,
    #             #    sampling = FloatRandomSampling(),
    #             #    selection = RandomSelection(),
    #             #    crossover = SimulatedBinaryCrossover(prob_var=0.55),
    #             #    mutation = PolynomialMutation(prob = 0.85, eta = 19, at_least_once = True),
    #                eliminate_duplicates = True,
    #             #    survival= RankAndCrowding(),
    #                n_offsprings = 600)
    
    # algorithm = PSO(pop_size = 100,
    #                 sampling=FloatRandomSampling(),
    #                 w=0.5,
    #                 c1=2.5,
    #                 c2=2.5,
    #                 max_velocity_rate=0.1
    #                 )

    algorithm = PatternSearch(init_delta=0.3,
                              init_rho=0.6,
                              step_size=1.5)

    res = minimize(problem,
                   algorithm,
                   (('n_gen', 250)),
                   seed = 1,
                   verbose = True,               
                   )
    
    results = {}
    results['Lucro'] = - res.F
    x = res.X
    
    # Decompõe o vetor de variáveis de decisão em matrizes
    p_bm, p_dl, p_chg, p_dch, soc, u_bm, u_dl, u_chg, u_dch = decomp_vetor_v1(x, Nt, Nbm, Ndl, Nbat) 

    # Reshape dos vetores em matrizes
    results['p_bm'] = p_bm.reshape((Nbm, Nt))
    results['p_dl'] = p_dl.reshape((Ndl, Nt))
    results['p_chg'] = p_chg.reshape((Nbat, Nt))
    results['p_dch'] = p_dch.reshape((Nbat, Nt))
    results['soc'] = soc.reshape((Nbat, Nt))
    results['u_bm'] = u_bm.reshape((Nbm, Nt))
    results['u_dl'] = u_dl.reshape((Ndl, Nt))
    results['u_chg'] = u_chg.reshape((Nbat, Nt))
    results['u_dch'] = u_dch.reshape((Nbat, Nt))

    return results, x

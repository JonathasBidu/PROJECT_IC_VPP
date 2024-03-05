from pymoo.algorithms.moo.nsga2 import NSGA2 # Algoritmo multiobjetivo
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.config import Config
import numpy as np

Config.warnings['not_compiled'] = False

# função objetivo 1
def fob(x):
    return [np.sin(x[0]**2) + np.cos(x[1]**2)]

# função objetivo 2
def fob2(x):
    return [(x[0] - 1)**2 + x[1]**2]

def constraints(x):
    g1 = 2*(x[0] - 0.1) * (x[0] - 0.9) / 0.18
    g2 = - 20*(x[0] - 0.4) * (x[0] - 0.6) / 4.8
    return [g1, g2]

# MyProblem -> classe meu problema modificada para a resolução do problema 
class MyProblem(ElementwiseProblem):
   
    def _evaluate(self, x, out, *args, **kwargs):


        out['F'] = [fob(x)] # Deve ser uma lista do comprimento de n_var
        out['G'] = constraints(x) # Deve ser uma lista do comprimento de n_ieq_const/n_eq_const


prb = MyProblem(n_var = 2, # Qtd de variáveis 
                n_obj = 1, # Qtd de objetivos
                n_ieq_constr = 2, # Qtd de restrições
                xl = np.array([-10., -10.]), # Limites inferiores(devem ter comprimento igual a qtd de variáveis)
                xu = np.array([13., 13.]) # Limites superiores(devem ter comprimento igual a qtd de variáveis)
                )

# algorithm = NSGA2(pop_size = 100,
#                   n_offsprings = 10,
#                   sampling = FloatRandomSampling(),
#                   crossover = SBX(prob = 0.9, eta = 15),
#                   mutation = PM(eta = 20),
#                   eliminate_duplicates = True # Elimina as duplicatas
#                   )

algorithm = GA()

res = minimize(prb, # Objeto a ser minimizado
               algorithm, # Objjeto algoritmo
               (('n_gen', 100)), # Definindo o número de geração
               seed = 1,
               verbose = False # Se False deixa de mostra o display 
               )

X = res.X
F = res.F

print('')
print(f'O valor mínimo da função é {F}\n')
print(f'O ponto de mínimo da função é {X}\n')


# n_gen -> número de gerações
# n_eval -> número de avaliações
# cv_min ->  violação mínima da restrição
# cv_avg ->  violação média da restrição

import matplotlib.pyplot as plt
xl, xu = prb.bounds()
plt.figure(figsize=(7, 5))
plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='none', edgecolors='r')
plt.xlim(xl[0], xu[0])
plt.ylim(xl[1], xu[1])
plt.title("Design Space")
plt.show()

plt.figure(figsize=(7, 5))
plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
plt.title("Objective Space")
plt.show()

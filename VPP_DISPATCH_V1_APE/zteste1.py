import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.algorithms.soo.nonconvex.pattern import PatternSearch

from pymoo.config import Config

'''
    Este programa otimiza uma função de forma vetorizada, onde x representa todo um subconjunto de
'''

Config.warnings['not_compiled'] = False

# fob -> função objetivo
def fob(z):
    x = z[0]
    y = z[1]
    return (4 - 2.1 * (x ** 2) + (x ** (4 / 3))) * (x ** 2) + (x * y) + (- 4 + 4 * (y ** 2)) * (y ** 2) 

# Função para maximizar a função fob
# l = lambda x: - fob(x)

# cont -> função de restrição
def const(z):
    x = z[0]
    y = z[1]
    # [1,5 + x(1)*x(2) + x(1) - x(2);
    #  -x(1)*x(2) + 10];
    c1 = 1.5 + (x * y) + x - y
    c2 = - x * y + 10
    return c1, c2

# Preparando os dados para o plot
x = np.linspace(0, 1, 500)
y = np.linspace(0, 13, 500)
X, Y = np.meshgrid(x, y)

Z = fob(np.array([X, Y]))

# ponto de mínimo
a, b = [ 0.81222921, 12.31508802]

# ponto de máximo
# a, b = [ 1.63191726, 13.        ]


# Plot de superfície
# fig = plt.figure(figsize = (12, 6))
# ax = fig.add_subplot(1, 2, 1, projection ='3d')
# ax.plot_surface(X, Y, Z, cmap = cm.jet)
# # plt.plot(a, b, 'ro', markersize = 5)
# ax.set_title('Superfície da função objetivo')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# # Plot de contorno
# ax = fig.add_subplot(1, 2, 2)
# contour = ax.contour(X, Y, Z, cmap = cm.jet, levels = 40)
# ax.set_title('Contorno da função objetivo')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')

# plt.plot(a, b, 'bo', markersize = 10)
# plt.show()
fig = plt.figure(figsize=(8, 6))

# Plot de contorno
ax = fig.add_subplot(1, 1, 1)
contour = ax.contour(X, Y, Z, cmap=cm.jet, levels=40)
ax.set_title('Contorno da função objetivo')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Plota o ponto mínimo
ax.plot(a, b, 'bo', markersize=10)

plt.show()



# MyProblem -> classe meu problema modificada para a resolução do problema 
class MyProblem(ElementwiseProblem):

    def _evaluate(self, x, out, *args, **kwargs):

        out['F'] = np.array(fob(x))
        out['G'] = np.array(const(x))

prb = MyProblem(n_var = 2, # Quantidade de variáveis
                n_obj = 1, # Qunatidade de função objetivo
                n_ieq_constr = 2,
                xl = [0, 0], # limite inferior(deve ter o mesmo tamanho da quantidade de variáveis)
                xu = [1, 13] # limite superior(deve ter o mesmo tamanho da quantidade de variáveis)
                )

algorithm = GA(pop_size = 150)
# algorithm = PSO(pop_size = 150)
# algorithm = PatternSearch()
               

res = minimize(prb, # Objeto problema criado acima 
               algorithm, # Algoritmo definido acima
                ('n_gen', 100), # Número de geração
                seed = 1, # Semente
                verbose = True
                )

print('')
print(f'O valor mínimo da função é {res.F}\n')
print(f'O ponto de mínimo da função é {res.X}\n')

# Calcular as restrições para a solução ótima encontrada
constraints = const(res.X)
c1, c2 = constraints[0], constraints[1]

# Verificar se as restrições são satisfeitas
if c1 <= 0 and c2 <= 0:
    print("As restrições do problema são satisfeitas para a solução ótima encontrada.")
else:
    print("As restrições do problema não são satisfeitas para a solução ótima encontrada.")
    print("Restrição 1:", c1)
    print("Restrição 2:", c2)

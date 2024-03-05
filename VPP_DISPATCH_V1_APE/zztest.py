from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.algorithms.soo.nonconvex.pattern import PatternSearch
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
from pymoo.config import Config
Config.warnings['not_compiled'] = False



def f(x, y):
    return 2*x**2 + 3*y**2 + 4*x*y + 10*x - 5*y

x = np.linspace(- 20, 20, 500)
y = np.linspace(- 20, 20, 500)
X, Y = np.meshgrid(x, y)
f_arr = f(X, Y)
f_arr = np.array(f_arr)
a, b = [-10.00214105, 7.50268401]

fig = plt.figure(figsize = (12, 5))
ax = fig.add_subplot(1, 2, 1, projection = '3d')
ax.set_title('Gráfico de Superfície')
ax.set_xlabel('EIXO X')
ax.set_ylabel('EIXO Y')
ax.plot_surface(X, Y, f_arr, cmap = 'coolwarm', alpha=0.8)

ax2 = fig.add_subplot(1, 2, 2)

ax2.contour(X, Y, f_arr, levels = 50, cmap='coolwarm', alpha=0.8)
ax2.set_title('Gráfico de Contorno')
ax2.set_xlabel('EIXO X')
ax2.set_ylabel('EIXO Y')
plt.plot(a, b, 'ro')
plt.show()

def fob(z):

    x = z[0]
    y = z[1]
    return  2*x**2 + 3*y**2 + 4*x*y + 10*x - 5*y

class MyProblem(Problem):

    def _evaluate(self, x, out):

        res = []
        for i in x:
            res.append(fob(i))

        out['F'] = np.array(res)

prb = MyProblem(n_var = 2,
                n_obj = 1,
                xl = np.array([-20, -20]),
                xu = np.array([20, 20])
                )


# algorithm = GA()
algorithm = PSO()
# algorithm = PatternSearch()

res = minimize(prb,
               algorithm,
               seed = 1,
               verbose = True
               )

print('')
print(f'A solução ótima encontrada foi {res.F}\n')
print(f'O ponto de ótimo encontrado é {res.X}\n')


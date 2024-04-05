import numpy as np
import matplotlib.pyplot as plt  
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
"""
    Esse script constrói um previsor de séries temporais.
    Parâmetros:
    - Z (list): Lista contendo os valores da série temporal.
    Retorna:
    tuple: Uma tupla contendo o modelo MLPRegressor treinado, o número de lags, as séries observadas (Y) e as séries estimadas (Yhat).
"""
def generator_nnmodel(Z: list)-> tuple:

    # Obtendo o tamanho de z 
    N = len(Z)
    # Obtendo a quantidade de lags
    while True:
        p = input('Insira o número de lags ou tecle enter para 2: ')
        if p == '':
            p = 2
            break
        try:
            p = int(p)
            if p > 0:
                p = p
                break
            else:
                print("Insira um valor numérico inteiro e positivo")
        except ValueError:
            print("Insira um valor numérico inteiro e positivo")

        
    # Iniciando a matriz de entrada "X" e o vetor de saída "Y" que será utilizado no modelo a seguir
    X = np.zeros((N - p, p))
    Y = np.zeros((N - p, ))
    
    # separando os dados de entrada e os dados de saída para o modelo de RNA que será implementado a seguir.
    # Entrada = y(t) para y(t-p), t = p + 1 : T
    # Saída = y(t + 1), t = p + 1 : T
    for k in range(p, N):
        X[k - p, : ] = Z[k - p : k]  
        Y[k - p] = Z[k]   

    """
    Criando a arquitetura RNA atravéz do modelo MPLRegressor onde, MPL(Multi-Layer Perception) modelo de multi-camadas de neurônios Perception e Regressor é uma classe da biblioteca sklearn que utiliza a regressão e o solucionador "adam" para ajustar os pesos e bias. 
    *** Método 'adam' (Adaptive Moment Estimation)

    Descrição:
    O método 'adam' é um otimizador amplamente utilizado em algoritmos de aprendizado de máquina, especialmente em redes neurais. Ele combina características de otimizadores de momento e taxa de aprendizado adaptativa para eficientemente minimizar a soma dos quadrados dos resíduos entre uma função modelada e os dados observados.

    Funcionamento:
    1. Inicialização: O método inicia com uma estimativa inicial dos parâmetros a serem otimizados.
    2. Iteração: Utiliza uma combinação adaptativa de descida do gradiente e algoritmo de momento para ajustar iterativamente os parâmetros.
    3. Taxa de Aprendizado Adaptativa: A técnica ajusta dinamicamente a taxa de aprendizado para cada parâmetro, proporcionando convergência eficiente.

    Parâmetros:
    - Função a ser otimizada: Deve ser fornecida a função que calcula os resíduos a serem minimizados.
    - Parâmetros iniciais: Lista dos valores iniciais para os parâmetros a serem otimizados.
    - Limites dos parâmetros: Pode ser especificado um intervalo permitido para cada parâmetro.
    - Tolerância: Define a precisão desejada para a solução, indicando a convergência.
    - Beta1 e Beta2: Parâmetros que controlam as médias móveis exponenciais de gradientes e quadrados de gradientes, respectivamente.
    - Epsilon: Pequeno valor adicionado para evitar divisões por zero na adaptação da taxa de aprendizado.

    Nota: O método 'adam' é particularmente eficaz em problemas de grande escala e variabilidade na escala dos gradientes.
    """    
    model = MLPRegressor(
                            hidden_layer_sizes = (50, 50), 
                            solver = 'adam', 
                            max_iter = 5000, 
                            learning_rate = 'adaptive', 
                            learning_rate_init= 0.001,
                            verbose = True
                        )

    # Treinando o modelo onde, X é a matriz de entrada e Y é a saída desejada
    model.fit(X, Y)

    # obtendo o vetor de épocas que será utilzado na plotagem do gráfico
    epochs = np.arange(p, N)

    # Geração da previsão pela rede utilizando o modelo treinado acima para os dados de entrada (X) 
    print(f'Estou no previsor: tipo = {type(X)}, shape = {X.shape}')
    Yhat = model.predict(X)

    # Erro médio quadrado obtido pelo modelo
    perf = mean_squared_error(Y, Yhat)
    # Obtendo coeficiente de determinação R² da previsão, R² é uma métrica que varia de 0 a 1, quanto mais próximo de 1 indica um ajuste melhor do modelo
    metric = model.score(X, Y)
    print(f'O desempenho do modelo em termos de erro médio quadrático foi: {perf:.3f}')
    print(f'O ajuste geral do modelo aos dados usando o coeficiênte de determinação R² foi: {metric:.3f}')

    # Plotando o gráfico de saídas esperadas e saídas previstas   
    fig, ax = plt.subplots(figsize = (12, 5))
    ax.plot(epochs, Y)
    ax.plot(epochs, Yhat)
    ax.set_title('Forecast Model MLPRegressor', fontsize = 17)
    ax.set_xlabel('Epoch', fontsize = 14)
    ax.set_ylabel('Amplitude', fontsize = 14)
    plt.legend(['Saídas esperadas', 'Saídas previstas'])
    plt.grid(True)
    plt.show()
    
    Mdl = model
    return Mdl, p, Y, Yhat
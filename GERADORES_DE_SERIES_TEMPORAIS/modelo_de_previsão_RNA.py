import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Criando uma variável que irá atribuir o caminho da tebela em emu computador
path = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP\\GERADORES_DE_SERIES_TEMPORAIS\\BANCO_DE_DADOS\\TABELA_DE_CONVERSÃO_DE_CELSIUS_PARA_FAHRENHEIT.xlsx"

# Gerando um DataFrame
temperature_df = pd.read_excel(path)

# dividindo os dados em conjunto de treinamento e teste
x = temperature_df['Celsius']
y = temperature_df['Fahrenheit']
x_train , x_test = x[:25], x[25:]
y_train , y_test = y[:25], y[25:]

# Criando e configurando a arquitetura da rede neural com 3 neurônios de entrada e um de saída
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=10, input_shape=[1], activation='relu'),
    tf.keras.layers.Dense(units=1, activation='linear')
])
# print(model.summary())

# Treinamento do neurônio  
# aplicando o modelo de otimização Adam, função de custo a ser minimizada erro médio quadrado e acompanhando pela métrica erro médio absoluto
model.compile(loss = 'mse', optimizer = tf.keras.optimizers.Adam(0.05))
result = model.fit(x_train, y_train, epochs = 350, validation_data = (x_test, y_test))

# epochs_hist = model.fit(x, y, epochs= 1200)
result.history.keys()

# Avaliando o modelo
loss = model.evaluate(x_test, y_test)
print(f'Loss no conjunto de teste: {loss}')


# # Avaliação do modelo
temp_C = np.array([float(input('Insira uma temperatura em graus Celsius: '))])  # Valor para prever
temp_F = model.predict(temp_C)
temp_F_real = (9 / 5) * temp_C[0] + 32

print(f'Valor encontrado pelo modelo foi {temp_F}')
print(f'O valor real é {temp_F_real}')

# # plotagem do erro em função das épocas
plt.plot(result.history['loss'])
plt.plot(result.history['val_loss'])
plt.title('Model Loss Progress During Training')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Loss', 'Traning'])
plt.show()



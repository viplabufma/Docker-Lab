import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# Verificar se GPU está disponível
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    print(f"GPUs detectadas: {len(gpus)}")
    for gpu in gpus:
        print(f"Nome da GPU: {gpu.name}")
else:
    print("Nenhuma GPU disponível. Usando CPU.")

# Carregar o conjunto de dados CIFAR-10
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

# Normalizar os valores de pixel (entre 0 e 1)
x_train, x_test = x_train / 255.0, x_test / 255.0

# Definir o modelo CNN
model = models.Sequential()

# Camada Convolucional 1
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))

# Camada Convolucional 2
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Camada Convolucional 3
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

# Camadas totalmente conectadas
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))  # 10 classes de saída

# Compilar o modelo
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Resumo do modelo
model.summary()

# Treinar a CNN
model.fit(x_train, y_train, epochs=10, 
          validation_data=(x_test, y_test),
          batch_size=64)

# Avaliar a CNN no conjunto de teste
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f"Acurácia no conjunto de teste: {test_acc:.2f}")

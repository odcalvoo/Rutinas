import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random
import matplotlib.pyplot as plt

# Instrucciones para el usuario
print("""
=== Clasificador de Daños Estructurales en Vigas ===
Este programa usa un árbol de decisión para determinar si una viga de concreto está dañada
basándose en datos de sensores: deformación (mm/mm), vibración (Hz) y carga (kN).
Los datos son simulados, pero reflejan un caso realista de monitoreo estructural.
Se incluye una gráfica para visualizar los resultados.
Ejecute el código y revise los resultados en la consola y la gráfica generada.
""")

# Función para generar datos sintéticos de sensores
def generate_synthetic_data(n_samples=1000):
    """
    Genera datos simulados de sensores para vigas de concreto.
    - strain: Deformación en mm/mm (0.0001 a 0.01)
    - vibration: Frecuencia de vibración en Hz (0.1 a 10.0)
    - load: Carga aplicada en kN (50 a 500)
    - is_damaged: 1 si la viga está dañada (strain > 0.005 y load > 300), 0 si no
    """
    data = []
    for _ in range(n_samples):
        strain = random.uniform(0.0001, 0.01)
        vibration = random.uniform(0.1, 10.0)
        load = random.uniform(50, 500)
        is_damaged = 1 if strain > 0.005 and load > 300 else 0
        data.append([strain, vibration, load, is_damaged])
    return pd.DataFrame(data, columns=['strain', 'vibration', 'load', 'is_damaged'])

# Generar datos
print("Generando datos sintéticos de sensores...")
data = generate_synthetic_data()

# Preparar datos para el modelo
X = data[['strain', 'vibration', 'load']]  # Características
y = data['is_damaged']  # Etiquetas (0: No dañada, 1: Dañada)

# Dividir datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo de árbol de decisión
print("Entrenando el modelo de árbol de decisión...")
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluar la precisión del modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nPrecisión del modelo en datos de prueba: {accuracy:.2%}")
print("Esto indica qué tan bien el modelo clasifica vigas dañadas vs. no dañadas.\n")

# Probar con ejemplos de vigas
test_beams = pd.DataFrame([
    [0.006, 5.0, 350],  # Viga con alta deformación y carga
    [0.002, 4.0, 200],  # Viga con bajas deformación y carga
    [0.007, 6.0, 250],  # Viga con alta deformación pero baja carga
    [0.008, 3.0, 400],  # Viga con alta deformación y carga
], columns=['strain', 'vibration', 'load'])

# Realizar predicciones
print("Predicciones para vigas de prueba:")
predictions = model.predict(test_beams)
results = test_beams.copy()
results['Estado'] = ['Dañada' if pred == 1 else 'No dañada' for pred in predictions]
results.columns = ['Deformación (mm/mm)', 'Vibración (Hz)', 'Carga (kN)', 'Estado']

# Mostrar resultados en una tabla formateada
print("\nResultados de las vigas de prueba:")
print(results.to_string(index=False, formatters={
    'Deformación (mm/mm)': '{:.4f}'.format,
    'Vibración (Hz)': '{:.1f}'.format,
    'Carga (kN)': '{:.0f}'.format
}))

# Visualización con Matplotlib
print("\nGenerando gráfica de dispersión...")
plt.figure(figsize=(8, 6))
colors = ['red' if pred == 1 else 'green' for pred in predictions]
plt.scatter(test_beams['strain'], test_beams['load'], c=colors, s=100, alpha=0.7)
plt.xlabel('Deformación (mm/mm)')
plt.ylabel('Carga (kN)')
plt.title('Clasificación de Vigas: Dañada (Rojo) vs. No Dañada (Verde)')
plt.grid(True)

# Agregar leyenda
plt.scatter([], [], c='red', label='Dañada')
plt.scatter([], [], c='green', label='No dañada')
plt.legend()

# Mostrar la gráfica
plt.show()

# Instrucciones finales
print("""
=== Fin del programa ===
Para usar datos reales, reemplace la función `generate_synthetic_data` con sus propios datos.
Asegúrese de tener instaladas las bibliotecas: numpy, pandas, scikit-learn, matplotlib.
Instálelas con: `pip install numpy pandas scikit-learn matplotlib`
Guarde este archivo en su repositorio de GitHub y ejecute con Python 3.
La gráfica muestra las vigas de prueba, con puntos rojos para vigas dañadas y verdes para no dañadas.
""")
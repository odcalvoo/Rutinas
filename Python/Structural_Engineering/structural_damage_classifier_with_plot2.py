import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import warnings

# Suprimir warnings de Matplotlib
warnings.filterwarnings("ignore", category=UserWarning)

# Instrucciones para el usuario
print("""
=== Clasificador de Daños Estructurales en Vigas ===
Este programa usa un árbol de decisión para determinar si una viga de concreto está dañada
basándose en datos de sensores: deformación (mm/mm), vibración (Hz) y carga (kN).
Se generan datos sintéticos, pero puede adaptarse a datos reales (ver instrucciones finales).
Ejecute el código y revise los resultados en la consola y la gráfica generada.
""")

# Función para generar datos sintéticos optimizada
def generate_synthetic_data(n_samples=1000):
    """
    Genera datos simulados de sensores para vigas de concreto.
    - strain: Deformación en mm/mm (0.0001 a 0.01)
    - vibration: Frecuencia de vibración en Hz (0.1 a 10.0)
    - load: Carga aplicada en kN (50 a 500)
    - is_damaged: 1 si strain > 0.005 y load > 300, 0 si no (con ruido aleatorio)
    """
    strain = np.random.uniform(0.0001, 0.01, n_samples)
    vibration = np.random.uniform(0.1, 10.0, n_samples)
    load = np.random.uniform(50, 500, n_samples)
    is_damaged = ((strain > 0.005) & (load > 300)).astype(int)  # Regla base
    is_damaged = np.where(np.random.random(n_samples) > 0.1, is_damaged, 1 - is_damaged)  # 10% de ruido
    return pd.DataFrame({
        'strain': strain,
        'vibration': vibration,
        'load': load,
        'is_damaged': is_damaged
    })

# Generar datos
print("Generando datos sintéticos de sensores...")
data = generate_synthetic_data()

# Preparar datos para el modelo
X_features = data[['strain', 'vibration', 'load']]  # Características
y_labels = data['is_damaged']  # Etiquetas

# Dividir datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X_features, y_labels, test_size=0.2, random_state=42)

# Entrenar el modelo de árbol de decisión
print("Entrenando el modelo de árbol de decisión...")
dt_classifier = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_classifier.fit(X_train, y_train)

# Evaluar la precisión del modelo
y_pred = dt_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nPrecisión del modelo en datos de prueba: {accuracy:.2%}")
print("Esto indica qué tan bien el modelo clasifica vigas dañadas vs. no dañadas.\n")

# Probar con ejemplos de vigas
test_beams = pd.DataFrame([
    [0.006, 5.0, 350],  # Alta deformación y carga
    [0.002, 4.0, 200],  # Bajas deformación y carga
    [0.007, 6.0, 250],  # Alta deformación, baja carga
    [0.008, 3.0, 400],  # Alta deformación y carga
], columns=['strain', 'vibration', 'load'])

# Realizar predicciones
print("Predicciones para vigas de prueba:")
predictions = dt_classifier.predict(test_beams)
results = test_beams.copy()
results['Estado'] = ['Dañada' if pred == 1 else 'No dañada' for pred in predictions]
results.columns = ['Deformación (mm/mm)', 'Vibración (Hz)', 'Carga (kN)', 'Estado']

# Mostrar resultados
print("\nResultados de las vigas de prueba:")
print(results.to_string(index=False, formatters={
    'Deformación (mm/mm)': '{:.4f}'.format,
    'Vibración (Hz)': '{:.1f}'.format,
    'Carga (kN)': '{:.0f}'.format
}))

# Visualización
print("\nGenerando gráfica de dispersión...")
plt.figure(figsize=(8, 6))
colors = ['red' if pred == 1 else 'green' for pred in predictions]
scatter = plt.scatter(test_beams['strain'], test_beams['load'], c=colors, s=100, alpha=0.7)
plt.xlabel('Deformación (mm/mm)')
plt.ylabel('Carga (kN)')
plt.title('Clasificación de Vigas: Dañada (Rojo) vs. No Dañada (Verde)')
plt.grid(True)
# Ajuste para evitar warnings en la leyenda
plt.legend(['Dañada', 'No dañada'], loc='best')
plt.show()

# Instrucciones finales
print("""
=== Fin del programa ===
Para usar datos reales, reemplace 'generate_synthetic_data' con un DataFrame de pandas
conteniendo columnas 'strain', 'vibration', 'load' e 'is_damaged'.
Instale las bibliotecas con: 'pip install numpy pandas scikit-learn matplotlib'
Ejecute con Python 3.
La gráfica muestra las vigas de prueba clasificadas por estado.
""")
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Autor: Oscar Calvo
# Fecha: Julio 14, 2025
# Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
# Descripción: Simulación de análisis Pushover con un modelo estructural simplificado
#              y predicción de desplazamiento en el colapso usando IA.

# Simulación de un marco estructural simplificado
def simular_pushover(cargas, k_elastic=1000, yield_force=500, ductility=4):
    """
    Simula el comportamiento Pushover de un marco 1D con elasticidad y plasticidad.
    Retorna desplazamientos considerando un punto de rendimiento y colapso.
    """
    desplazamientos = np.zeros_like(cargas)
    for i, carga in enumerate(cargas):
        if carga <= yield_force:
            desplazamientos[i] = carga / k_elastic  # Región elástica
        else:
            delta_yield = yield_force / k_elastic
            delta_ultimate = ductility * delta_yield
            if carga < yield_force * ductility:
                desplazamientos[i] = delta_yield + (carga - yield_force) / (k_elastic / ductility)
            else:
                desplazamientos[i] = delta_ultimate  # Colapso
    return desplazamientos

# Generar datos de entrenamiento
np.random.seed(42)
cargas = np.linspace(0, 1000, 200)
desplazamientos = simular_pushover(cargas)
X = np.column_stack((cargas, cargas**2 / 1000))  # Añadir término no lineal
y = desplazamientos + np.random.normal(0, 0.01 * desplazamientos)

# Escalar datos
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Entrenar modelo de IA
modelo = MLPRegressor(hidden_layer_sizes=(30, 20), max_iter=2000, random_state=42)
modelo.fit(X_train, y_train)

# Predicciones
y_pred_scaled = modelo.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()
y_test_unscaled = scaler_y.inverse_transform(y_test.reshape(-1, 1)).ravel()
X_test_unscaled = scaler_X.inverse_transform(X_test)[:, 0]  # Solo la carga como eje X

# Métricas
mse = mean_squared_error(y_test_unscaled, y_pred)
r2 = r2_score(y_test_unscaled, y_pred)
print(f"Error Cuadrático Medio (MSE): {mse:.4f}")
print(f"Coeficiente de Determinación (R²): {r2:.4f}")

# Visualización
plt.figure(figsize=(10, 6))
plt.plot(cargas, simular_pushover(cargas), 'b-', label="Curva Pushover Real", linewidth=2)
plt.scatter(X_test_unscaled, y_pred, color='red', label="Predicción IA", s=20)
plt.xlabel("Carga (N)")
plt.ylabel("Desplazamiento (m)")
plt.title("Análisis Pushover: Curva Real vs. Predicción con IA")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()
plt.savefig('pushover_structural_plot.png')
plt.show()
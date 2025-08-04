import numpy as np
import random
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
#
#Autor: Oscar Calvo
# Fecha: Agosto 03/2025
# Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
#
# 1. Generar datos sintéticos de un ciclo de histéresis realista
def generar_ciclo_realista(amplitud, rigidez, gordura, pellizco=0.8):
    t = np.linspace(0, 2 * np.pi, 150)
    x = amplitud * np.sin(t)
    y_elastico = rigidez * x
    y_histeretico = gordura * amplitud * np.cos(t) * (1 - pellizco * np.abs(np.sin(t)))
    y = y_elastico + y_histeretico + np.random.normal(0, 0.05, 150)  # Añadimos ruido
    return x, y

def calcular_area(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

# Generamos datos de entrenamiento con más muestras y ruido
datos_entrenamiento = []
etiquetas = []

np.random.seed(42)
# Nivel 1: Elástico/Seguro
for _ in range(50):
    amp = np.random.uniform(0.3, 0.7)
    rig = np.random.uniform(8, 12)
    gord = np.random.uniform(1.0, 2.5)
    x, y = generar_ciclo_realista(amp, rig, gord, pellizco=0.5)
    datos_entrenamiento.append([np.max(x), calcular_area(x, y)])
    etiquetas.append("Seguro")

# Nivel 2: Daño Dúctil
for _ in range(50):
    amp = np.random.uniform(1.5, 2.5)
    rig = np.random.uniform(3, 6)
    gord = np.random.uniform(4.0, 6.0)
    x, y = generar_ciclo_realista(amp, rig, gord, pellizco=0.8)
    datos_entrenamiento.append([np.max(x), calcular_area(x, y)])
    etiquetas.append("Daño Dúctil")

# Nivel 3: Daño Severo
for _ in range(50):
    amp = np.random.uniform(3.0, 4.5)
    rig = np.random.uniform(1, 3)
    gord = np.random.uniform(3.0, 5.0)
    x, y = generar_ciclo_realista(amp, rig, gord, pellizco=0.95)
    datos_entrenamiento.append([np.max(x), calcular_area(x, y)])
    etiquetas.append("Daño Severo")

X_entrenamiento = np.array(datos_entrenamiento)
y_entrenamiento = np.array(etiquetas)

# 2. Preparar los datos y entrenar
X_train, X_test, y_train, y_test = train_test_split(X_entrenamiento, y_entrenamiento, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

ia_clasificador = MLPClassifier(hidden_layer_sizes=(12, 6), max_iter=2000, alpha=0.01, random_state=42)
print("🧠 Entrenando la Red Neuronal con datos realistas...")
ia_clasificador.fit(X_train_scaled, y_train)
print("✅ ¡Entrenamiento completo!")

# 3. Evaluar el modelo
y_pred = ia_clasificador.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=["Seguro", "Daño Dúctil", "Daño Severo"])
print(f"\n📊 Precisión en el conjunto de prueba: {accuracy:.2f}")
print("Matriz de confusión:")
print(cm)

# 4. Probar con un nuevo ciclo aleatorio
print("\n--------------------------------------------------")
print("🎲 Generando un nuevo ciclo de prueba aleatorio y realista...")
tipos_posibles = ["Seguro", "Daño Dúctil", "Daño Severo"]
tipo_real = random.choice(tipos_posibles)

if tipo_real == "Seguro":
    params = {'amplitud': random.uniform(0.4, 0.9), 'rigidez': random.uniform(9, 12), 'gordura': random.uniform(1.5, 2.5), 'pellizco': 0.6}
elif tipo_real == "Daño Dúctil":
    params = {'amplitud': random.uniform(1.8, 2.6), 'rigidez': random.uniform(3, 5), 'gordura': random.uniform(4.5, 5.5), 'pellizco': 0.8}
else:  # Daño Severo
    params = {'amplitud': random.uniform(3.0, 4.0), 'rigidez': random.uniform(1, 2), 'gordura': random.uniform(4.5, 5.5), 'pellizco': 0.95}

x_nuevo, y_nuevo = generar_ciclo_realista(**params)
amplitud_nueva = np.max(x_nuevo)
area_nueva = calcular_area(x_nuevo, y_nuevo)

print(f"  > El ciclo generado es de tipo real: '{tipo_real}'")
print(f"  > Características: Amplitud={amplitud_nueva:.2f}, Área={area_nueva:.2f}")

dato_nuevo_escalado = scaler.transform([[amplitud_nueva, area_nueva]])
prediccion = ia_clasificador.predict(dato_nuevo_escalado)

print(f"\n🤖 La IA predice que el nivel de daño es: *** {prediccion[0]} ***")
if prediccion[0] == tipo_real:
    print("🎯 ¡La predicción es CORRECTA!")
else:
    print("❌ ¡La predicción es INCORRECTA!")
print("--------------------------------------------------")

# 5. Visualizar el ciclo de prueba
plt.figure(figsize=(8, 6))
plt.plot(x_nuevo, y_nuevo, 'b-', linewidth=2, label=f'Tipo Real: {tipo_real}\nPredicción: {prediccion[0]}')
plt.title('Ciclo de Histéresis Realista y Predicción de la IA')
plt.xlabel('Deformación (Desplazamiento)')
plt.ylabel('Fuerza')
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.legend()
plt.axis('equal')
plt.savefig('hysteresis_realistic_prediction.png')
plt.show()
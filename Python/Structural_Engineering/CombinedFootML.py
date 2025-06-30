import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
#
#Autor: Oscar Calvo
# Fecha: Junio 30/2025
# Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
#
# Instrucciones para el usuario
print("""
=== Clasificador de Zapatas Combinadas con Machine Learning ===
Este programa evalúa si una zapata combinada es adecuada para soportar dos columnas,
basándose en sus cargas (P1, P2), la distancia entre ellas (d) y la capacidad portante del suelo (q).
Usa un árbol de decisión entrenado con datos sintéticos y estima dimensiones iniciales.
Incluye una gráfica con los datos de entrada del usuario y el conjunto de entrenamiento como contexto.
Nota: Este es un ejercicio educativo. Valide los resultados con normativas (ej. ACI 318, Eurocódigo).
Para datos reales, reemplace la función `generar_datos_entrenamiento` con un archivo CSV o datos de proyecto.
""")

# Función para generar datos sintéticos
def generar_datos_entrenamiento(n_samples=1000):
    """
    Genera datos sintéticos para entrenar el modelo (simula datos de proyecto).
    - P1, P2: Cargas de las columnas (kN)
    - d: Distancia entre columnas (m)
    - q: Capacidad portante del suelo (kN/m^2)
    - Etiqueta: 1 (Adecuada) si el área mínima es menor que d*2 y la carga total es soportable
    Para datos reales, reemplace esta función con datos de un CSV o proyecto estructural.
    Ejemplo: pd.read_csv('datos_zapatas.csv', columns=['P1', 'P2', 'd', 'q', 'etiqueta'])
    """
    datos = []
    etiquetas = []
    for _ in range(n_samples):
        P1 = np.random.uniform(100, 1000)
        P2 = np.random.uniform(100, 1000)
        d = np.random.uniform(2, 6)
        q = np.random.uniform(100, 300)
        area_minima = (P1 + P2) / q
        if area_minima < (d * 2) and (P1 + P2) < (q * d * 2):
            etiquetas.append(1)  # Adecuada
        else:
            etiquetas.append(0)  # No Adecuada
        datos.append([P1, P2, d, q])
    return pd.DataFrame(datos, columns=['P1', 'P2', 'd', 'q']), np.array(etiquetas)

# Generar y preparar datos
print("Generando datos sintéticos...")
X, y = generar_datos_entrenamiento()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entrenar el modelo
print("Entrenando el modelo de árbol de decisión...")
modelo = DecisionTreeClassifier(max_depth=5, random_state=42)
modelo.fit(X_train, y_train)

# Evaluar el modelo
predicciones = modelo.predict(X_test)
precision = accuracy_score(y_test, predicciones)
print(f"\nPrecisión del modelo en datos de prueba: {precision:.2%}")
print("Esto indica qué tan bien el modelo clasifica zapatas adecuadas vs. no adecuadas.\n")

# Función para evaluar zapata con validación y visualización
def evaluar_zapata():
    """
    Solicita datos al usuario, valida entradas, realiza predicciones y muestra resultados.
    Incluye una gráfica de dispersión con los datos de entrenamiento como contexto.
    Los valores deben ser realistas según el proyecto estructural.
    """
    try:
        print("\nEvaluación de Zapata Combinada")
        print("Nota: Ingrese valores realistas basados en su proyecto estructural.")
        P1 = float(input("Ingrese la carga de la primera columna (P1, kN): "))
        P2 = float(input("Ingrese la carga de la segunda columna (P2, kN): "))
        d = float(input("Ingrese la distancia entre columnas (d, m): "))
        q = float(input("Ingrese la capacidad portante del suelo (q, kN/m^2): "))

        # Validación de entradas
        if P1 <= 0 or P2 <= 0:
            raise ValueError("Las cargas (P1, P2) deben ser mayores a 0 kN.")
        if d < 0.5:
            raise ValueError("La distancia (d) debe ser al menos 0.5 m.")
        if q <= 0:
            raise ValueError("La capacidad portante (q) debe ser mayor a 0 kN/m^2.")

        # Predicción
        entrada = pd.DataFrame([[P1, P2, d, q]], columns=['P1', 'P2', 'd', 'q'])
        resultado = modelo.predict(entrada)

        # Resultados
        estado = "ADECUADA" if resultado[0] == 1 else "NO ADECUADA"
        print(f"\nResultado: La zapata combinada es {estado} para las condiciones dadas.")

        # Estimación de área y dimensiones
        area_estimada = (P1 + P2) / q
        margen = 0.5  # Margen de 50 cm a cada lado
        largo = d + 2 * margen
        ancho = max(area_estimada / largo, 1.0)  # Ancho mínimo de 1 m

        # Mostrar resultados en una tabla, incluyendo la precisión del modelo
        resultados = pd.DataFrame([{
            'Carga P1 (kN)': P1,
            'Carga P2 (kN)': P2,
            'Distancia (m)': d,
            'Capacidad portante (kN/m^2)': q,
            'Área estimada (m^2)': area_estimada,
            'Largo (m)': largo,
            'Ancho (m)': ancho,
            'Estado': estado,
            'Precisión del modelo (%)': precision * 100
        }])
        print("\nResultados detallados:")
        print(resultados.to_string(index=False, formatters={
            'Carga P1 (kN)': '{:.1f}'.format,
            'Carga P2 (kN)': '{:.1f}'.format,
            'Distancia (m)': '{:.2f}'.format,
            'Capacidad portante (kN/m^2)': '{:.1f}'.format,
            'Área estimada (m^2)': '{:.2f}'.format,
            'Largo (m)': '{:.2f}'.format,
            'Ancho (m)': '{:.2f}'.format,
            'Precisión del modelo (%)': '{:.2f}'.format
        }))

        # Visualización con datos de entrenamiento como contexto
        print("\nGenerando gráfica de dispersión...")
        plt.figure(figsize=(8, 6))
        # Mostrar datos de entrenamiento como fondo
        plt.scatter(X['P1'] + X['P2'], X['d'], c=['green' if label == 1 else 'red' for label in y], 
                    s=10, alpha=0.2, label='Datos de entrenamiento')
        # Mostrar punto del usuario
        color = 'green' if resultado[0] == 1 else 'red'
        plt.scatter(P1 + P2, d, c=color, s=100, edgecolors='black', label=f'Zapata: {estado}')
        plt.xlabel('Carga Total (P1 + P2, kN)')
        plt.ylabel('Distancia entre columnas (m)')
        plt.title('Clasificación de Zapata Combinada: Adecuada (Verde) vs. No Adecuada (Rojo)')
        plt.grid(True)
        # Personalizar la leyenda: sin fondo, borde negro, texto negro, fuera del cuadro principal
        plt.legend(facecolor='none', edgecolor='black', labelcolor='black', loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.show()

        print("\nNota: Las dimensiones son estimaciones iniciales. Valide con normativas de diseño estructural.")

    except ValueError as e:
        print(f"Error: {e}. Por favor, ingrese valores numéricos válidos.")
    except Exception as e:
        print(f"Error inesperado: {e}. Contacte al desarrollador.")

# Ejecutar evaluación
evaluar_zapata()

# Instrucciones finales
print("""
=== Fin del programa ===
Para usar datos reales, modifique `generar_datos_entrenamiento` para cargar datos de un proyecto
(ej. un archivo CSV con columnas P1, P2, d, q, etiqueta).
Asegúrese de tener instaladas las bibliotecas: numpy, pandas, scikit-learn, matplotlib.
Instálelas con: `pip install numpy pandas scikit-learn matplotlib`
Guarde este archivo en su repositorio de GitHub y ejecute con Python 3.
La gráfica muestra la zapata evaluada (punto grande) y los datos de entrenamiento (puntos pequeños).
""")
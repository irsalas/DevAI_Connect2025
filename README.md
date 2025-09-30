# DevAI_Connect2025

## Descripción General  ML-DL-Demos Folder

Este repositorio contiene el codigo que muestran técnicas de Machine Learning (ML) y Deep Learning (DL) aplicadas al análisis y pronóstico de métricas de red.

El objetivo principal es mostrar, mediante ejemplos prácticos, cómo aplicar distintos algoritmos de ML y DL en escenarios de detección de anomalías, clustering y forecasting de series temporales, enfocados en métricas operativas de redes.

📂 Contenido de los notebooks
1. ML_Techniques_final.ipynb

Este notebook presenta diferentes técnicas clásicas de Machine Learning aplicadas a datos de métricas de red.

Incluye:

Preprocesamiento de datos

Normalización y escalado de features

División de datasets en entrenamiento y prueba

Técnicas de Aprendizaje Supervisado y No Supervisado

Clasificación (Random Forest, Decision Trees, Logistic Regression, etc.)

Clustering (K-Means, DBSCAN, PCA para reducción de dimensionalidad)

Detección de anomalías

Evaluación de modelos

Matrices de confusión

Métricas: Precisión, Recall, F1-score

Visualizaciones de clusters y resultados

2. DL-Metric-forecast_English_v3.ipynb

Este notebook aborda técnicas de Deep Learning enfocadas en forecasting de métricas de red usando redes neuronales recurrentes (RNN/LSTM).

Incluye:

Conceptos de series temporales aplicados a métricas de red

Construcción de datasets con ventanas temporales (time steps)

Creación de tensores para entrenamiento de modelos DL

Modelado con LSTM

Construcción de una red LSTM para predicción de métricas (ej. suscriptores BNG, tráfico)

Explicación de hiperparámetros relevantes (timestep, horizonte de predicción, batch size)

Entrenamiento y validación con GPU/TPU

Evaluación del modelo

Funciones de pérdida (MSE, MAE, MAPE)

Visualización de curvas de aprendizaje (loss, val_loss)

Gráficos comparando valores reales vs predicciones

⚙️ Requisitos

Antes de ejecutar los notebooks, asegúrate de tener instalado:

python >= 3.9
tensorflow >= 2.9
keras
scikit-learn
numpy
pandas
matplotlib
seaborn


Puedes instalar los paquetes requeridos con:

pip install -r requirements.txt


Ejecución:

Clona este repositorio o descarga los notebooks.

Abre los notebooks en Jupyter Notebook o JupyterLab:

jupyter notebook


Ejecuta las celdas paso a paso siguiendo la secuencia propuesta.

Resultados esperados

ML_Techniques_final.ipynb:

Clusters de equipos de red agrupados por métricas de CPU, memoria, temperatura, etc.

Clasificación de estados de riesgo de los equipos.

DL-Metric-forecast_English_v3.ipynb:

Modelo LSTM entrenado para predecir métricas de red en ventanas de tiempo.

Curvas de entrenamiento (loss/val_loss) y predicciones frente a valores reales.

Autoría:

Estos notebooks fueron desarrollados como parte de un trabajo aplicado en ML y DL para operaciones de red, mostrando cómo aplicar IA para análisis proactivo y forecasting de métricas.



## Descripción General Troubleshooting Agent Folder

En este folder encontraran el codigo del agente (basado en langgraph) y el front-end del chatbor (streamlit).
Para iniciarlo ejecutar el comando: streamlit run main.py dentro del directorio "troubleshooting_agent".

Ten en cuenta que para interactuar con el NSO y por ende para obtener informacion en tiempo real del entorno de red tendras que tenerlo configurado por separado (no se incluye en este proyecto).

De igual forma las credenciales se deberian poder cargar desde un file dentro del folder denominado .env (en este caso vacio).
Dentro de ese archivo tienes que configurar tus variables y credenciales. El codigo carga las siguientes variables:
- OPENAI_API_KEY
- NSO_USER
- NSO_PWD
- NSO_URL
- DATABASE_URL
- LANGSMITH_TRACING
- LANGSMITH_API_KEY
- LANGSMITH_ENDPOINT
- LANGSMITH_PROJECT
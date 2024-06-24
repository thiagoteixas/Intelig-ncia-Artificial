# -*- coding: utf-8 -*-
"""Kmeans.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JUl4MfT6qZW80B90loLn-EkFW2csmlBZ
"""

!pip install plotly --upgrade
!pip install kneed # To install only knee-detection algorithm

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy as sp
from kneed import DataGenerator, KneeLocator #para mostrar o número de grupos ideal do agrupamento
from sklearn.cluster import KMeans #Importando a função Kmeans
from sklearn.preprocessing import StandardScaler #Função utilizada para normalização dos dados
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler #Função utilizada para normalização dos dados

import pandas as pd
base= pd.read_csv('Iris.csv', sep=',',encoding='cp1252')
print(base)

"""Identificamos o Z-score ( segundo link abaixo ) para determinar outliers

https://docs.oracle.com/cloud/help/pt_BR/pbcs_common/PFUSU/insights_metrics_Z-Score.htm#PFUSU-GUID-640CEBD1-33A2-4B3C-BD81-EB283F82D879
"""

entries_zscores = base.iloc[:, 0:4].apply(sp.stats.zscore)
print(entries_zscores)

"""Outliers contém z-scores maior que 3 ou menor que -3, então separamos estas entradas."""

outliers = (entries_zscores.abs() > 3).any(axis=1)
print(base[outliers])

"""Normalizando os dados"""

minmax_scaler = MinMaxScaler()
normalized_base = pd.DataFrame(minmax_scaler.fit_transform(base.iloc[:, :-1]), columns=base.columns[:-1])
normalized_base['class'] = base['class']
print(normalized_base)

"""#Elbow

Encontrar o número de clusteres ideal.
O método Elbow é utilizado para determinar o número ideal de clusters em um conjunto de dados. Ele faz isso ao traçar a soma dos erros quadráticos (sum of squared errors, SSE) ou inércia para diferentes valores de
𝑘(número de clusters). A SSE é definida como a soma das distâncias ao quadrado entre cada ponto de dados e o centroide do seu cluster mais próximo.


"""

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, random_state = 42)
    kmeans.fit(normalized_base.iloc[:, :-1])
    wcss.append(kmeans.inertia_)

# Plotando o gráfico
elbow_normalized_base = normalized_base.copy()
elbow_nor
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o')
plt.xlabel('Número de Clusters')
plt.ylabel('Soma dos quadrados dos erros')
plt.title('Elbow')
plt.show()

"""Aplicando K-means com k = 3 ( número onde temos a "dobra do cotovelo" no gráfico )"""

kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(normalized_base.iloc[:, :-1])

"""# Silhouette

O método Silhouette é uma maneira de avaliar a qualidade do agrupamento medindo o quão semelhante cada ponto de dados é ao seu próprio cluster (coesão) em comparação com outros clusters (separação). A pontuação silhouette para um ponto de dados é calculada como:

S(i) = (b(i) - a(i)) / max(a(i), b(i))

Onde:

* S(i) é a pontuação silhouette do ponto de dados i;
* a é a distância média intra-cluster, ou seja a distância média de cada ponto dentro do cluster;
* b é a distância média inter-cluster, ou seja a distância média de todos os clusteres
"""

silhouette_media = silhouette_score(normalized_base.iloc[:, :-1], clusters)
print(silhouette_media)

aux_normalized_base = normalized_base.copy()
aux_normalized_base['cluster'] = clusters
aux_normalized_base['true_class'] = base['class']

"""Média de cada cluster"""

cluster_means = aux_normalized_base.drop(columns=['class', 'true_class']).groupby('cluster').mean()
print(cluster_means)

plt.figure(figsize=(10, 6))
plt.scatter(aux_normalized_base['sepallength'], aux_normalized_base['sepalwidth'], c=aux_normalized_base['cluster'], cmap='viridis', marker='o', label='Cluster correto')
plt.scatter(incorrectly_clustered['sepallength'], incorrectly_clustered['sepalwidth'], c='red', marker='x', label='Cluster incorreto')

"""#Calinski Harabasz

A métrica Calinski-Harabasz é utilizada para avaliar a qualidade dos clusters gerados pelo K-Means. Essa métrica mede a relação entre a dispersão dentro dos clusters e a dispersão entre os clusters. Quanto maior o valor do índice Calinski-Harabasz, melhor é a separação entre os clusters.

A fórmula do índice Calinski-Harabasz (CHi) é dada por:

CHi = ( B(K)/W(K) ) x ( N-K / K-1 )
"""

normalized_base

from sklearn.metrics import calinski_harabasz_score

calinski_harabasz_scores = []

for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    clusters = kmeans.fit_predict(normalized_base.iloc[:, :-1])
    score = calinski_harabasz_score(normalized_base.iloc[:, :-1], clusters)
    calinski_harabasz_scores.append(score)

ch_normalized_base = normalized_base.copy()
ch_normalized_base['cluster'] = clusters
ch_normalized_base['true_class'] = base['class']

incorrectly_clustered = ch_normalized_base[ch_normalized_base['cluster'] != ch_normalized_base['true_class'].map({'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2})]
plt.figure(figsize=(10, 6))
plt.scatter(ch_normalized_base['sepallength'], ch_normalized_base['sepalwidth'], c=ch_normalized_base['cluster'], cmap='viridis', marker='o', label='Cluster correto')
plt.scatter(incorrectly_clustered['sepallength'], incorrectly_clustered['sepalwidth'], c='red', marker='x', label='Cluster incorreto')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('Visualização de Agrupamentos Incorretos')
plt.legend()
plt.show()

plt.plot(range(2, 11), calinski_harabasz_scores, marker='o')
plt.xlabel('Número de Clusters')
plt.ylabel('Índice Calinski-Harabasz')
plt.title('Método Calinski-Harabasz')
plt.show()

"""# Relatório

Etapas de Pré-processamento:
- Carregamento dos Dados:

Utilizamos dados de amostra da base Iris com os primeiros 20 exemplos.
- Normalização dos Dados:

Normalizamos os dados utilizando Min-Max Scaling para trazer os valores para o intervalo [0, 1].

- Clusterização com K-means:

Aplicamos o algoritmo K-means para agrupar os dados em 3 clusters.
* Avaliação dos Agrupamentos:
 - Pontuação Silhouette:

Calculamos a pontuação Silhouette para avaliar a coesão e separação dos clusters.




Índice Calinski-Harabasz:

Calculamos o índice Calinski-Harabasz para avaliar a qualidade da separação dos clusters.


* Resultados:

Identificamos instâncias que foram agrupadas incorretamente pelo K-means em relação às classes reais.
A visualização mostrou que a maioria das instâncias foram agrupadas incorretamente.
"""


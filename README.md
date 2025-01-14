# IA : Détection d'Anomalies dans les Logs

Ce projet a pour objectif d'analyser des logs récupérés depuis Elasticsearch afin d'identifier des anomalies. Le processus repose sur un pipeline complet qui prépare les données et utilise des algorithmes d'apprentissage automatique pour détecter des comportements inhabituels dans les logs.

---

## Description du Projet

### 1. **Récupération des Logs**
Les logs sont extraits avec l'utilisation de logstash puis extraits avec Elasticsearch et sauvegardés dans un fichier `.csv`. Ce fichier contient toutes les informations nécessaires à l'analyse, comme les colonnes numériques ou catégoriques qui seront traitées dans les étapes suivantes.

### 2. **Encodage des Données (One-Hot Encoding)**
Les colonnes contenant des données catégoriques sont transformées en colonnes binaires grâce à la méthode **One-Hot Encoding** de Scikit-learn. Cette transformation permet aux modèles d'apprentissage automatique de traiter correctement les catégories sous forme numérique.

### 3. **Détection des Anomalies**

L'Isolation Forest est un algorithme de machine learning utilisé pour la détection d'anomalies. Son objectif principal est d'isoler les points de données atypiques (anomalies) dans un dataset. L'idée derrière l'Isolation Forest repose sur le fait que les anomalies sont plus faciles à isoler que les points normaux, car elles sont rares et différentes des autres observations.

Nous avons choisi ce modéle car contrairement à d'autres techniques de détection d'anomalies, l'Isolation Forest est capable de gérer de grands volumes de données avec un faible coût de calcul.
Il fonctionne sur des données multidimensionnelles, qu'elles soient numériques, catégoriques (avec un encodage approprié), ou mixtes.
L'Isolation Forest exploite la rareté et la dissimilarité des anomalies pour les détecter, ce qui en fait un choix naturel pour des applications comme l'analyse de logs.

### 4. **Résultats et Exportation**

- Les prédictions de l'algorithme sont ajoutées sous forme de colonne supplémentaire dans le fichier d'origine.
- Les anomalies sont indiquées par une valeur `-1`, tandis que les données normales sont marquées par `1`.
- Les résultats finaux sont exportés dans un fichier nommé `logs_with_anomalies.csv`, qui inclut les logs originaux ainsi que les annotations des anomalies.

---

## Fonctionnement du Script Python

### Aperçu du Code

```python
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Charger les logs
file_path = "logs.csv"  
logs_df = pd.read_csv(file_path)

# One-Hot Encoding
onehot_encoder = OneHotEncoder(handle_unknown='ignore')
preprocessor = ColumnTransformer(
    transformers=[
        ('onehot', onehot_encoder, ['log.file.path', 'message', 'event.original']) # Choix des colonnes
    ]
)

# Transformer les données avec One-Hot Encoding
encoded_array = preprocessor.fit_transform(logs_df)
encoded_df = pd.DataFrame(
    encoded_array.toarray(),
    columns=preprocessor.named_transformers_['onehot'].get_feature_names_out(['log.file.path', 'message', 'event.original'])
)

# Exporter les 500 premières lignes du fichier One-Hot Encoding pour vérifier
encoded_output_file = "log2s_onehot_encoded.csv"
encoded_df.head(500).to_csv(encoded_output_file, index=False)

# Utilisation de IsolationForest pour la détection d'anomalies
pipeline = make_pipeline(
    preprocessor,
    IsolationForest(contamination=0.05, random_state=42)  # Détection d'anomalies
)

# Entraînement du modèle
pipeline.fit(logs_df)

# Faire des prédictions (1: normal, -1: anomalie)
logs_df['anomaly'] = pipeline.predict(logs_df)

# Ajouter une colonne pour indiquer les anomalies avec un message sur le fichier csv
logs_df['anomaly_message'] = logs_df['anomaly'].apply(lambda x: "Anomalie détectée" if x == -1 else "Normal")

# Séparer les anomalies pour examen
anomalies = logs_df[logs_df['anomaly'] == -1]

# Exporter les résultats dans un fichier CSV
output_file = "logs_with_anomalies.csv"
logs_df.to_csv(output_file, index=False)

# Résumé des anomalies
total_logs = len(logs_df)
total_anomalies = len(anomalies)
print(f"Total de logs : {total_logs}")
print(f"Total d'anomalies détectées : {total_anomalies}")
print(f"Résultats exportés dans le fichier : {output_file}")
print(f"Fichier One-Hot Encoded (500 premières lignes) exporté : {encoded_output_file}")

```
**Fonctionnement du code**
Chargement des données : on charge les logs depuis un fichier CSV appelé logs.csv dans un DataFrame Pandas nommé logs_df.

One-hot-encoding : on transforme les colonnes catégoriques spécifiées (log.file.path, message, event.original) en plusieurs colonnes binaires (0 ou 1), où chaque colonne représente une valeur unique d'origine.

Transformation des données : La fonction transforme les colonnes spécifiées en une matrice avec l'encodage One-Hot.


Export du one-hot-encoding: Les 500 premières lignes du DataFrame encodé sont exportées dans un fichier CSV appelé log2s_onehot_encoded.csv pour vérifier.
Pipeline : La pipeline combine le prétraitement (one-hot-encoding) avec le modèle Isolation Forest.

Prédiction des anomalies : 1 si le log est considéré comme normal, -1 si le log est considéré comme une anomalie.

---

## Fichiers du Projet

- `logs.csv` : Fichier de logs initial contenant les données brutes.
- `logs_with_anomalies.csv` : Fichier final contenant les anomalies annotées.
-  `log2s_onehot_encoded.csv` : Fichier contenant l'encoding One hot.

---

## Instructions d'Utilisation

1. **Installer les Prérequis** :
   ```bash
   pip install pandas scikit-learn
   ```

2. **Exécuter le Script** :
   ```bash
   python3 iasiem3.py
   ```

   ![image](https://github.com/user-attachments/assets/69ba2d15-3700-4746-9f9c-d7730a7ef8bf)

3. **Vérifier les Résultats** :
   - Le fichier `logs_with_anomalies.csv` contiendra les résultats finaux avec une colonne `anomaly` et des annotations textuelles (`Normal` ou `Anomalie détectée`).

     <img width="316" alt="Capture d’écran 2025-01-14 à 09 22 36" src="https://github.com/user-attachments/assets/5f18be9a-7896-4a8d-a0d0-0023beeb8cca" />

---

## Améliorations Possibles

- Intégrer une visualisation des anomalies avec des outils comme Matplotlib ou Seaborn.
- Automatiser le pipeline complet avec une connexion directe à Elasticsearch pour traiter les données en temps réel.
- Discrimination des alertes légitime.
-Adoption des règles firewall.


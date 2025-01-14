# IA : Détection d'Anomalies dans les Logs

Ce projet a pour objectif d'analyser des logs récupérés depuis Elasticsearch afin d'identifier des anomalies. Le processus repose sur un pipeline complet qui prépare les données et utilise des algorithmes d'apprentissage automatique pour détecter des comportements inhabituels dans les logs.

---

## Description du Projet

### 1. **Récupération des Logs**
Les logs sont extraits depuis Elasticsearch et sauvegardés dans un fichier `.csv`. Ce fichier contient toutes les informations nécessaires à l'analyse, comme les colonnes numériques ou catégoriques qui seront traitées dans les étapes suivantes.

### 2. **Prétraitement des Données**
Le prétraitement des données est réalisé à l'aide d'un script Python qui suit les étapes suivantes :

- **Chargement des Données** : Les logs sont importés dans un DataFrame Pandas.

### 3. **Encodage des Données (One-Hot Encoding)**
Les colonnes contenant des données catégoriques sont transformées en colonnes binaires grâce à la méthode **One-Hot Encoding** de Scikit-learn. Cette transformation permet aux modèles d'apprentissage automatique de traiter correctement les catégories sous forme numérique.

### 4. **Détection des Anomalies**
L’algorithme **Isolation Forest** est utilisé pour calculer un score d’anomalie pour chaque observation. Cet algorithme fonctionne en isolant les données de manière récursive, en choisissant une variable et un seuil de coupure au hasard, afin d'évaluer la facilité avec laquelle une observation peut être isolée. Cela permet d’identifier efficacement les anomalies potentielles dans le dataset.

**Choix du Modèle** : Isolation Forest a été choisi pour sa capacité à traiter les données non étiquetées et à détecter des anomalies même dans des jeux de données de grande taille. Son taux de contamination est configuré à 5 %, ce qui correspond à une hypothèse réaliste dans la majorité des cas d'analyse de logs.

### 5. **Résultats et Exportation**
- Les prédictions de l'algorithme sont ajoutées sous forme de colonne supplémentaire dans le fichier d'origine.
- Les anomalies sont indiquées par une valeur `-1`, tandis que les données normales sont marquées par `1`.
- Les résultats finaux sont exportés dans un fichier nommé `logs_with_anomalies.csv`, qui inclut les logs originaux ainsi que les annotations des anomalies. Ces prédictions sont validées pour leur pertinence, en vérifiant les cas extrêmes et en les corrélant avec les logs réels pour assurer leur fiabilité.

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

- **Encodage** : Les colonnes `log.file.path`,`message`,`event.original` sont transformées en variables numériques grâce au One-Hot Encoding.
- **Détection des Anomalies** : Isolation Forest identifie les anomalies avec un seuil de contamination défini à 5 %.
- **Exportation des Résultats** : Le fichier final inclut les logs originaux avec une colonne supplémentaire pour les anomalies.

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


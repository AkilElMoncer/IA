# Projet de Détection d'Anomalies à Partir de Logs

Ce projet vise à analyser des logs récupérés depuis Elasticsearch pour en extraire des anomalies. Le processus de traitement des données est effectué en plusieurs étapes, depuis la récupération des logs jusqu'à l'application de techniques d'apprentissage automatique pour détecter des anomalies.

## Description du Processus

### 1. **Récupération des Logs**
Les logs ont été récupérés depuis Elasticsearch et ont été sauvegardés dans un fichier `.csv`. Ce fichier contient toutes les données nécessaires pour l’analyse.

### 2. **Prétraitement des Données**
Une fois les logs collectés, un script Python a été utilisé pour charger et préparer ces données avant leur analyse. Voici les étapes clés du prétraitement :

- **Chargement des Données** : Les logs sont chargés dans un DataFrame Pandas à partir du fichier CSV.
- **Nettoyage des Données** : Les valeurs manquantes ou incorrectes sont traitées (par exemple, remplacement des valeurs manquantes par des moyennes ou suppression des lignes erronées).

### 3. **One-Hot Encoding**
Pour préparer les données à l'analyse, une technique appelée "One-Hot Encoding" a été appliquée aux variables catégorielles. Cette méthode transforme chaque catégorie en une nouvelle colonne binaire, ce qui est essentiel pour les algorithmes d'apprentissage automatique qui ne peuvent pas traiter directement les données sous forme de texte.

Par exemple, si une variable "status" a les valeurs possibles ["OK", "Warning", "Error"], l'encodage one-hot transforme cette variable en trois nouvelles colonnes : `status_OK`, `status_Warning`, et `status_Error`. Chaque colonne contient 1 si la ligne correspond à cette catégorie, sinon 0.

### 4. **Détection des Anomalies**
Une fois les données préparées, nous avons utilisé un algorithme pour détecter des anomalies dans les logs. Cet algorithme identifie des événements ou comportements qui dévient des tendances habituelles dans les données.

Les anomalies détectées sont ensuite enregistrées dans un nouveau fichier CSV contenant à la fois les logs et les anomalies détectées pour chaque ligne.

### 5. **Sortie des Résultats**
Les résultats finaux sont enregistrés dans un fichier `logs2_with_anomalies.csv`, qui contient les logs originaux ainsi que les anomalies détectées par l'algorithme.

## Code Python

### Explication du Code

Voici un résumé du fonctionnement principal du code :

```python
# Chargement des bibliothèques nécessaires
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import IsolationForest

# Chargement du fichier de logs
logs_df = pd.read_csv("logs.csv")

# Prétraitement des données : application du One-Hot Encoding sur les variables catégorielles
encoder = OneHotEncoder()
encoded_data = encoder.fit_transform(logs_df[['status', 'event_type']])

# Ajout des colonnes encodées au DataFrame original
logs_df_encoded = pd.concat([logs_df, pd.DataFrame(encoded_data.toarray())], axis=1)

# Détection des anomalies à l'aide de l'algorithme Isolation Forest
model = IsolationForest(contamination=0.05)
anomalies = model.fit_predict(logs_df_encoded)

# Ajout des anomalies détectées au DataFrame
logs_df['anomaly'] = anomalies

# Sauvegarde des résultats dans un fichier CSV
logs_df.to_csv("logs2_with_anomalies.csv", index=False)
```

- **Chargement des bibliothèques** : Nous utilisons Pandas pour la gestion des données, `OneHotEncoder` de scikit-learn pour l'encodage des variables catégorielles et `IsolationForest` pour la détection des anomalies.
- **One-Hot Encoding** : Cette étape transforme les colonnes catégorielles en variables numériques adaptées pour l'apprentissage automatique.
- **Isolation Forest** : C'est un modèle d'apprentissage non supervisé qui est efficace pour identifier les anomalies dans des ensembles de données volumineux.
- **Sauvegarde des Résultats** : Les anomalies sont ajoutées au DataFrame original et le résultat est sauvegardé dans un nouveau fichier CSV.


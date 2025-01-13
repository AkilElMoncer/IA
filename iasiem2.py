import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Charger les logs
file_path = "logs.csv"  # Remplacez par le chemin de votre fichier
logs_df = pd.read_csv(file_path)

# Créer le préprocesseur pour One-Hot Encoding
preprocessor = ColumnTransformer(
    transformers=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'), ['log.file.path', 'message', 'event.original'])
    ]
)

# Créer le pipeline pour la détection d'anomalies
pipeline = make_pipeline(
    preprocessor,
    IsolationForest(contamination=0.05, random_state=42)  # Détection d'anomalies
)

# Entraîner le modèle
pipeline.fit(logs_df)

# Faire des prédictions (1: normal, -1: anomalie)
logs_df['anomaly'] = pipeline.predict(logs_df)

# Ajouter une colonne pour indiquer les anomalies avec un message
logs_df['anomaly_message'] = logs_df['anomaly'].apply(lambda x: "Anomalie détectée" if x == -1 else "Normal")

# Séparer les anomalies pour examen
anomalies = logs_df[logs_df['anomaly'] == -1]

# Exporter les résultats dans un fichier CSV
output_file = "logs2_with_anomalies.csv"
logs_df.to_csv(output_file, index=False)

# Résumé des anomalies
total_logs = len(logs_df)
total_anomalies = len(anomalies)
print(f"Total de logs : {total_logs}")
print(f"Total d'anomalies détectées : {total_anomalies}")
print(f"Résultats exportés dans le fichier : {output_file}")

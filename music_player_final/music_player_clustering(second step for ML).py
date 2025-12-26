# ml_cluster_assigner.py
# Load embeddings from PostgreSQL, run KMeans clustering, save cluster IDs.

import psycopg2
import psycopg2.extras
import numpy as np
from sklearn.cluster import KMeans


# ============================================================
# DATABASE HELPER
# ============================================================

class Database:
    def __init__(
        self,
        host="localhost",
        port=5432,
        dbname="musicplayer",
        user="postgres",
        password="asal1234@",
    ):
        self.conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_all_embeddings(self):
        """
        Returns list of (path, embedding_list)
        Only songs with embeddings are returned.
        """
        self.cursor.execute("""
            SELECT path, features
            FROM songs
            WHERE features IS NOT NULL
              AND features->'embedding' IS NOT NULL;
        """)
        return self.cursor.fetchall()

    def save_cluster(self, path, cluster_id, embedding):
        features_dict = {
            "embedding": embedding.tolist(),   # <-- FIXED
            "cluster": int(cluster_id)
        }
    
        self.cursor.execute("""
            UPDATE songs
            SET features = %s
            WHERE path = %s;
        """, (psycopg2.extras.Json(features_dict), path))
    
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_clustering(n_clusters=5):
    db = Database()
    try:
        rows = db.get_all_embeddings()
        print(f"Found {len(rows)} songs with embeddings.")

        if len(rows) < n_clusters:
            print("Not enough songs for clustering.")
            return

        # Build matrix of embeddings
        paths = []
        X = []

        for row in rows:
            path = row["path"]
            features = row["features"]
            embedding = features["embedding"]

            paths.append(path)
            X.append(embedding)

        X = np.array(X)

        print("Running KMeans clustering...")
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(X)

        # Save cluster IDs
        for path, embedding, cluster_id in zip(paths, X, labels):
            db.save_cluster(path, cluster_id, embedding)

        # Summary
        print("\n=== CLUSTER SUMMARY ===")
        for c in range(n_clusters):
            count = sum(1 for label in labels if label == c)
            print(f"Cluster {c}: {count} songs")

        print("\nClustering complete.")

    finally:
        db.close()


if __name__ == "__main__":
    run_clustering(n_clusters=5)
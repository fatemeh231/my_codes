# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 18:30:51 2025

@author: fatemeh
"""

# ml_feature_extractor.py
# Extract MFCC features for all songs and store them in PostgreSQL (features JSONB)

import os
import psycopg2
import psycopg2.extras
import numpy as np
import librosa


# ============================================================
# DATABASE HELPER (minimal, separate from your UI code)
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

    def get_all_songs_with_features(self):
        """
        Returns list of dicts: { 'path': ..., 'features': ... }
        """
        self.cursor.execute("SELECT path, features FROM songs ORDER BY id;")
        return self.cursor.fetchall()

    def save_features(self, path, features_dict):
        """
        Store ML features in the JSONB column 'features'.
        Example features_dict:
            { "embedding": [float, float, ...] }
        """
        self.cursor.execute(
            """
            UPDATE songs
            SET features = %s
            WHERE path = %s;
        """,
            (psycopg2.extras.Json(features_dict), path),
        )
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def extract_embedding(path, sr=22050, n_mfcc=20):
    """
    Extract a 40-dimensional embedding:
    - 20 MFCC means
    - 20 MFCC standard deviations
    Returns a Python list of floats.
    """
    # Load audio
    y, sr = librosa.load(path, sr=sr, mono=True)

    # Compute MFCCs: shape (n_mfcc, time_frames)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    # Mean and std along time axis
    mfcc_mean = mfcc.mean(axis=1)
    mfcc_std = mfcc.std(axis=1)

    # Concatenate → 40-dim vector
    embedding = np.concatenate([mfcc_mean, mfcc_std])

    # Convert to plain Python list for JSON storage
    return embedding.tolist()


# ============================================================
# MAIN PIPELINE
# ============================================================

def process_all_songs():
    db = Database()
    try:
        rows = db.get_all_songs_with_features()
        print(f"Found {len(rows)} songs in database.")

        processed = 0
        skipped = 0
        failed = 0

        for row in rows:
            path = row["path"]
            features = row["features"]

            # Skip if features already exist and have an embedding
            if features is not None and isinstance(features, dict) and "embedding" in features:
                print(f"[SKIP] Already has embedding: {path}")
                skipped += 1
                continue

            # Skip if file not found
            if not os.path.exists(path):
                print(f"[MISS] File not found, skipping: {path}")
                failed += 1
                continue

            print(f"[PROC] Extracting features for: {path}")

            try:
                embedding = extract_embedding(path)
                features_dict = {
                    "embedding": embedding
                    # we can add "cluster": ... later
                }
                db.save_features(path, features_dict)
                processed += 1
                print(f"       Done. Embedding length = {len(embedding)}")
            except Exception as e:
                print(f"[ERR ] Failed for {path}: {e}")
                failed += 1

        print("\n=== SUMMARY ===")
        print(f"Processed: {processed}")
        print(f"Skipped (already had embedding): {skipped}")
        print(f"Failed / missing: {failed}")

    finally:
        db.close()


if __name__ == "__main__":
    process_all_songs()
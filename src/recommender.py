import pandas as pd

class Recommender:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)
        self.df["playlist_genre"] = self.df["playlist_genre"].str.lower().str.strip()
        self.mood_profile = {
            "happy": {"valence": (0.6, 1.0)},
            "sad": {"valence": (0.0, 0.4)},
            "energetic": {"energy": (0.7, 1.0)},
            "chill": {"energy": (0.0, 0.4)},
            "romantic": {"valence": (0.5, 0.9), "energy": (0.2, 0.6)},
            "angry": {"energy": (0.8, 1.0)},
            "neutral": {}  # fallback to genre or random
        }

    def recommend(self, mood=None, genre=None, n=10):
        filtered_df = self.df.copy()

        # Apply mood filter
        if mood in self.mood_profile and self.mood_profile[mood]:
            print(f"🔍 Filtering by mood: {mood}")
            mood_filter = self.mood_profile[mood]
            if "valence" in mood_filter:
                v_min, v_max = mood_filter["valence"]
                filtered_df = filtered_df[
                    (filtered_df["valence"] >= v_min) & (filtered_df["valence"] <= v_max)
                ]
            if "energy" in mood_filter:
                e_min, e_max = mood_filter["energy"]
                filtered_df = filtered_df[
                    (filtered_df["energy"] >= e_min) & (filtered_df["energy"] <= e_max)
                ]

        # Apply genre filter
        if genre:
            print(f"🎧 Filtering by genre: {genre}")
            filtered_df = filtered_df[
                filtered_df["playlist_genre"] == genre.lower()
            ]

        # Fallback 1: Try mood-only or genre-only
        if filtered_df.empty:
            print("⚠️ No exact match. Trying fallback...")
            if mood and self.mood_profile.get(mood):
                mood_filter = self.mood_profile[mood]
                filtered_df = self.df.copy()
                if "valence" in mood_filter:
                    v_min, v_max = mood_filter["valence"]
                    filtered_df = filtered_df[
                        (filtered_df["valence"] >= v_min) & (filtered_df["valence"] <= v_max)
                    ]
                if "energy" in mood_filter:
                    e_min, e_max = mood_filter["energy"]
                    filtered_df = filtered_df[
                        (filtered_df["energy"] >= e_min) & (filtered_df["energy"] <= e_max)
                    ]
            elif genre:
                filtered_df = self.df[self.df["playlist_genre"] == genre.lower()]

        # Fallback 2: Still nothing → random
        if filtered_df.empty:
            print("⚠️ Still nothing found. Showing random songs.")
            filtered_df = self.df.sample(n=n)

        result = filtered_df[["track_name", "track_artist", "playlist_genre"]].sample(n=min(n, len(filtered_df)))
        result = result.rename(columns={
            "track_name": "Name",
            "track_artist": "Artist",
            "playlist_genre": "Genre"
        })
        return result




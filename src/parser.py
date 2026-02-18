import spacy
from spacy.matcher import Matcher

class MoodGenreParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)

        # --- Fallback mood keywords ---
        self.moods = {
            "happy": [
                "joyful", "cheerful", "elated", "glad", "up", "ecstatic", "delighted", "overjoyed",
                "blissful", "sunny", "excited", "grateful", "lighthearted", "jolly", "content",
                "cheery", "smiling", "optimistic", "bubbly", "radiant", "hyped", "buzzing", "lit",
                "goofy", "grinning", "vibing", "in a good mood", "feelin good", "stoked", "pure", "nice", "good", "happy",
            ],
            "sad": [
                "sorrowful", "depressed", "melancholic", "down", "blue", "low", "gloomy",
                "tearful", "miserable", "hopeless", "heartbroken", "grieving", "moody",
                "lonely", "tired", "lost", "unhappy", "broken", "drained", "crying", "sadge",
                "in my feels", "emo", "not okay", "dark", "void", "raw", "pain", "ruined", "ugh", "sad"
            ],
            "angry": [
                "furious", "irate", "enraged", "mad", "annoyed", "frustrated", "pissed",
                "fuming", "agitated", "livid", "raging", "bitter", "infuriated", "tense",
                "hostile", "grumpy", "fed up", "snappy", "exploding", "done", "rage", "on edge",
                "burning", "mad af", "seething", "tilted", "bent", "blowing up", "angry"
            ],
            "romantic": [
                "loving", "tender", "intimate", "sweet", "slow", "in love", "affectionate",
                "emotional", "sensual", "caring", "cuddly", "dreamy", "crushy", "wholesome",
                "soft", "charming", "mushy", "passionate", "date", "flirty", "sappy",
                "heart eyes", "simp", "lovey-dovey", "valentine", "rosy", "slow dance", "freaky", "rizz", "rizzy", "romantic"
            ],
            "chill": [
                "relaxed", "mellow", "calm", "laid-back", "cool", "easygoing", "serene",
                "peaceful", "soft", "gentle", "loose", "casual", "vibing", "breezy", "cozy",
                "unwind", "smooth", "quiet", "zen", "chillax", "lowkey", "no stress", "laid out",
                "slowed", "kickin", "just chillin", "soft vibe", "lofi", "ambient", "chill"
            ],
            "energetic": [
                "lively", "hyper", "pumped", "upbeat", "wild", "bouncy", "excited",
                "charged", "hyped", "electrified", "amped", "motivated", "fast", "jumping",
                "dancing", "ecstatic", "ready", "thrilled", "bursting", "turnt", "fired up",
                "cranked", "banger", "go time", "insane", "explosive", "adrenaline", "energetic"
            ],
            "neutral": [
                "composed", "fine", "ok", "normal", "meh", "alright", "average", "okay",
                "nothing", "blank", "uncertain", "flat", "idle", "neutral", "plain", "default",
                "dry", "basic", "regular", "standard", "mid", "i guess", "whatever", "neutral"
            ]
        }

    # --- Genre keywords ---
        self.genres = {
            "rock": [
                "guitar", "band", "concert", "drums", "amp", "garage", "punk", "metal",
                "grunge", "headbang", "mosh", "riff", "alternative", "hard", "indie",
                "electric", "distortion", "live", "screamo", "thrash", "power chords", "raw",
                "moshpit", "underground", "angsty", "rock"
            ],
            "pop": [
                "singer", "dance", "hit", "catchy", "trending", "mainstream", "idol",
                "radio", "chorus", "vocal", "viral", "billboard", "auto-tune", "chart",
                "glam", "commercial", "melodic", "flashy", "slay", "sparkle", "aesthetic",
                "tiktok", "girl group", "boy band", "bubblegum", "glossy", "basic", "pop"
            ],
            "rap": [
                "hip-hop", "beats", "flow", "bars", "freestyle", "trap", "gangsta",
                "spit", "rhymes", "mc", "verse", "808", "real", "lyrics", "drill",
                "cypher", "rhyme", "mic", "urban", "fire", "bussin", "heat", "flex",
                "hustle", "no cap", "street", "freestyle", "hard", "vibe check", "rap"
            ],
            "latin": [
                "salsa", "bailar", "fiesta", "reggaeton", "latino", "bachata", "rumba",
                "merengue", "dance", "caliente", "spanish", "tropical", "mambo",
                "cumbia", "ritmo", "fiery", "party", "spicy", "despacito", "perreo",
                "zumba", "latin vibes", "dominican", "cuba", "romántico", "dembow", "latin"
            ],
            "r&b": [
                "soul", "rhythm", "blues", "smooth", "vocals", "love", "melody",
                "slow", "emotional", "groove", "romantic", "jazzy", "cool", "chill",
                "sensual", "deep", "vocal", "harmonies", "sweet", "vibe", "lofi",
                "aesthetic", "heart", "crying in the club", "midnight", "intimate", "r&b",
                "soft", "sadboy"
            ],
            "edm": [
                "electronic", "club", "bass", "beat drop", "synth", "trance", "techno",
                "rave", "house", "dubstep", "build-up", "drop", "festival", "vibe",
                "dj", "remix", "electro", "banger", "dancefloor", "lights", "insane",
                "plur", "energy", "neon", "blast", "glow", "euphoria", "go crazy", "edm"
            ]
        }

        self.default_genres_for_mood = {
            "happy": "pop",
            "sad": "r&b",
            "angry": "rock",
            "romantic": "r&b",
            "chill": "r&b",
            "energetic": "edm",
            "neutral": "pop",       # fallback default
        }

        self._register_patterns()

    def _generate_matcher_patterns(self, keywords_dict):
        patterns = {}
        for label, phrases in keywords_dict.items():
            label_upper = label.upper()
            patterns[label_upper] = []
            for phrase in phrases:
                pattern = [{"LOWER": token} for token in phrase.lower().split()]
                patterns[label_upper].append(pattern)
        return patterns

    def _register_patterns(self):
        mood_patterns = self._generate_matcher_patterns(self.moods)
        genre_patterns = self._generate_matcher_patterns(self.genres)

        for label, patterns in {**mood_patterns, **genre_patterns}.items():
            self.matcher.add(label, patterns)

    def parse(self, user_input):
        doc = self.nlp(user_input.lower())
        matches = self.matcher(doc)

        found_mood = None
        found_genre = None

        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id].lower()
            if not found_mood and label in self.moods:
                found_mood = label
            elif not found_genre and label in self.genres:
                found_genre = label

        # Fallback token search for mood
        if not found_mood:
            for token in doc:
                for mood, words in self.moods.items():
                    if token.text in words:
                        found_mood = mood
                        break
                if found_mood:
                    break

        # Fallback token search for genre
        if not found_genre:
            for token in doc:
                for genre, words in self.genres.items():
                    if token.text in words:
                        found_genre = genre
                        break
                if found_genre:
                    break

        # Apply fallback genre from mood
        if not found_genre and found_mood in self.default_genres_for_mood:
            found_genre = self.default_genres_for_mood[found_mood]

        # Apply fallback mood from genre
        if not found_mood:
            for mood, default_genre in self.default_genres_for_mood.items():
                if found_genre == default_genre:
                    found_mood = mood
                    break

        return found_mood, found_genre


# CLI Debugging Test
if __name__ == "__main__":
    parser = MoodGenreParser()
    while True:
        user_input = input("\n🎧 What kind of music are you in the mood for? (type 'exit' to quit)\n> ")
        if user_input.lower() == "exit":
            break
        mood, genre = parser.parse(user_input)
        print(f"🎯 Mood: {mood or 'not found'} | Genre: {genre or 'not found'}")

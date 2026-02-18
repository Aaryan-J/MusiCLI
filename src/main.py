from parser import MoodGenreParser
from recommender import Recommender

def main():
    parser = MoodGenreParser()
    recommender = Recommender("data/spotify_songs.csv")

    while True:
        user_input = input("\n🎧 What kind of music are you in the mood for? (type 'exit' to quit)\n> ")
        if user_input.lower() == "exit":
            break

        mood, genre = parser.parse(user_input)
        print(f"\n🎯 Mood: {mood if mood else 'not found'} | Genre: {genre if genre else 'not found'}")

        recs = recommender.recommend(mood=mood, genre=genre, n=10)

        print("\n🎶 Recommended Songs:\n")
        for _, row in recs.iterrows():
            print(f"🎵 {row['Name']:<35} | {row['Artist']:<25} | {row['Genre']}")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

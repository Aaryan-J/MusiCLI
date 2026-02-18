# MusiCLI

## Description
MusiCLI is a terminal-based music recommendation AI that suggests songs based on user input. It can detect mood and genre from text or choose a genre based on the user's mood, then recommends the top 10 songs using energy, genre, and other musical features. The system works entirely in the terminal, providing a lightweight, accessible music discovery experience without a graphical interface.

## Features
- **Mood and Genre Detection**: Parses user input to identify mood and preferred music genre.
- **Top 10 Recommendations**: Suggests the best songs based on mood, genre, and energy levels.
- **Terminal-Based Interaction**: Lightweight, minimal interface for fast and easy usage.
- **Logic-Driven AI**: Uses rule-based logic combined with basic music features to generate recommendations.
- **Extensible Design**: Easy to add new datasets, recommendation logic, or features in the future.

## Installation
1. Clone the repository:  
```bash
git clone https://github.com/Aaryan-J/MusiCLI.git
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the program:
```bash
python musiccli.py
```

## Usage
- Launch the program and input your mood or preferred genre.
- Examples of inputs:
  - “I feel relaxed”
  - “Play some energetic rock music”
- MusiCLI will recommend the top 10 songs matching your mood or genre.

## How It Works
1. Parses the user input to detect mood and/or genre.
2. Chooses a suitable genre if only mood is provided.
3. Scores songs based on energy, genre match, and other musical features.
4. Returns the top 10 recommendations in the terminal.

## Future Work
- Integrate with local music libraries to play songs directly.
- Enhance mood and genre detection with more advanced NLP techniques.
- Add personalization based on past interactions.
- Optionally, provide a simple GUI for visualization of recommendations.

Contributing
Contributions are welcome! You can help by adding new recommendation logic, expanding the music dataset, or improving mood/genre detection. Please follow standard Python practices when adding new modules or features.

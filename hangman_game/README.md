# Hangman Game

A comprehensive terminal-based Hangman game implemented in Python with modular architecture, featuring categories, extensive word lists, scoring system, persistent statistics, and ASCII art hangman drawings.

## 🎮 Features

- **Extensive Word Database**: 2800+ words across multiple categories
- **Category Selection**: Animals, Countries, Programming, Science, or Mixed
- **ASCII Art Hangman**: Visual hangman drawing that updates with wrong guesses
- **Scoring System**: Points based on word length and performance
- **Persistent Statistics**: Track wins, losses, scores, and win rates across sessions
- **Comprehensive Logging**: Detailed logs for each game session
- **Input Validation**: Robust handling of user input with clear error messages
- **Clean Modular Design**: Well-organized code structure following Python best practices

## 📁 Project Structure

```
hangman_game/
├── main.py                     # Entry point - run this to start the game
├── words/
│   ├── words.txt              # Combined word list (2800+ words)
│   └── categories/
│       ├── animals.txt        # Animal words
│       ├── countries.txt      # Country and location words
│       ├── programming.txt    # Programming and tech terms
│       └── science.txt        # Science and biology terms
├── game/
│   ├── engine.py             # Core game logic and state management
│   ├── wordlist.py           # Word loading and random selection
│   └── ascii_art.py          # Hangman drawings and game art
├── ui/
│   └── display.py            # User interface and display functions
├── game_log/                  # Auto-generated game logs
│   ├── game1/
│   │   └── log.txt
│   ├── game2/
│   │   └── log.txt
│   └── ...
├── statistics.json            # Auto-generated persistent statistics
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Installation & Running

1. **Download/Clone the project**:
   ```bash
   # If downloaded as zip, extract to desired location
   # If using git:
   git clone <repository-url>
   cd hangman_game
   ```

2. **Run the game**:
   ```bash
   python main.py
   ```
   
   Or on some systems:
   ```bash
   python3 main.py
   ```

That's it! The game will start immediately.

## 🎯 How to Play

### Game Flow

1. **Start the Game**: Run `python main.py`
2. **Choose Category**: Select from Animals, Countries, Programming, Science, or All Categories
3. **Guess Letters**: Enter single letters to guess
4. **Optional Word Guess**: Type 'guess' to attempt the full word
5. **Win/Lose**: Complete the word before 6 wrong guesses to win!

### Game Controls

| Input | Action |
|-------|--------|
| `a-z` | Guess a single letter |
| `guess` | Attempt to guess the full word |
| `quit` or `q` | Exit the game |
| `y`/`n` | Play again (yes/no) |

### Scoring System

- **Base Score**: Word length × 10 points
- **Penalty**: 5 points deducted per wrong guess
- **Minimum**: 10 points for any win
- **Loss**: 0 points

**Example**: 6-letter word with 2 wrong guesses = (6×10) - (2×5) = 50 points

### Categories

- **Animals**: Wildlife, pets, sea creatures, birds, insects (400+ words)
- **Countries**: Nations, cities, states, landmarks (350+ words)  
- **Programming**: Languages, frameworks, algorithms, data structures (800+ words)
- **Science**: Biology, chemistry, physics, anatomy, genetics (900+ words)
- **All Categories**: Random selection from entire database (2800+ words)

## 📊 Game Statistics

The game automatically tracks and displays:

- **Games Played**: Total number of games
- **Wins/Losses**: Win-loss record
- **Win Rate**: Percentage of games won
- **Total Score**: Accumulated points across all games
- **Average Score**: Points per game average

Statistics persist between sessions and are stored in `statistics.json`.

## 📝 Game Logging

Each game creates a detailed log in `game_log/gameN/log.txt` containing:

- Selected category and word
- All player guesses (correct and incorrect)
- Progress trace showing word completion
- Final score and statistics
- Timestamp and session notes

Example log structure:
```
Game 1 Log
Category: Programming  
Word: python
Word Length: 6
Date & Time: 2025-10-29 14:30:00

Guesses (in order):
1. p → Correct (letter)
2. y → Correct (letter)
3. z → Wrong (letter)
4. t → Correct (letter)
...

Result: Win
Points Earned: 50
Total Score: 50
```

## 🎨 ASCII Art Features

The game includes:

- **7-Stage Hangman**: Progressive drawing from empty gallows to complete hangman
- **Win/Lose Animations**: Special ASCII art for game outcomes
- **Welcome Screen**: Attractive game title display

Hangman progression:
```
Stage 0: Empty gallows
Stage 1: Head
Stage 2: Body  
Stage 3: Left arm
Stage 4: Right arm
Stage 5: Left leg
Stage 6: Right leg (Game Over)
```

## 🔧 Technical Details

### Architecture

- **Modular Design**: Separated concerns across multiple modules
- **Clean Interfaces**: Well-defined APIs between components
- **Error Handling**: Robust error handling and user feedback
- **Path Management**: Uses `pathlib` for cross-platform compatibility

### Key Classes

- `HangmanGame`: Main game controller and state management
- `WordList`: Word loading and category management
- `GameDisplay`: User interface and output formatting
- `GameStatistics`: Persistent statistics tracking
- `GameLogger`: Comprehensive game session logging
- `HangmanArt`: ASCII art management

### Data Persistence

- **Statistics**: JSON format for cross-session statistics
- **Logs**: Human-readable text logs for each game
- **Auto-Creation**: Directories and files created automatically

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors**:
- Ensure you're running from the `hangman_game` directory
- Verify all files are present in correct structure

**"No words available" errors**:
- Check that `words/words.txt` exists and contains words
- Verify category files in `words/categories/` are present

**Permission errors with logs/statistics**:
- Ensure write permissions in the game directory
- Check available disk space

### File Validation

The game includes built-in validation:
- Checks for missing word files
- Validates file permissions
- Reports specific issues with helpful messages

## 🎓 Educational Value

This project demonstrates:

- **Modular Programming**: Clean separation of concerns
- **File I/O Operations**: Reading word lists, writing logs and statistics
- **Data Structures**: Sets, lists, dictionaries for game state
- **Object-Oriented Design**: Classes with clear responsibilities  
- **Error Handling**: Graceful handling of edge cases
- **User Experience**: Intuitive interface and clear feedback
- **Documentation**: Comprehensive docstrings and comments

## 🔄 Future Enhancements

Potential improvements:
- **Difficulty Levels**: Easy/Medium/Hard with different word lengths
- **Multiplayer Support**: Two-player word selection
- **Hint System**: Category-based hints for stuck players
- **Custom Word Lists**: User-provided word files
- **GUI Version**: Graphical interface with tkinter/pygame
- **Online Leaderboards**: Compare scores with other players

## 📄 Requirements Compliance

✅ **All assignment requirements met**:

- [x] Terminal-based Hangman game
- [x] Modular Python project structure  
- [x] 1000+ words (2800+ included)
- [x] Category support (4 categories + mixed)
- [x] Letter guessing with validation
- [x] Optional full-word guessing
- [x] Win/lose conditions (6 wrong guesses max)
- [x] Progress tracking and display
- [x] ASCII-art hangman (7 stages)
- [x] Clean, readable, documented code
- [x] Scoring system
- [x] Persistent statistics
- [x] Comprehensive logging
- [x] Game runs via `main.py` only

## 📜 License

This project is created for educational purposes as part of an Advanced Python course assignment.

## 👨‍💻 Author

Advanced Python Course Assignment  
October 2025

---

**Enjoy playing Hangman! 🎉**#   p y t h o n _ h a n g m a n _ a s s i g n m e n t _ 1  
 
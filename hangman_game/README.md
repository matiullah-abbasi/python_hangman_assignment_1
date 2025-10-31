# Hangman Game

A terminal-based Hangman game implemented in Python with multiple word categories, scoring system, and game logging.

## How to Run the Game

1. **Prerequisites**: Python 3.6 or higher (no external dependencies required)

2. **Running the Game**: 
   ```bash
   cd hangman_game
   python main.py
   ```

3. **Gameplay**:
   - Choose a word category or select random
   - Guess letters one at a time
   - You have 6 wrong guesses before losing
   - Win by guessing all letters in the word

## Wordlist Format and Categories

### Word Categories Available:
- **Animals** (`words/categories/animals.txt`)
- **Countries** (`words/categories/countries.txt`) 
- **Programming** (`words/categories/programming.txt`)
- **Science** (`words/categories/science.txt`)
- **General** (`words/words.txt`) - Mixed words from all categories

### Format:
- Each word file contains one word per line
- Words are stored as plain text
- No special formatting required
- Categories are automatically detected from filenames

### Example word file structure:
```
elephant
tiger
lion
zebra
```

## Scoring Method

The scoring system calculates points based on:

1. **Base Score**: Fixed points for completing a word (varies by word length)
2. **Efficiency Bonus**: Extra points for fewer wrong guesses
   - 0 wrong guesses: Maximum bonus
   - 1-2 wrong guesses: High bonus  
   - 3-4 wrong guesses: Medium bonus
   - 5-6 wrong guesses: Low/no bonus
3. **Word Length Multiplier**: Longer words earn more points
4. **Category Difficulty**: Some categories may have scoring multipliers

### Score Calculation Example:
```
Word: "PYTHON" (6 letters, Programming category)
Wrong guesses: 2
Score = (Base: 60) + (Length bonus: 6) + (Efficiency bonus: 20) = 86 points
```

## How Logs Are Saved

### Log Structure:
```
game_log/
├── game1/
│   └── log.txt
├── game2/ 
│   └── log.txt
├── game3/
└── game4/
    └── log.txt
```

### Log Content:
Each game session creates a detailed log file containing:

1. **Game Header**: 
   - Timestamp when game started
   - Selected word and category
   - Game session number

2. **Turn-by-Turn Progress**:
   - Each letter guessed
   - Whether guess was correct or wrong
   - Current word state (e.g., "P_T_ON")
   - Number of wrong guesses so far

3. **Game Summary**:
   - Final result (Win/Loss)
   - Total guesses made
   - Final score earned
   - Game duration

### Example Log Entry:
```
=== HANGMAN GAME LOG ===
Game #: 4
Started: 2025-10-31 14:30:15
Word: PYTHON
Category: programming
Length: 6

Turn 1: Guessed 'E' - WRONG (1/6 wrong)
Turn 2: Guessed 'A' - WRONG (2/6 wrong)  
Turn 3: Guessed 'P' - CORRECT! P_____
Turn 4: Guessed 'Y' - CORRECT! PY____
Turn 5: Guessed 'T' - CORRECT! PYT___
Turn 6: Guessed 'H' - CORRECT! PYTH__
Turn 7: Guessed 'O' - CORRECT! PYTHO_
Turn 8: Guessed 'N' - CORRECT! PYTHON

GAME WON!
Total Guesses: 8
Wrong Guesses: 2/6
Score: 86 points
Duration: 2:34
Ended: 2025-10-31 14:32:49
```

### Statistics Persistence:
Game statistics are also saved in `statistics.json`:
- Total games played, wins, losses
- Win rate percentage
- Average score and total score
- Last played timestamp

This data persists between game sessions and is updated after each game.
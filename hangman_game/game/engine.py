"""
Core gameplay engine for the Hangman game.
Handles game logic, scoring, statistics, and logging functionality.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any

from game import wordlist
from game import ascii_art
from ui import display


# Global game state variables
current_word = ""
current_category = ""
guessed_letters = set()
correct_letters = set()
wrong_letters = set()
wrong_guesses = 0
max_wrong_guesses = 6
game_won = False
game_lost = False
guess_count = 0
progress_trace = []
project_root = None
stats_file = None
log_dir = None
current_game_number = 1


def initialize_game(root_path: Path) -> None:
    """
    Initialize the game with project paths.
    
    Args:
        root_path: Root directory of the project
    """
    global project_root, stats_file, log_dir, max_wrong_guesses
    
    project_root = root_path
    words_dir = project_root / "words"
    log_dir = project_root / "game_log"
    stats_file = project_root / "statistics.json"
    max_wrong_guesses = ascii_art.get_max_wrong_guesses()
    
    # Load words into memory
    wordlist.load_words(words_dir)


def reset_game_state() -> None:
    """Reset the current game state."""
    global current_word, current_category, guessed_letters, correct_letters
    global wrong_letters, wrong_guesses, game_won, game_lost, guess_count, progress_trace
    
    current_word = ""
    current_category = ""
    guessed_letters = set()
    correct_letters = set()
    wrong_letters = set()
    wrong_guesses = 0
    game_won = False
    game_lost = False
    guess_count = 0
    progress_trace = []


def load_statistics() -> Dict[str, Any]:
    """Load statistics from file or create new ones."""
    default_stats = {
        'games_played': 0,
        'wins': 0,
        'losses': 0,
        'total_score': 0,
        'win_rate': 0.0,
        'average_score': 0.0,
        'last_played': None
    }
    
    if stats_file.exists():
        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                loaded_stats = json.load(f)
                # Ensure all required keys exist
                for key, default_value in default_stats.items():
                    if key not in loaded_stats:
                        loaded_stats[key] = default_value
                return loaded_stats
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load statistics ({e}). Starting fresh.")
    
    return default_stats


def save_statistics(stats: Dict[str, Any]) -> None:
    """Save statistics to file."""
    try:
        # Create directory if it doesn't exist
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save statistics ({e})")


def update_statistics(won: bool, score: int) -> Dict[str, Any]:
    """
    Update statistics after a game.
    
    Args:
        won: Whether the player won
        score: Score earned in the game
        
    Returns:
        Updated statistics dictionary
    """
    stats = load_statistics()
    
    stats['games_played'] += 1
    if won:
        stats['wins'] += 1
    else:
        stats['losses'] += 1
    
    stats['total_score'] += score
    stats['win_rate'] = (stats['wins'] / stats['games_played']) * 100
    stats['average_score'] = stats['total_score'] / stats['games_played']
    stats['last_played'] = datetime.now().isoformat()
    
    save_statistics(stats)
    return stats


def get_next_game_number() -> int:
    """Get the next game number based on existing log directories."""
    if not log_dir.exists():
        return 1
    
    existing_games = [
        int(d.name.replace('game', ''))
        for d in log_dir.iterdir()
        if d.is_dir() and d.name.startswith('game') and d.name[4:].isdigit()
    ]
    
    return max(existing_games, default=0) + 1


def start_game_log(game_number: int) -> Path:
    """
    Start logging for a new game.
    
    Args:
        game_number: Sequential game number
        
    Returns:
        Path to the game log directory
    """
    game_dir = log_dir / f"game{game_number}"
    game_dir.mkdir(parents=True, exist_ok=True)
    return game_dir


def save_game_log(game_number: int, won: bool, score: int, stats: Dict[str, Any]) -> None:
    """
    Save the complete game log.
    
    Args:
        game_number: Game number
        won: Whether the player won
        score: Score earned
        stats: Current statistics
    """
    game_dir = log_dir / f"game{game_number}"
    log_file = game_dir / "log.txt"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = "Win" if won else "Loss"
    
    log_entries = [
        f"Game {game_number} Log",
        f"Category: {current_category.title() if current_category else 'Mixed'}",
        f"Word: {current_word}",
        f"Word Length: {len(current_word)}",
        f"Date & Time: {timestamp}",
        "",
        "Guesses (in order):"
    ]
    
    # Add guess entries (we'll track these during gameplay)
    guess_num = 1
    for letter in guessed_letters:
        if letter in correct_letters:
            log_entries.append(f"{guess_num}. {letter} → Correct (letter)")
        else:
            log_entries.append(f"{guess_num}. {letter} → Wrong (letter)")
        guess_num += 1
    
    log_entries.extend([
        "",
        f"Wrong Guesses List: {', '.join(sorted(wrong_letters)) if wrong_letters else 'None'}",
        f"Wrong Guesses Count: {wrong_guesses}",
        f"Remaining Attempts at End: {max_wrong_guesses - wrong_guesses}",
        f"Result: {result}",
        f"Points Earned: {score}",
        f"Total Score (after this round): {stats['total_score']}",
        f"Games Played: {stats['games_played']}",
        f"Wins: {stats['wins']}",
        f"Losses: {stats['losses']}",
        f"Win Rate: {stats['win_rate']:.2f}%",
        "",
        "---------------------------------------",
        "Session Notes:",
        f"- ASCII hangman reached state {wrong_guesses} after {wrong_guesses} wrong guess(es).",
        "- Progress trace:"
    ])
    
    # Add progress trace
    for i, progress in enumerate(progress_trace):
        arrow = " -> " if i > 0 else " "
        log_entries.append(f"{arrow}{progress}")
    
    log_entries.append("---------------------------------------")
    
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write('\\n'.join(log_entries))
    except IOError as e:
        print(f"Warning: Could not save game log ({e})")


def calculate_score(word_length: int, wrong_guess_count: int) -> int:
    """
    Calculate score for a won game.
    
    Args:
        word_length: Length of the word
        wrong_guess_count: Number of wrong guesses made
        
    Returns:
        Calculated score (0 if game was lost)
    """
    if game_lost:
        return 0
    
    # Base score is word length * 10
    base_score = word_length * 10
    
    # Penalty for wrong guesses (5 points per wrong guess)
    penalty = wrong_guess_count * 5
    
    # Minimum score of 10 for any win
    score = max(base_score - penalty, 10)
    
    return score


def get_word_progress() -> str:
    """
    Get current word progress with guessed letters revealed.
    
    Returns:
        Word progress string (e.g., "p y _ h _ n")
    """
    progress = []
    for letter in current_word:
        if letter in correct_letters:
            progress.append(letter)
        else:
            progress.append('_')
    
    return ' '.join(progress)


def is_word_complete() -> bool:
    """Check if the word has been completely guessed."""
    return set(current_word) <= correct_letters


def process_letter_guess(letter: str) -> str:
    """
    Process a letter guess.
    
    Args:
        letter: The guessed letter
        
    Returns:
        Result of the guess: "repeated", "correct", or "wrong"
    """
    global wrong_guesses, game_won, game_lost, guess_count
    
    letter = letter.lower()
    
    # Check for repeated guess
    if letter in guessed_letters:
        return "repeated"
    
    # Add to guessed letters
    guessed_letters.add(letter)
    guess_count += 1
    
    # Check if letter is in word
    if letter in current_word:
        correct_letters.add(letter)
        
        # Update progress trace
        progress = get_word_progress()
        progress_trace.append(progress)
        
        # Check for win condition
        if is_word_complete():
            game_won = True
        
        return "correct"
    else:
        wrong_letters.add(letter)
        wrong_guesses += 1
        
        # Update progress trace (no change but add for logging)
        progress = get_word_progress()
        progress_trace.append(f"{progress} ({letter} wrong — no progress change)")
        
        # Check for lose condition
        if wrong_guesses >= max_wrong_guesses:
            game_lost = True
        
        return "wrong"


def process_word_guess(guess: str) -> str:
    """
    Process a full word guess.
    
    Args:
        guess: The guessed word
        
    Returns:
        Result of the guess: "correct" or "wrong"
    """
    global wrong_guesses, game_won, game_lost, guess_count
    
    guess = guess.lower().replace(' ', '')
    target = current_word.replace(' ', '')
    
    guess_count += 1
    
    if guess == target:
        # Correct word guess - mark all letters as guessed
        for letter in current_word:
            if letter.isalpha():
                correct_letters.add(letter)
                guessed_letters.add(letter)
        
        game_won = True
        
        # Update progress trace
        progress = get_word_progress()
        progress_trace.append(progress)
        
        return "correct"
    else:
        # Wrong word guess
        wrong_guesses += 1
        
        # Update progress trace
        progress = get_word_progress()
        progress_trace.append(f"{progress} (word '{guess}' wrong — no progress change)")
        
        # Check for lose condition
        if wrong_guesses >= max_wrong_guesses:
            game_lost = True
        
        return "wrong"


def start_new_game(category: Optional[str] = None) -> bool:
    """
    Start a new game with the specified category.
    
    Args:
        category: Category to select word from, or None for all categories
        
    Returns:
        True if game started successfully, False otherwise
    """
    global current_word, current_category, current_game_number
    
    try:
        # Reset game state
        reset_game_state()
        
        # Get word and category
        current_word, current_category = wordlist.get_random_word(category)
        
        # Initialize progress trace
        initial_progress = get_word_progress()
        progress_trace.append(initial_progress)
        
        # Get next game number
        current_game_number = get_next_game_number()
        start_game_log(current_game_number)
        
        return True
        
    except Exception as e:
        display.display_error(f"Could not start game: {e}")
        return False


def play_game() -> None:
    """Play a single game of Hangman."""
    # Display game start
    display.display_game_start(current_category, len(current_word))
    
    # Main game loop
    while not game_won and not game_lost:
        # Display current game state
        progress = get_word_progress()
        guessed_list = list(guessed_letters)
        display.display_game_state(progress, guessed_list, wrong_guesses, max_wrong_guesses)
        
        # Get user input
        user_input = display.get_user_guess()
        
        if user_input == 'quit':
            display.display_goodbye()
            return
        
        elif user_input == 'guess':
            # Full word guess
            word_guess = display.get_full_word_guess()
            
            if word_guess == 'quit':
                display.display_goodbye()
                return
            
            result = process_word_guess(word_guess)
            
            if result == "correct":
                display.display_correct_word_guess(word_guess)
            else:
                display.display_wrong_word_guess(word_guess, wrong_guesses, max_wrong_guesses)
        
        else:
            # Letter guess
            result = process_letter_guess(user_input)
            
            if result == "repeated":
                display.display_repeated_guess(user_input)
            elif result == "correct":
                progress = get_word_progress()
                display.display_correct_guess(user_input, progress)
            else:  # wrong
                display.display_wrong_guess(user_input, wrong_guesses, max_wrong_guesses)
    
    # Game ended - display results
    end_game()


def end_game() -> None:
    """Handle end of game - display results and update statistics."""
    # Calculate score
    score = calculate_score(len(current_word), wrong_guesses)
    
    # Update statistics
    stats = update_statistics(game_won, score)
    
    # Display results
    if game_won:
        display.display_win(current_word, score, stats['total_score'])
    else:
        display.display_lose(current_word, stats['total_score'])
    
    # Display statistics
    display.display_statistics(stats)
    
    # Log game end
    save_game_log(current_game_number, game_won, score, stats)


def run_game() -> None:
    """Run the main game loop."""
    # Display welcome screen
    display.display_welcome()
    
    # Main game loop
    while True:
        try:
            # Get available categories
            categories = wordlist.get_available_categories()
            
            # Display categories and get user choice  
            display.display_categories(categories)
            chosen_category = display.get_category_choice(categories)
            
            if chosen_category == 'quit':
                break
            
            # Start new game
            if start_new_game(chosen_category):
                play_game()
            else:
                continue
            
            # Ask if user wants to play again
            if not display.ask_play_again():
                break
                
        except KeyboardInterrupt:
            print("\nGame interrupted by user.")
            break
        except Exception as e:
            display.display_error(f"Unexpected error: {e}")
            break
    
    # Display goodbye message
    display.display_goodbye()
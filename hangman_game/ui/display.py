"""
Display module for the Hangman game user interface.
Handles all game output, progress display, and user interaction.
"""

import os
from typing import List, Optional, Dict, Any
from game.ascii_art import get_hangman_stage, get_welcome_art, get_win_art, get_lose_art

# Global setting for screen clearing
clear_screen_enabled = True


def clear_screen() -> None:
    """Clear the terminal screen."""
    if clear_screen_enabled:
        os.system('cls' if os.name == 'nt' else 'clear')


def display_welcome() -> None:
    """Display the welcome screen."""
    clear_screen()
    print(get_welcome_art())
    print()


def display_categories(categories: List[str]) -> None:
    """
    Display available categories for word selection.
    
    Args:
        categories: List of available category names
    """
    print("Available Categories:")
    for i, category in enumerate(categories, 1):
        formatted_category = category.replace('_', ' ').title()
        print(f"{i}. {formatted_category}")
    print(f"{len(categories) + 1}. All Categories (Mixed)")
    print()


def get_category_choice(categories: List[str]) -> Optional[str]:
    """
    Get user's category choice.
    
    Args:
        categories: List of available categories
        
    Returns:
        Selected category name or None for all categories
    """
    while True:
        try:
            choice = input("Choose a category (enter number or name, 'quit' to exit): ").strip().lower()
            
            if choice in ['quit', 'q', 'exit']:
                return 'quit'
            
            # Try to parse as number
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    return categories[choice_num - 1]
                elif choice_num == len(categories) + 1:
                    return None  # All categories
                else:
                    print(f"Please enter a number between 1 and {len(categories) + 1}")
                    continue
            except ValueError:
                pass
            
            # Try to match category name
            for category in categories:
                if choice == category.lower() or choice == category.replace('_', ' ').lower():
                    return category
            
            if choice in ['all', 'mixed', 'any']:
                return None
            
            print("Invalid choice. Please try again.")
            
        except KeyboardInterrupt:
            print("\\nGame interrupted by user.")
            return 'quit'
        except EOFError:
            print("\\nGame interrupted.")
            return 'quit'

def display_game_start(category: Optional[str], word_length: int) -> None:
    """
    Display game start information.
    
    Args:
        category: Selected category or None for mixed
        word_length: Length of the selected word
    """
    category_name = category.replace('_', ' ').title() if category else 'Mixed'
    print(f"\nNew word selected from '{category_name}' (length {word_length})")
    print()


def display_game_state(word_progress: str, 
                      guessed_letters: List[str], 
                      wrong_guesses: int, 
                      max_wrong_guesses: int) -> None:
    """
    Display current game state.
    
    Args:
        word_progress: Current word progress (e.g., "p y _ h _ n")
        guessed_letters: List of all guessed letters
        wrong_guesses: Number of wrong guesses made
        max_wrong_guesses: Maximum allowed wrong guesses
    """
    print(f"Word: {word_progress}")
    print(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
    print(f"Remaining attempts: {max_wrong_guesses - wrong_guesses}")
    print()
    
    # Display hangman art
    hangman_art = get_hangman_stage(wrong_guesses)
    print(hangman_art)
    print()


def get_user_guess() -> str:
    """
    Get user's guess (letter or full word).
    
    Returns:
        User's guess as a string
    """
    while True:
        try:
            guess = input("Enter a letter (or type 'guess' to guess full word, 'quit' to exit): ").strip().lower()
            
            if guess in ['quit', 'q', 'exit']:
                return 'quit'
            
            if guess == 'guess':
                return 'guess'
            
            # Validate single letter input
            if len(guess) == 1 and guess.isalpha():
                return guess
            
            if len(guess) > 1:
                print("Please enter only a single letter, or type 'guess' to guess the full word.")
            elif not guess.isalpha():
                print("Please enter only letters.")
            else:
                print("Please enter a valid letter.")
            
        except KeyboardInterrupt:
            print("\\nGame interrupted by user.")
            return 'quit'
        except EOFError:
            print("\\nGame interrupted.")
            return 'quit'


def get_full_word_guess() -> str:
    """
    Get user's full word guess.
    
    Returns:
        User's full word guess
    """
    while True:
        try:
            guess = input("Enter your guess for the full word: ").strip().lower()
            
            if guess in ['quit', 'q', 'exit']:
                return 'quit'
            
            if guess and guess.replace(' ', '').isalpha():
                return guess
            
            print("Please enter a valid word (letters only).")
            
        except KeyboardInterrupt:
            print("\\nGame interrupted by user.")
            return 'quit'
        except EOFError:
            print("\\nGame interrupted.")
            return 'quit'

def display_correct_guess(letter: str, word_progress: str) -> None:
    """
    Display message for correct letter guess.
    
    Args:
        letter: The correctly guessed letter
        word_progress: Updated word progress
    """
    print(f"Correct! '{letter.upper()}' is in the word.")
    print(f"Progress: {word_progress}")
    print()


def display_wrong_guess(letter: str, wrong_guesses: int, max_wrong_guesses: int) -> None:
    """
    Display message for wrong letter guess.
    
    Args:
        letter: The incorrectly guessed letter
        wrong_guesses: Current number of wrong guesses
        max_wrong_guesses: Maximum allowed wrong guesses
    """
    print(f"Wrong! '{letter.upper()}' is not in the word.")
    print(f"Wrong guesses: {wrong_guesses}/{max_wrong_guesses}")
    print()


def display_repeated_guess(letter: str) -> None:
    """
    Display message for repeated letter guess.
    
    Args:
        letter: The repeated letter
    """
    print(f"You already guessed '{letter.upper()}'. No penalty!")
    print()


def display_correct_word_guess(word: str) -> None:
    """
    Display message for correct full word guess.
    
    Args:
        word: The correctly guessed word
    """
    print(f"Excellent! You guessed the word '{word.upper()}' correctly!")
    print()


def display_wrong_word_guess(guess: str, wrong_guesses: int, max_wrong_guesses: int) -> None:
    """
    Display message for wrong full word guess.
    
    Args:
        guess: The incorrect word guess
        wrong_guesses: Current number of wrong guesses
        max_wrong_guesses: Maximum allowed wrong guesses
    """
    print(f"Wrong! '{guess.upper()}' is not the correct word.")
    print(f"Wrong guesses: {wrong_guesses}/{max_wrong_guesses}")
    print()


def display_win(word: str, score: int, total_score: int) -> None:
    """
    Display win message and score.
    
    Args:
        word: The completed word
        score: Points earned this round
        total_score: Total score across all games
    """
    print(get_win_art())
    print(f"\nYou win! Word: {word.upper()}")
    print(f"Points earned this round: {score}")
    print(f"Total score: {total_score}")
    print()


def display_lose(word: str, total_score: int) -> None:
    """
    Display lose message.
    
    Args:
        word: The correct word that wasn't guessed
        total_score: Total score across all games
    """
    print(get_lose_art())
    print(f"\nYou lose! The word was: {word.upper()}")
    print(f"Points earned this round: 0")
    print(f"Total score: {total_score}")
    print()


def display_statistics(stats: Dict[str, Any]) -> None:
    """
    Display game statistics.
    
    Args:
        stats: Dictionary containing game statistics
    """
    print("=== GAME STATISTICS ===")
    print(f"Games played: {stats['games_played']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Win rate: {stats['win_rate']:.2f}%")
    print(f"Average score per game: {stats['average_score']:.1f}")
    print(f"Total score: {stats['total_score']}")
    print()


def ask_play_again() -> bool:
    """
    Ask user if they want to play again.
    
    Returns:
        True if user wants to play again, False otherwise
    """
    while True:
        try:
            choice = input("Would you like to play again? (y/n): ").strip().lower()
            
            if choice in ['y', 'yes', 'yeah', 'yep']:
                return True
            elif choice in ['n', 'no', 'nope']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
                
        except KeyboardInterrupt:
            print("\\nGame interrupted by user.")
            return False
        except EOFError:
            print("\\nGame interrupted.")
            return False


def display_goodbye() -> None:
    """Display goodbye message."""
    print("\nThanks for playing Hangman! Goodbye! 👋")
    print()


def display_error(message: str) -> None:
    """
    Display error message.
    
    Args:
        message: Error message to display
    """
    print(f"❌ Error: {message}")
    print()


def display_info(message: str) -> None:
    """
    Display informational message.
    
    Args:
        message: Info message to display
    """
    print(f"ℹ️  {message}")
    print()


def pause_for_user() -> None:
    """Pause and wait for user to press Enter."""
    try:
        input("Press Enter to continue...")
    except (KeyboardInterrupt, EOFError):
        pass
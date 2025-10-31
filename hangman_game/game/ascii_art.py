"""
ASCII art module for the Hangman game.
Contains hangman drawings for each stage of wrong guesses (0-6).
"""

from typing import List

# Hangman stages from 0 (no wrong guesses) to 6 (game over)
HANGMAN_STAGES = [
    # Stage 0: No wrong guesses
    """
    +---+
    |   |
        |
        |
        |
        |
    =========
    """,
    
    # Stage 1: Head
    """
    +---+
    |   |
    O   |
        |
        |
        |
    =========
    """,
    
    # Stage 2: Body
    """
    +---+
    |   |
    O   |
    |   |
        |
        |
    =========
    """,
    
    # Stage 3: Left arm
    """
    +---+
    |   |
    O   |
   /|   |
        |
        |
    =========
    """,
    
    # Stage 4: Right arm
    """
    +---+
    |   |
    O   |
   /|\\  |
        |
        |
    =========
    """,
    
    # Stage 5: Left leg
    """
    +---+
    |   |
    O   |
   /|\\  |
   /    |
        |
    =========
    """,
    
    # Stage 6: Right leg (Game Over)
    """
    +---+
    |   |
    O   |
   /|\\  |
   / \\  |
        |
    =========
    """
]

# Game state art
WIN_ART = """
🎉 CONGRATULATIONS! 🎉
    You Won!
    
    \\    o    /
     \\   |   /
      \\  |  /
       \\ | /
        \\|/
        /|\\
       / | \\
      /  |  \\
     /   |   \\
    /    o    \\
"""

LOSE_ART = """
    💀 GAME OVER 💀
    You Lost!
    
    Better luck next time!
"""

WELCOME_ART = """
╔══════════════════════════════╗
║        HANGMAN GAME          ║
║                              ║
║     Can you guess the        ║
║        word in time?         ║
╚══════════════════════════════╝
"""


def get_hangman_stage(wrong_guesses: int) -> str:
    """
    Get the hangman ASCII art for the current number of wrong guesses.
    
    Args:
        wrong_guesses: Number of wrong guesses (0-6)
        
    Returns:
        ASCII art string for the hangman stage
        
    Raises:
        ValueError: If wrong_guesses is not in valid range
    """
    if not 0 <= wrong_guesses <= 6:
        raise ValueError(f"Wrong guesses must be between 0 and 6, got {wrong_guesses}")
    
    return HANGMAN_STAGES[wrong_guesses].strip()


def get_all_stages() -> List[str]:
    """
    Get all hangman stages.
    
    Returns:
        List of all hangman ASCII art stages
    """
    return [stage.strip() for stage in HANGMAN_STAGES]


def get_max_wrong_guesses() -> int:
    """
    Get the maximum number of wrong guesses before game over.
    
    Returns:
        Maximum wrong guesses (6)
    """
    return len(HANGMAN_STAGES) - 1


def is_game_over(wrong_guesses: int) -> bool:
    """
    Check if the game is over based on wrong guesses.
    
    Args:
        wrong_guesses: Number of wrong guesses
        
    Returns:
        True if game is over, False otherwise
    """
    return wrong_guesses >= get_max_wrong_guesses()


def get_win_art() -> str:
    """Get win celebration art."""
    return WIN_ART.strip()


def get_lose_art() -> str:
    """Get game over art."""
    return LOSE_ART.strip()


def get_welcome_art() -> str:
    """Get welcome screen art."""
    return WELCOME_ART.strip()
#!/usr/bin/env python3
"""
Hangman Game - Main Entry Point

A terminal-based Hangman game with modular Python project structure.
Features categories, extensive wordlist, scoring, persistent statistics, 
and ASCII-art hangman drawings.

Author: Advanced Python Assignment
Date: October 2025
"""

import sys
from pathlib import Path

# Add the project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from game.engine import initialize_game, run_game
except ImportError as e:
    print(f"Error importing game modules: {e}")
    print("Please ensure all required modules are in the correct directories.")
    sys.exit(1)


def main():
    """
    Main entry point for the Hangman game.
    
    This function serves as the top-level controller, initializing
    the game and starting the main game loop.
    """
    try:
        # Initialize the game with project root
        initialize_game(PROJECT_ROOT)
        
        # Run the main game loop
        run_game()
        
    except KeyboardInterrupt:
        print("\\n\\nGame interrupted by user. Goodbye!")
        
    except Exception as e:
        print(f"\\nFatal error occurred: {e}")
        print("Please report this issue if it persists.")
        sys.exit(1)


if __name__ == "__main__":
    main()
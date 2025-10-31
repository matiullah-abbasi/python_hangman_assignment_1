"""
Word loading and selection module for the Hangman game.
Handles loading words from files and random selection by category.
"""

import random
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Global variables to store loaded words
_all_words = []
_category_words = {}
_categories = {
    'animals': 'animals.txt',
    'countries': 'countries.txt', 
    'programming': 'programming.txt',
    'science': 'science.txt'
}


def load_words(words_dir: str) -> None:
    """
    Load words from various word files into memory.
    
    Args:
        words_dir: Path to the words directory containing word files
    """
    global _all_words, _category_words
    
    # Convert to Path object if needed
    from pathlib import Path
    words_path = Path(words_dir)
    
    # Load main word list
    main_words_file = words_path / 'words.txt'
    if main_words_file.exists():
        with open(main_words_file, 'r', encoding='utf-8') as f:
            _all_words = [word.strip().lower() for word in f.readlines() if word.strip()]
    
    # Load category-specific words
    categories_dir = words_path / 'categories'
    if categories_dir.exists():
        for category, filename in _categories.items():
            category_file = categories_dir / filename
            if category_file.exists():
                with open(category_file, 'r', encoding='utf-8') as f:
                    words = [word.strip().lower() for word in f.readlines() if word.strip()]
                    _category_words[category] = words


def get_available_categories() -> List[str]:
    """
    Get list of available categories.
    
    Returns:
        List of category names
    """
    return list(_category_words.keys())


def get_random_word(category: Optional[str] = None) -> Tuple[str, str]:
    """
    Get a random word from the specified category or all words.
    
    Args:
        category: Category name to select from, or None for all words
        
    Returns:
        Tuple of (selected_word, actual_category)
        
    Raises:
        ValueError: If category doesn't exist or no words available
    """
    if category is None:
        # Select from all words
        if not _all_words:
            raise ValueError("No words available")
        
        word = random.choice(_all_words)
        # Try to determine category
        actual_category = determine_category(word)
        return word, actual_category
    
    else:
        # Select from specific category
        category = category.lower()
        if category not in _category_words:
            raise ValueError(f"Category '{category}' not found")
        
        category_words = _category_words[category]
        if not category_words:
            raise ValueError(f"No words available in category '{category}'")
        
        word = random.choice(category_words)
        return word, category


def determine_category(word: str) -> str:
    """
    Determine which category a word belongs to.
    
    Args:
        word: The word to categorize
        
    Returns:
        Category name or 'mixed' if not found in specific category
    """
    for category, words in _category_words.items():
        if word in words:
            return category
    return 'mixed'


def get_word_count(category: Optional[str] = None) -> int:
    """
    Get the number of words in a category or total.
    
    Args:
        category: Category name or None for total count
        
    Returns:
        Number of words
    """
    if category is None:
        return len(_all_words)
    
    category = category.lower()
    if category in _category_words:
        return len(_category_words[category])
    
    return 0


def validate_word_files(words_dir: Path) -> Dict[str, bool]:
    """
    Validate that all word files exist and are readable.
    
    Args:
        words_dir: Path to the words directory
        
    Returns:
        Dictionary mapping file names to existence status
    """
    validation_results = {}
    
    # Check main words file
    main_file = words_dir / 'words.txt'
    validation_results['words.txt'] = main_file.exists() and main_file.is_file()
    
    # Check category files
    categories_dir = words_dir / 'categories' 
    for category, filename in _categories.items():
        category_file = categories_dir / filename
        validation_results[f'categories/{filename}'] = (
            category_file.exists() and category_file.is_file()
        )
    
    return validation_results
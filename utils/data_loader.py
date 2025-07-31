"""
Data loading utilities for the TV Shows Dashboard
"""

import pandas as pd
import os
from typing import Optional, Tuple
import config

def load_imdb_data() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Load IMDB data files (basics and episodes)
    
    Returns:
        Tuple of (basics_df, episodes_df) or (None, None) if files not found
    """
    try:
        # Try to load the actual IMDB files
        basics_path = config.DATA_FILES['basics']
        episodes_path = config.DATA_FILES['episodes']
        
        if os.path.exists(basics_path) and os.path.exists(episodes_path):
            print("Loading IMDB data files...")
            basics = pd.read_csv(basics_path, sep='\t', low_memory=False)
            episodes = pd.read_csv(episodes_path, sep='\t', low_memory=False)
            return basics, episodes
        else:
            print("IMDB data files not found. Using sample data...")
            return None, None
            
    except Exception as e:
        print(f"Error loading IMDB data: {e}")
        return None, None

def load_sample_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate sample data for demonstration purposes
    
    Returns:
        Tuple of (basics_df, episodes_df) with sample data
    """
    from data.sample_data import generate_sample_data
    return generate_sample_data()

def get_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Get data - either from IMDB files or generate sample data
    
    Returns:
        Tuple of (basics_df, episodes_df)
    """
    basics, episodes = load_imdb_data()
    
    if basics is None or episodes is None:
        basics, episodes = load_sample_data()
    
    return basics, episodes

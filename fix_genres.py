#!/usr/bin/env python3
"""
Quick fix for the genre visualization issue
"""

import sys
import os
sys.path.append('.')

from utils.data_loader import get_data
from utils.data_processor import process_one_season_shows

def test_genres():
    """Test genre data processing"""
    print("Testing genre data...")
    
    basics, episodes = get_data()
    df = process_one_season_shows(basics, episodes)
    
    print(f"Total shows: {len(df)}")
    print(f"Sample genres:")
    print(df['genres'].head(10))
    
    # Check for genre splitting
    print(f"\nGenres with commas: {df['genres'].str.contains(',', na=False).sum()}")
    
    # Extract primary genres
    df['primary_genre'] = df['genres'].str.split(',').str[0]
    print(f"\nTop primary genres:")
    print(df['primary_genre'].value_counts().head())

if __name__ == "__main__":
    test_genres()

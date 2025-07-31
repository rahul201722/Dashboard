"""
Data processing utilities for the TV Shows Dashboard
"""

import pandas as pd
import numpy as np
from typing import List
import config

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataframe by replacing null values and converting data types
    
    Args:
        df: Input dataframe
        
    Returns:
        Cleaned dataframe
    """
    df_clean = df.copy()
    
    # Replace various null representations with pandas NA
    for null_val in config.NULL_VALUES:
        df_clean.replace(null_val, pd.NA, inplace=True)
    
    # Convert numeric columns
    for col in config.NUMERIC_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    return df_clean

def process_one_season_shows(basics: pd.DataFrame, episodes: pd.DataFrame) -> pd.DataFrame:
    """
    Process the data to find shows with one season or less
    
    Args:
        basics: Title basics dataframe
        episodes: Episodes dataframe
        
    Returns:
        Processed dataframe with one-season shows information
    """
    # Group by parentTconst to find shows with limited episodes
    one_season_shows = episodes.groupby('parentTconst').size()
    one_season_shows = one_season_shows[one_season_shows <= config.EPISODE_THRESHOLD]
    
    # Convert to DataFrame
    one_season_shows = one_season_shows.reset_index(name='num_episodes')
    
    # Merge with basics for additional information
    one_season_info = pd.merge(
        one_season_shows, 
        basics, 
        left_on='parentTconst', 
        right_on='tconst'
    )
    
    # Clean the merged data
    one_season_info = clean_data(one_season_info)
    
    return one_season_info

def split_genres(df: pd.DataFrame, genre_column: str = 'genres') -> pd.DataFrame:
    """
    Split genres string into separate rows
    
    Args:
        df: Input dataframe
        genre_column: Name of the genre column
        
    Returns:
        Dataframe with split genres
    """
    df_exploded = df.copy()
    if genre_column in df_exploded.columns:
        # Split genres by comma and explode into separate rows
        df_exploded[genre_column] = df_exploded[genre_column].str.split(',')
        df_exploded = df_exploded.explode(genre_column)
        df_exploded[genre_column] = df_exploded[genre_column].str.strip()
    
    return df_exploded

def get_top_shows_by_metric(df: pd.DataFrame, metric: str, n: int = 10) -> pd.DataFrame:
    """
    Get top N shows by a specific metric
    
    Args:
        df: Input dataframe
        metric: Column name to sort by
        n: Number of top shows to return
        
    Returns:
        Top N shows dataframe
    """
    return df.nlargest(n, metric)

def get_shows_by_year_range(df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Filter shows by year range
    
    Args:
        df: Input dataframe
        start_year: Start year (inclusive)
        end_year: End year (inclusive)
        
    Returns:
        Filtered dataframe
    """
    return df[
        (df['startYear'] >= start_year) & 
        (df['startYear'] <= end_year)
    ]

def get_summary_stats(df: pd.DataFrame) -> dict:
    """
    Get summary statistics for the dataset
    
    Args:
        df: Input dataframe
        
    Returns:
        Dictionary with summary statistics
    """
    stats = {
        'total_shows': len(df),
        'unique_genres': df['genres'].nunique() if 'genres' in df.columns else 0,
        'year_range': {
            'min': df['startYear'].min() if 'startYear' in df.columns else None,
            'max': df['startYear'].max() if 'startYear' in df.columns else None
        },
        'avg_episodes': df['num_episodes'].mean() if 'num_episodes' in df.columns else None,
        'avg_runtime': df['runtimeMinutes'].mean() if 'runtimeMinutes' in df.columns else None
    }
    return stats

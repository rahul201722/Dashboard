"""
Sample data generator for the TV Shows Dashboard
Used when original IMDB files are not available
"""

import pandas as pd
import numpy as np
from typing import Tuple
import random

def generate_sample_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate sample IMDB-like data for demonstration purposes
    
    Returns:
        Tuple of (basics_df, episodes_df)
    """
    np.random.seed(42)  # For reproducibility
    random.seed(42)
    
    # Generate sample show titles
    show_prefixes = [
        "The Amazing", "Mystery of", "Adventures of", "Chronicles of", "Tales from",
        "Secret", "Hidden", "Lost", "Forgotten", "Modern", "Classic", "Ultimate",
        "Super", "Mega", "Dark", "Bright", "Silent", "Loud", "Fast", "Slow"
    ]
    
    show_suffixes = [
        "Detective", "Family", "Friends", "World", "City", "House", "School",
        "Hospital", "Office", "Kitchen", "Garden", "Street", "Hill", "Valley",
        "Island", "Forest", "Beach", "Mountain", "River", "Lake"
    ]
    
    genres_list = [
        "Drama", "Comedy", "Action", "Thriller", "Romance", "Horror", "Sci-Fi",
        "Fantasy", "Documentary", "Animation", "Adventure", "Crime", "Mystery",
        "Family", "Music", "Sport", "War", "Western", "Biography", "History"
    ]
    
    # Generate basics data
    n_shows = 500
    
    # Generate tconst IDs
    tconsts = [f"tt{1000000 + i:07d}" for i in range(n_shows)]
    
    # Generate show titles
    titles = []
    for i in range(n_shows):
        prefix = random.choice(show_prefixes)
        suffix = random.choice(show_suffixes)
        if random.random() > 0.3:  # 70% chance of having both prefix and suffix
            title = f"{prefix} {suffix}"
        else:
            title = random.choice(show_prefixes + show_suffixes)
        
        # Add some variation
        if random.random() > 0.8:  # 20% chance of adding a number or year
            title += f" {random.choice(['II', 'III', '2020', '2021', '2022'])}"
        
        titles.append(title)
    
    # Generate other fields
    start_years = np.random.randint(1990, 2024, n_shows)
    end_years = []
    
    for start_year in start_years:
        if random.random() > 0.3:  # 70% chance of having an end year
            end_year = start_year + random.randint(0, 2)  # Most shows end within 2 years
        else:
            end_year = None
        end_years.append(end_year)
    
    # Generate runtime (15-120 minutes)
    runtimes = np.random.normal(45, 15, n_shows)
    runtimes = np.clip(runtimes, 15, 120).astype(int)
    
    # Generate genres (1-3 genres per show)
    show_genres = []
    for _ in range(n_shows):
        num_genres = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2])[0]
        genres = random.sample(genres_list, num_genres)
        show_genres.append(','.join(genres))
    
    # Create basics DataFrame
    basics_df = pd.DataFrame({
        'tconst': tconsts,
        'titleType': ['tvSeries'] * n_shows,
        'primaryTitle': titles,
        'originalTitle': titles,  # Same as primary for simplicity
        'isAdult': [0] * n_shows,  # All non-adult content
        'startYear': start_years,
        'endYear': end_years,
        'runtimeMinutes': runtimes,
        'genres': show_genres
    })
    
    # Generate episodes data
    episodes_data = []
    
    for i, tconst in enumerate(tconsts):
        # Generate 1-20 episodes (within our threshold)
        num_episodes = random.randint(1, 20)
        
        for ep_num in range(1, num_episodes + 1):
            episode_tconst = f"tt{2000000 + len(episodes_data):07d}"
            episodes_data.append({
                'tconst': episode_tconst,
                'parentTconst': tconst,
                'seasonNumber': 1,  # All shows have only 1 season
                'episodeNumber': ep_num
            })
    
    episodes_df = pd.DataFrame(episodes_data)
    
    # Add some null values to simulate real data
    null_indices = np.random.choice(len(basics_df), size=int(0.05 * len(basics_df)), replace=False)
    basics_df.loc[null_indices, 'endYear'] = '\\N'
    
    null_indices = np.random.choice(len(basics_df), size=int(0.03 * len(basics_df)), replace=False)
    basics_df.loc[null_indices, 'runtimeMinutes'] = '\\N'
    
    null_indices = np.random.choice(len(basics_df), size=int(0.02 * len(basics_df)), replace=False)
    basics_df.loc[null_indices, 'genres'] = '\\N'
    
    # Convert columns to object type to avoid pandas warnings
    basics_df['endYear'] = basics_df['endYear'].astype('object')
    basics_df['runtimeMinutes'] = basics_df['runtimeMinutes'].astype('object')
    
    return basics_df, episodes_df

if __name__ == "__main__":
    # Test the sample data generation
    basics, episodes = generate_sample_data()
    print("Sample Basics Data:")
    print(basics.head())
    print(f"\nBasics shape: {basics.shape}")
    
    print("\nSample Episodes Data:")
    print(episodes.head())
    print(f"Episodes shape: {episodes.shape}")
    
    # Test processing
    one_season_shows = episodes.groupby('parentTconst').size()
    print(f"\nShows with episodes: {len(one_season_shows)}")
    print(f"Average episodes per show: {one_season_shows.mean():.2f}")

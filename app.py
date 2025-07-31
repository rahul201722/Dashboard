"""
TV Shows Analysis Dashboard - Main Application
A comprehensive Streamlit dashboard for analyzing one-season TV shows
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from utils.data_loader import get_data
from utils.data_processor import (
    process_one_season_shows, 
    split_genres, 
    get_summary_stats,
    get_shows_by_year_range,
    get_top_shows_by_metric
)
from utils.visualizations import (
    create_episodes_vs_year_plot,
    create_genre_distribution_plot,
    create_shows_over_time_plot,
    create_runtime_analysis_plot,
    create_interactive_scatter_plot,
    create_genre_treemap
)

# Configure Streamlit page
st.set_page_config(**config.PAGE_CONFIG)

def load_and_process_data():
    """Load and process the TV shows data"""
    try:
        with st.spinner('Loading and processing data...'):
            # Load data
            basics, episodes = get_data()
            
            # Process one-season shows
            df = process_one_season_shows(basics, episodes)
            
            # Create exploded genres version for some visualizations
            df_genres = split_genres(df)
            
            return df, df_genres
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def create_sidebar_filters(df):
    """Create sidebar filters for data exploration"""
    st.sidebar.header("🔍 Data Filters")
    
    # Year range filter
    if 'startYear' in df.columns and df['startYear'].notna().any():
        min_year = int(df['startYear'].min())
        max_year = int(df['startYear'].max())
        
        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1
        )
    else:
        year_range = (1990, 2023)
    
    # Genre filter
    if 'genres' in df.columns:
        available_genres = df['genres'].str.split(',').explode().str.strip().dropna().unique()
        selected_genres = st.sidebar.multiselect(
            "Select Genres",
            options=sorted(available_genres),
            default=[]
        )
    else:
        selected_genres = []
    
    # Episode count filter
    if 'num_episodes' in df.columns:
        max_episodes = int(df['num_episodes'].max())
        episode_range = st.sidebar.slider(
            "Episode Count Range",
            min_value=1,
            max_value=max_episodes,
            value=(1, max_episodes),
            step=1
        )
    else:
        episode_range = (1, 20)
    
    return year_range, selected_genres, episode_range

def apply_filters(df, year_range, selected_genres, episode_range):
    """Apply selected filters to the dataframe"""
    filtered_df = df.copy()
    
    # Apply year filter
    if 'startYear' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['startYear'] >= year_range[0]) & 
            (filtered_df['startYear'] <= year_range[1])
        ]
    
    # Apply genre filter
    if selected_genres and 'genres' in filtered_df.columns:
        genre_mask = filtered_df['genres'].str.contains('|'.join(selected_genres), na=False)
        filtered_df = filtered_df[genre_mask]
    
    # Apply episode count filter
    if 'num_episodes' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['num_episodes'] >= episode_range[0]) & 
            (filtered_df['num_episodes'] <= episode_range[1])
        ]
    
    return filtered_df

def display_summary_stats(df):
    """Display summary statistics in the sidebar"""
    st.sidebar.header("📊 Dataset Summary")
    
    stats = get_summary_stats(df)
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.metric("Total Shows", stats['total_shows'])
        if stats['avg_episodes']:
            st.metric("Avg Episodes", f"{stats['avg_episodes']:.1f}")
    
    with col2:
        st.metric("Unique Genres", stats['unique_genres'])
        if stats['avg_runtime']:
            st.metric("Avg Runtime", f"{stats['avg_runtime']:.0f} min")
    
    if stats['year_range']['min'] and stats['year_range']['max']:
        st.sidebar.info(f"📅 Year Range: {stats['year_range']['min']} - {stats['year_range']['max']}")

def main():
    """Main application function"""
    
    # App header
    st.title("📺 TV Shows Analysis Dashboard")
    st.markdown("""
    Explore patterns and trends in one-season TV shows. Use the sidebar to filter data 
    and discover insights about show genres, runtime, and temporal trends.
    """)
    
    # Load data
    df, df_genres = load_and_process_data()
    
    if df is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Create sidebar filters
    year_range, selected_genres, episode_range = create_sidebar_filters(df)
    
    # Apply filters
    filtered_df = apply_filters(df, year_range, selected_genres, episode_range)
    filtered_df_genres = apply_filters(df_genres, year_range, selected_genres, episode_range)
    
    # Display summary stats
    display_summary_stats(filtered_df)
    
    # Check if filtered data is empty
    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters. Please adjust your filter settings.")
        return
    
    # Main content area
    st.header("🔍 Data Overview")
    
    # Display sample data
    with st.expander("View Sample Data"):
        st.dataframe(filtered_df.head(10))
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Shows in Selection", len(filtered_df))
    
    with col2:
        if 'num_episodes' in filtered_df.columns:
            avg_episodes = filtered_df['num_episodes'].mean()
            st.metric("Avg Episodes", f"{avg_episodes:.1f}")
    
    with col3:
        if 'runtimeMinutes' in filtered_df.columns:
            avg_runtime = filtered_df['runtimeMinutes'].mean()
            st.metric("Avg Runtime", f"{avg_runtime:.0f} min")
    
    with col4:
        if 'startYear' in filtered_df.columns:
            latest_year = filtered_df['startYear'].max()
            st.metric("Latest Year", int(latest_year) if pd.notna(latest_year) else "N/A")
    
    # Visualizations
    st.header("📈 Visualizations")
    
    # Create tabs for different visualization categories
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Basic Charts", "🎭 Genre Analysis", "⏱️ Time Trends", "🎯 Interactive"])
    
    with tab1:
        st.subheader("Episodes vs Start Year")
        fig1 = create_episodes_vs_year_plot(filtered_df)
        st.pyplot(fig1)
        
        st.subheader("Top 10 Longest Runtime Shows")
        fig4 = create_runtime_analysis_plot(filtered_df)
        st.pyplot(fig4)
    
    with tab2:
        st.subheader("Genre Distribution")
        fig2 = create_genre_distribution_plot(filtered_df_genres)
        st.pyplot(fig2)
        
        st.subheader("Genre Distribution (Interactive Treemap)")
        fig_treemap = create_genre_treemap(filtered_df_genres)
        st.plotly_chart(fig_treemap, use_container_width=True)
    
    with tab3:
        st.subheader("Shows Released Over Time")
        fig3 = create_shows_over_time_plot(filtered_df)
        st.pyplot(fig3)
        
        # Additional time-based analysis
        if 'startYear' in filtered_df.columns and filtered_df['startYear'].notna().any():
            st.subheader("Shows by Decade")
            filtered_df_decade = filtered_df.copy()
            filtered_df_decade['decade'] = (filtered_df_decade['startYear'] // 10) * 10
            decade_counts = filtered_df_decade['decade'].value_counts().sort_index()
            st.bar_chart(decade_counts)
    
    with tab4:
        st.subheader("Interactive Scatter Plot")
        fig_interactive = create_interactive_scatter_plot(filtered_df)
        st.plotly_chart(fig_interactive, use_container_width=True)
        
        # Data exploration tool
        st.subheader("Data Explorer")
        if st.checkbox("Show detailed data table"):
            st.dataframe(
                filtered_df.sort_values('startYear', ascending=False) if 'startYear' in filtered_df.columns else filtered_df,
                use_container_width=True
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Source:** IMDB Dataset  
    **Dashboard Created With:** Streamlit, Pandas, Matplotlib, Seaborn, Plotly  
    **Note:** Sample data is used when original IMDB files are not available.
    """)

if __name__ == "__main__":
    main()


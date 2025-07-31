"""
Visualization utilities for the TV Shows Dashboard
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import config

# Set the style
sns.set_style(config.CHART_CONFIG['style'])
plt.rcParams['figure.figsize'] = config.CHART_CONFIG['figure_size']
plt.rcParams['figure.dpi'] = config.CHART_CONFIG['dpi']

def create_episodes_vs_year_plot(df: pd.DataFrame) -> plt.Figure:
    """
    Create scatter plot of episodes vs start year
    
    Args:
        df: Input dataframe
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=config.CHART_CONFIG['figure_size'])
    
    # Handle missing genre data or use first genre only for coloring
    if 'genres' in df.columns and df['genres'].notna().any():
        # Extract first genre for coloring to avoid cluttered legend
        df_plot = df.copy()
        df_plot['primary_genre'] = df_plot['genres'].str.split(',').str[0]
        
        # Limit to top 10 genres to avoid legend clutter
        top_genres = df_plot['primary_genre'].value_counts().head(10).index
        df_plot_filtered = df_plot[df_plot['primary_genre'].isin(top_genres)]
        
        sns.scatterplot(
            data=df_plot_filtered, 
            x='startYear', 
            y='num_episodes', 
            hue='primary_genre', 
            ax=ax, 
            palette=config.COLOR_PALETTES['primary'],
            alpha=0.7
        )
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        sns.scatterplot(
            data=df, 
            x='startYear', 
            y='num_episodes', 
            ax=ax, 
            color='steelblue',
            alpha=0.7
        )
    
    ax.set_xlabel('Start Year')
    ax.set_ylabel('Number of Episodes')
    ax.set_title('Number of Episodes vs. Start Year')
    plt.tight_layout()
    
    return fig

def create_genre_distribution_plot(df: pd.DataFrame) -> plt.Figure:
    """
    Create bar plot of genre distribution
    
    Args:
        df: Input dataframe with exploded genres
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=config.CHART_CONFIG['figure_size'])
    
    if 'genres' in df.columns and df['genres'].notna().any():
        # Filter out NaN values and get top genres
        genre_counts = df['genres'].value_counts().head(15)
        
        sns.countplot(
            y='genres', 
            data=df[df['genres'].isin(genre_counts.index)], 
            order=genre_counts.index, 
            palette=config.COLOR_PALETTES['secondary'],
            ax=ax
        )
        ax.set_xlabel('Number of Shows')
        ax.set_ylabel('Genres')
        ax.set_title('Distribution of Genres in One-Season Shows')
    else:
        ax.text(0.5, 0.5, 'No genre data available', 
                horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, fontsize=16)
        ax.set_title('Genre Distribution - No Data Available')
    
    plt.tight_layout()
    return fig

def create_shows_over_time_plot(df: pd.DataFrame) -> plt.Figure:
    """
    Create line plot of shows over time
    
    Args:
        df: Input dataframe
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=config.CHART_CONFIG['figure_size'])
    
    if 'startYear' in df.columns and df['startYear'].notna().any():
        shows_per_year = df.groupby('startYear').size().reset_index(name='counts')
        
        sns.lineplot(
            data=shows_per_year, 
            x='startYear', 
            y='counts', 
            marker='o', 
            ax=ax,
            linewidth=2,
            markersize=6
        )
        ax.set_ylabel('Number of Shows')
        ax.set_xlabel('Year')
        ax.set_title('Number of One-Season Shows Over Time')
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'No year data available', 
                horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, fontsize=16)
        ax.set_title('Shows Over Time - No Data Available')
    
    plt.tight_layout()
    return fig

def create_runtime_analysis_plot(df: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    """
    Create bar plot of longest runtime shows
    
    Args:
        df: Input dataframe
        top_n: Number of top shows to display
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=config.CHART_CONFIG['figure_size'])
    
    if 'runtimeMinutes' in df.columns and df['runtimeMinutes'].notna().any():
        top_runtime_shows = df.nlargest(top_n, 'runtimeMinutes')
        
        if len(top_runtime_shows) > 0:
            sns.barplot(
                data=top_runtime_shows, 
                x='runtimeMinutes', 
                y='primaryTitle', 
                ax=ax, 
                palette=config.COLOR_PALETTES['accent']
            )
            ax.set_xlabel('Runtime (minutes)')
            ax.set_ylabel('Show Title')
            ax.set_title(f'Top {top_n} Longest Runtime One-Season Shows')
        else:
            ax.text(0.5, 0.5, 'No runtime data available', 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax.transAxes, fontsize=16)
    else:
        ax.text(0.5, 0.5, 'No runtime data available', 
                horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, fontsize=16)
        ax.set_title('Runtime Analysis - No Data Available')
    
    plt.tight_layout()
    return fig

def create_interactive_scatter_plot(df: pd.DataFrame) -> go.Figure:
    """
    Create interactive scatter plot using Plotly
    
    Args:
        df: Input dataframe
        
    Returns:
        Plotly figure
    """
    if 'startYear' in df.columns and 'num_episodes' in df.columns:
        # Prepare data for plotting
        df_plot = df.copy()
        
        # Extract primary genre for coloring if genres exist
        if 'genres' in df.columns and df['genres'].notna().any():
            df_plot['primary_genre'] = df_plot['genres'].str.split(',').str[0]
            color_col = 'primary_genre'
        else:
            color_col = None
        
        fig = px.scatter(
            df_plot, 
            x='startYear', 
            y='num_episodes',
            color=color_col,
            hover_data=['primaryTitle', 'runtimeMinutes', 'genres'] if 'primaryTitle' in df.columns else None,
            title='Interactive: Episodes vs Start Year'
        )
        
        fig.update_layout(
            xaxis_title='Start Year',
            yaxis_title='Number of Episodes',
            hovermode='closest'
        )
        
        return fig
    else:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for scatter plot",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16)
        )
        return fig

def create_genre_treemap(df: pd.DataFrame) -> go.Figure:
    """
    Create treemap of genres using Plotly
    
    Args:
        df: Input dataframe with exploded genres
        
    Returns:
        Plotly figure
    """
    if 'genres' in df.columns and df['genres'].notna().any():
        genre_counts = df['genres'].value_counts().head(20)
        
        fig = go.Figure(go.Treemap(
            labels=genre_counts.index,
            values=genre_counts.values,
            parents=[""] * len(genre_counts),
            textinfo="label+value"
        ))
        
        fig.update_layout(title="Genre Distribution (Treemap)")
        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="No genre data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16)
        )
        return fig

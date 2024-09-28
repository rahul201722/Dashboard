import pandas as pd

# Load the dataset
basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
episodes = pd.read_csv('title.episode.tsv', sep='\t', low_memory=False)

# Group by parentTconst to find shows with 1 season or less
one_season_shows = episodes.groupby('parentTconst').size()
one_season_shows = one_season_shows[one_season_shows <= 20]  # Assuming <=10 episodes indicates 1 season

# Convert the Series to a DataFrame and rename the column
one_season_shows = one_season_shows.reset_index(name='num_episodes')

# Merge with title basics for additional information
one_season_info = pd.merge(one_season_shows, basics, left_on='parentTconst', right_on='tconst')

# Display the resulting DataFrame
print(one_season_info.head())

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data (Use the processed DataFrame `one_season_info`)
# If you saved the processed data to a CSV file, you could load it like this:
# df = pd.read_csv('one_season_shows_processed.csv')
# Assuming `one_season_info` is already available in your environment

# For the purpose of this code, we'll assume `one_season_info` is already loaded:
df = one_season_info  # Use the processed DataFrame

df.replace('\\N', pd.NA, inplace=True)

# Convert numeric columns
df['startYear'] = pd.to_numeric(df['startYear'], errors='coerce')
df['endYear'] = pd.to_numeric(df['endYear'], errors='coerce')
df['runtimeMinutes'] = pd.to_numeric(df['runtimeMinutes'], errors='coerce')

# Set the title and layout of the Streamlit app
st.title('One-Season TV Shows Analysis Dashboard')

# First Visualization: Number of Episodes vs. Start Year
st.subheader('Number of Episodes vs. Start Year')
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='startYear', y='num_episodes', hue='genres', ax=ax, palette='viridis')
ax.set_xlabel('Start Year')
ax.set_ylabel('Number of Episodes')
st.pyplot(fig)

# Second Visualization: Distribution of Genres
st.subheader('Distribution of Genres in One-Season Shows')
genre_data = df.explode('genres')
fig, ax = plt.subplots()
sns.countplot(y='genres', data=genre_data, order=genre_data['genres'].value_counts().index, palette='pastel')
ax.set_xlabel('Number of Shows')
ax.set_ylabel('Genres')
st.pyplot(fig)

# Third Visualization: Number of One-Season Shows Over Time
st.subheader('Number of One-Season Shows Over Time')
shows_per_year = df.groupby('startYear').size().reset_index(name='counts')
fig, ax = plt.subplots()
sns.lineplot(data=shows_per_year, x='startYear', y='counts', marker='o', ax=ax)
ax.set_ylabel('Number of Shows')
ax.set_xlabel('Year')
st.pyplot(fig)

# Fourth Visualization: Longest Runtime One-Season Shows
st.subheader('Longest Runtime One-Season Shows')
top_runtime_shows = df.nlargest(10, 'runtimeMinutes')
fig, ax = plt.subplots()
sns.barplot(data=top_runtime_shows, x='runtimeMinutes', y='primaryTitle', ax=ax, palette='magma')
ax.set_xlabel('Runtime (minutes)')
ax.set_ylabel('Show Title')
st.pyplot(fig)

# Fifth Visualization: Genres by Start Year
st.subheader('Genres by Start Year')
fig, ax = plt.subplots()
sns.boxplot(x='startYear', y='genres', data=genre_data, palette='coolwarm')
ax.set_xlabel('Start Year')
ax.set_ylabel('Genres')
st.pyplot(fig)

st.markdown("**Data Source:** IMDB")


# TV Shows Analysis Dashboard 📺

Interactive Streamlit dashboard analyzing one-season TV shows using IMDB data.

## Features

- Interactive visualizations with filters
- Genre and runtime analysis
- Temporal trends and patterns
- Sample data generator included

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Or use the launch script:
```bash
./run_dashboard.sh
```

## Data

Uses IMDB files (`title.basics.tsv`, `title.episode.tsv`) or generates sample data automatically.

## Structure

- `app.py` - Main dashboard
- `config.py` - Configuration
- `utils/` - Data processing and visualizations
- `data/` - Sample data generator

See `DOCUMENTATION.md` for detailed information.
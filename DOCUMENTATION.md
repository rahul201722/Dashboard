# Project Documentation

## 📁 Project Structure

```
Dashboard/
├── 📄 README.md                 # Main project documentation
├── 📄 requirements.txt          # Python dependencies
├── 📄 .gitignore               # Git ignore rules
├── 📄 setup.py                 # Setup and installation script
├── 📄 test_dashboard.py        # Test script for validation
├── 🚀 run_dashboard.sh         # Quick launch script
├── 
├── 📱 app.py                   # Main Streamlit application
├── ⚙️ config.py                # Configuration settings
├── 📓 Dashboard.ipynb          # Jupyter notebook for exploration
├── 
├── 📂 utils/                   # Utility modules
│   ├── 📄 __init__.py          # Package initializer
│   ├── 📄 data_loader.py       # Data loading utilities
│   ├── 📄 data_processor.py    # Data processing functions
│   └── 📄 visualizations.py    # Chart and plot functions
├── 
└── 📂 data/                    # Data modules
    ├── 📄 __init__.py          # Package initializer
    └── 📄 sample_data.py       # Sample data generator
```

## 🎯 Key Features Implemented

### 1. **Modular Architecture**
- Separated concerns into logical modules
- Easy to maintain and extend
- Clear separation between data, processing, and visualization

### 2. **Robust Data Handling**
- Automatic fallback to sample data when IMDB files unavailable
- Data validation and cleaning
- Error handling throughout the pipeline

### 3. **Enhanced Visualizations**
- Multiple chart types (scatter, bar, line, treemap)
- Interactive Plotly charts
- Responsive design with tabs and columns

### 4. **User Experience**
- Interactive filters (year, genre, episode count)
- Real-time data updates based on filters
- Summary statistics and key metrics
- Expandable data views

### 5. **Configuration Management**
- Centralized configuration in `config.py`
- Customizable color schemes and chart settings
- Adjustable thresholds and parameters

### 6. **Development Tools**
- Comprehensive test suite
- Setup script for easy installation
- Launch script for quick startup
- Documentation and examples

## 🔧 Configuration Options

Edit `config.py` to customize:

- **Episode Threshold**: Maximum episodes to consider "one season"
- **Color Palettes**: Chart color schemes
- **Chart Settings**: Figure sizes, DPI, styles
- **Data Paths**: Location of IMDB files

## 📊 Available Visualizations

### Basic Charts
1. **Episodes vs Start Year**: Scatter plot showing episode count trends
2. **Runtime Analysis**: Bar chart of longest runtime shows

### Genre Analysis
3. **Genre Distribution**: Bar chart of genre popularity
4. **Genre Treemap**: Interactive hierarchical view of genres

### Time Trends
5. **Shows Over Time**: Line chart of release trends
6. **Decade Analysis**: Bar chart grouped by decades

### Interactive Features
7. **Interactive Scatter**: Plotly scatter with hover details
8. **Data Explorer**: Sortable and filterable data table

## 🛠️ Development Guide

### Adding New Visualizations

1. Create function in `utils/visualizations.py`:
```python
def create_new_chart(df):
    # Your chart code here
    return fig
```

2. Import and use in `app.py`:
```python
from utils.visualizations import create_new_chart

# In main function
fig = create_new_chart(filtered_df)
st.pyplot(fig)
```

### Adding New Data Processing

1. Add function to `utils/data_processor.py`:
```python
def new_processing_function(df):
    # Processing logic
    return processed_df
```

2. Use in the main pipeline

### Customizing Sample Data

Edit `data/sample_data.py` to:
- Change the number of generated shows
- Modify genre lists
- Adjust year ranges
- Add new fields

## 🧪 Testing

Run the test suite:
```bash
python test_dashboard.py
```

Individual component tests:
```bash
# Test data generation
python -c "from data.sample_data import generate_sample_data; generate_sample_data()"

# Test data processing
python -c "from utils.data_loader import get_data; get_data()"

# Test visualization imports
python -c "from utils.visualizations import create_episodes_vs_year_plot"
```

## 🚀 Deployment Options

### Local Development
```bash
./run_dashboard.sh
```

### Manual Launch
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Cloud Deployment
The app is ready for deployment to:
- Streamlit Cloud
- Heroku
- AWS/GCP/Azure
- Docker containers

## 📈 Performance Notes

- Sample data generates 500 shows with ~5000 episodes
- Processing time: <1 second for sample data
- Memory usage: ~50MB for sample dataset
- Real IMDB data will require more resources

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the project root
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Data Loading Issues**: Check file paths in `config.py`
4. **Chart Display Problems**: Update matplotlib/plotly versions

### Debug Mode

Add to `config.py`:
```python
DEBUG = True
```

Then check console output for detailed error messages.

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Update documentation
5. Submit a pull request

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas User Guide](https://pandas.pydata.org/docs/)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [Plotly Documentation](https://plotly.com/python/)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Run the test script
3. Review error messages carefully
4. Create an issue on GitHub with full error details

#!/usr/bin/env python3
"""
Test script for the TV Shows Analysis Dashboard
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ matplotlib import failed: {e}")
        return False
    
    try:
        import seaborn as sns
        print("✅ seaborn imported successfully")
    except ImportError as e:
        print(f"❌ seaborn import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ plotly imported successfully")
    except ImportError as e:
        print(f"❌ plotly import failed: {e}")
        return False
    
    return True

def test_custom_modules():
    """Test if custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        import config
        print("✅ config imported successfully")
    except ImportError as e:
        print(f"❌ config import failed: {e}")
        return False
    
    try:
        from utils.data_loader import get_data
        print("✅ data_loader imported successfully")
    except ImportError as e:
        print(f"❌ data_loader import failed: {e}")
        return False
    
    try:
        from utils.data_processor import process_one_season_shows
        print("✅ data_processor imported successfully")
    except ImportError as e:
        print(f"❌ data_processor import failed: {e}")
        return False
    
    try:
        from utils.visualizations import create_episodes_vs_year_plot
        print("✅ visualizations imported successfully")
    except ImportError as e:
        print(f"❌ visualizations import failed: {e}")
        return False
    
    try:
        from data.sample_data import generate_sample_data
        print("✅ sample_data imported successfully")
    except ImportError as e:
        print(f"❌ sample_data import failed: {e}")
        return False
    
    return True

def test_sample_data_generation():
    """Test sample data generation"""
    print("\nTesting sample data generation...")
    
    try:
        from data.sample_data import generate_sample_data
        basics, episodes = generate_sample_data()
        
        print(f"✅ Generated {len(basics)} shows and {len(episodes)} episodes")
        print(f"✅ Basics columns: {list(basics.columns)}")
        print(f"✅ Episodes columns: {list(episodes.columns)}")
        
        return True
    except Exception as e:
        print(f"❌ Sample data generation failed: {e}")
        return False

def test_data_processing():
    """Test data processing pipeline"""
    print("\nTesting data processing...")
    
    try:
        from utils.data_loader import get_data
        from utils.data_processor import process_one_season_shows
        
        basics, episodes = get_data()
        df = process_one_season_shows(basics, episodes)
        
        print(f"✅ Processed data shape: {df.shape}")
        print(f"✅ Processed data columns: {list(df.columns)}")
        
        return True
    except Exception as e:
        print(f"❌ Data processing failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing TV Shows Analysis Dashboard")
    print("=" * 50)
    
    tests = [
        ("Basic imports", test_imports),
        ("Custom modules", test_custom_modules),
        ("Sample data generation", test_sample_data_generation),
        ("Data processing", test_data_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The dashboard should work correctly.")
        print("\nYou can now run:")
        print("streamlit run app.py")
        return 0
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    exit(main())

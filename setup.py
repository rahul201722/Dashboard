#!/usr/bin/env python3
"""
Setup script for the TV Shows Analysis Dashboard
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_data_files():
    """Check if IMDB data files exist"""
    required_files = ['title.basics.tsv', 'title.episode.tsv']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"📋 IMDB data files not found: {missing_files}")
        print("The application will use sample data for demonstration.")
        print("To use real IMDB data, download the files from:")
        print("https://datasets.imdbws.com/")
        print("- title.basics.tsv.gz")
        print("- title.episode.tsv.gz")
        print("Extract them to the project directory.")
    else:
        print("✅ IMDB data files found!")
    
    return len(missing_files) == 0

def main():
    """Main setup function"""
    print("🚀 Setting up TV Shows Analysis Dashboard...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please check the error messages above.")
        return 1
    
    # Check data files
    check_data_files()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nTo run the dashboard:")
    print("streamlit run app.py")
    print("\nTo run the Jupyter notebook:")
    print("jupyter notebook Dashboard.ipynb")
    
    return 0

if __name__ == "__main__":
    exit(main())

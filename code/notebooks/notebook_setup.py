import os
import sys
from dotenv import load_dotenv
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rcParams

# Load environment variables from .env file
load_dotenv()

# Define key environment variables

# SerpAPI key, for Google Scholar querying
SERP_API_KEY = os.getenv('SERP_API_KEY')
# Check if SERP API Key is loaded
if not SERP_API_KEY:
    raise ValueError("SerpAPI Key is not found in environment variables.")

# NCBI credentials for PubMed/Medline
NCBI_API_KEY = os.getenv('NCBI_API_KEY')
NCBI_EMAIL = os.getenv('NCBI_EMAIL')
if not NCBI_EMAIL or not NCBI_API_KEY:
    raise ValueError("NCBI API/Email is not found in environment variables.")

# Embase API key
EMBASE_API_KEY = os.getenv('EMBASE_API_KEY')
if not EMBASE_API_KEY:
    raise ValueError("Embase API Key is not found in environment variables.")

# Scopus API key
SCOPUS_API_KEY = os.getenv('SCOPUS_API_KEY')
if not SCOPUS_API_KEY:
    raise ValueError("SCOPUS API Key is not found in environment variables.")

# Web of Science API key
WOS_API_KEY = os.getenv('WOS_API_KEY')
if not WOS_API_KEY:
    raise ValueError("WOS API Key is not found in environment variables.")

# Directories
INPUT_DIR = os.getenv('INPUT_DIR') # parent input directory
OUTPUT_DIR = os.getenv('OUTPUT_DIR') # parent output directory
RAW_DATA_DIR = os.getenv('RAW_DATA_DIR') # directory for raw data
PROC_DATA_DIR = os.getenv('PROC_DATA_DIR') # directory for processed data
FIG_DIR = os.getenv('FIG_DIR') # directory for figures
SCRIPTS_DIR = os.getenv('SCRIPTS_DIR') # directory for scripts

# Add the 'scripts' directory to sys.path if it exists
if SCRIPTS_DIR and os.path.exists(SCRIPTS_DIR) and SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

# Import custom helper functions (if needed)
try:
    import helpers
except ImportError:
    raise ImportError(f"Unable to import 'helpers' from {SCRIPTS_DIR}. Ensure the directory is correct.")

# Pre-format matplotlib plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Helvetica Neue']
rcParams['text.color'] = '#404040'
rcParams['axes.labelcolor'] = '#404040'
rcParams['xtick.color'] = '#404040'
rcParams['ytick.color'] = '#404040'
rcParams['axes.edgecolor'] = '#404040'  # Color of the axes edges
rcParams['grid.color'] = '#404040'      # Color of the gridlines
rcParams['axes.titlecolor'] = '#404040' # Color of the axes title (optional)
rcParams['figure.figsize'] = [10, 6]  # Width, Height in inches
rcParams['figure.dpi'] = 500

# Print confirmation
print("Notebook setup complete.")

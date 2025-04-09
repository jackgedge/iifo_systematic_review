# Import libraries
import os
import sys
from dotenv import load_dotenv
import pandas as pd # For data manipulation
import numpy as np # for c
from matplotlib import pyplot as plt    # For plots
from matplotlib import rcParams # For standardised plot layouts
import re # For regular expressions
import requests # for HTTP requests and querying internet
import time
import gc
import csv
from habanero import Crossref
import seaborn as sns
from matplotlib.patches import FancyBboxPatch
from serpapi.google_search import GoogleSearch  # Google Search Module from SerpAPI
from msc_code.scripts.helpers import *   # Custom helper functions
from msc_code.scripts.data_extraction_helpers import * 

load_dotenv()

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

# Expand any env var relative to home directory
def expand_env_path(var_name):
    value = os.getenv(var_name)
    if value and not value.startswith("/"):
        return os.path.join(os.path.expanduser("~"), value)
    return value

# Directories
PROJ_ROOT_DIR = expand_env_path("PROJ_ROOT_DIR")  # project root
INPUT_DIR = expand_env_path("INPUT_DIR")  # parent input directory
OUTPUT_DIR = expand_env_path("OUTPUT_DIR")  # parent output directory
RAW_DATA_DIR = expand_env_path("RAW_DATA_DIR")  # directory for raw data
PROC_DATA_DIR = expand_env_path("PROC_DATA_DIR")  # directory for processed data
FIG_DIR = expand_env_path("FIG_DIR")  # directory for figures
SCRIPTS_DIR = expand_env_path("SCRIPTS_DIR")  # directory for scripts

# Patch sys.path so msc_code is always importable
if PROJ_ROOT_DIR and PROJ_ROOT_DIR not in sys.path:
    sys.path.insert(0, PROJ_ROOT_DIR)

# Add the 'scripts' directory to sys.path if it exists
if SCRIPTS_DIR and os.path.exists(SCRIPTS_DIR) and SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

# Import custom helper functions (if needed)
try:
    import msc_code.scripts.helpers as helpers
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

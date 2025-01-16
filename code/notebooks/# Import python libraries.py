# Import python libraries
import os               # for accessing local file systems
import sys
import pandas as pd     # for dataframe functionality
from matplotlib import pyplot as plt    # for plotting data
from matplotlib import rcParams         # for standardising plot layouts
import serpapi 
from dotenv import load_dotenv # for environmental variables, aiding privacy when not wanting to display private information (API keys; actual file locations)

# Define the path to the 'scripts' folder
scripts_path = os.path.join(os.getcwd(), "code", "scripts")

# Add the path to sys.path if not already included
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

# Import custom functions from helper.py file for use in this project.
from code.scripts.helpers import dataframe_to_ris, track_duplicate_removal

# Try to load environment variables from .env file
try: 
    load_dotenv()   # should return True if successful.
except ImportError:
    # if fails, print error.
    print("Environment Variables failed to load")

INPUT_DIR = os.getenv('INPUT_DIR')    # define input path for environment
OUTPUT_DIR = os.getenv('OUTPUT_DIR')  # define output path for environment
RAW_DATA_DIR = os.getenv('RAW_DATA_DIR') # define raw data input path
PROC_DATA_DIR = os.getenv('PROC_DATA_DIR')  # define processed data path
FIG_DIR = os.getenv('FIG_DIR') # define figure path

# pre-format plots
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
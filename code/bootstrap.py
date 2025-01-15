import os
import sys

# Define the path to the 'code/scripts' folder
scripts_path = os.path.join(os.getcwd(), "code", "scripts")

# Add the path to sys.path if not already included
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

# Import the notebook setup
from notebook_setup import *
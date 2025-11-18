import os
import shutil

# Define the root directory
root_dir = '/Users/jackgedge/Projects/qmul_data/'

# Set this to True to move files and prepend directories, False to reverse the operation
move_files = False  # Change to False to reverse

def move_and_prepending():
    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Skip files already in the root
            if dirpath == root_dir:
                continue
            
            # Create the full path of the original file
            original_file_path = os.path.join(dirpath, filename)
            
            # Create new filename by prepending the directory structure
            relative_path = os.path.relpath(dirpath, root_dir)
            new_name = f"{relative_path.replace(os.path.sep, '_')}_{filename}" if relative_path else filename
            new_file_path = os.path.join(root_dir, new_name)

            # Move the file to the root directory
            shutil.move(original_file_path, new_file_path)
            print(f'Moved: {original_file_path} to {new_file_path}')

def reverse_move():
    # Walk through the root directory
    for filename in os.listdir(root_dir):
        # Check files that contain the prepended paths
        if '_' in filename:
            # Split the filename to determine its original directory structure
            parts = filename.split('_', 1)
            dir_structure = parts[0].replace('_', os.path.sep)
            original_dir_path = os.path.join(root_dir, dir_structure)

            # Create the original directory if it doesn't exist
            os.makedirs(original_dir_path, exist_ok=True)

            # Move the file back to its original directory
            original_file_path = os.path.join(root_dir, filename)
            new_file_path = os.path.join(original_dir_path, parts[1])
            shutil.move(original_file_path, new_file_path)
            print(f'Moved back: {original_file_path} to {new_file_path}')

# Choose operation based on the flag
if move_files:
    move_and_prepending()
else:
    reverse_move()

import sys
import os
from datetime import datetime
import shutil

def rename_file(file_id):
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_filename = f"{current_datetime}.pdf"

    # Copy the original file to the 'renamed' directory
    try:
        shutil.copy2('uploads/' + file_id, 'renamed/' + file_id)
        print(f"Original file copied to 'renamed' directory")
    except OSError as e:
        print(f"Error copying file: {e}")
        sys.exit(1)

    # Rename the copied file
    try:
        os.rename('renamed/' + file_id, 'renamed/' + new_filename)
        print(f"Copied file renamed to: {new_filename}")
    except OSError as e:
        print(f"Error renaming file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if file_id and original_name arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python {python_script} {file_id}")
        sys.exit(1)

    # Extract file_id and original_name from command line arguments
    file_id = sys.argv[1]

    # Call the rename_file function
    rename_file(file_id)

import pathlib
import shutil
import subprocess
import sys

def process_python_files(input_dir_path_str, output_dir_path_str):
    """
    Processes python files in the input directory, creating modified copies in the output directory.

    Args:
        input_dir_path_str (str): Path to the input directory.
        output_dir_path_str (str): Path to the output directory.
    """

    input_dir = pathlib.Path(input_dir_path_str)
    output_dir = pathlib.Path(output_dir_path_str)

    # Create output directory if it doesn't exist, or remove and recreate if it does
    if output_dir.exists():
        shutil.rmtree(output_dir)  # Remove directory and all contents
    output_dir.mkdir(parents=True)  # Create directory and any necessary parents

    for input_file in input_dir.glob("*.py"):
        if input_file.is_file():
            process_file(input_file, output_dir)

def process_file(input_file, output_dir):
    """
    Processes a single python file.

    Args:
        input_file (pathlib.Path): Path to the input python file.
        output_dir (pathlib.Path): Path to the output directory.
    """
    output_file_original = output_dir / input_file.name
    output_file_temp = output_dir / (input_file.stem + "_temp.py")

    # Copy to _temp and original filenames
    shutil.copy2(input_file, output_file_temp) # copy2 to preserve metadata
    shutil.copy2(input_file, output_file_original)

    # Append print statement to _temp file
    with open(output_file_temp, "a") as f_temp:
        f_temp.write("\nprint(part.volume)\n")

    # Run the _temp file and capture output
    try:
        result = subprocess.run(
            [sys.executable, str(output_file_temp)], # Use sys.executable to ensure correct python interpreter
            capture_output=True,
            text=True,
            check=True # Raise exception for non-zero exit codes
        )
        captured_output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running {output_file_temp}:")
        print(e.stderr) # Print standard error if the script failed
        captured_output = "Error during execution" # Or handle error as needed

    # Modify the original file to add the comment
    with open(output_file_original, "a") as f_original:
        f_original.write(f"\n# Volume: {captured_output} mm^3\n")

    # Delete the _temp file
    output_file_temp.unlink()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_directory> <output_directory>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    process_python_files(input_directory, output_directory)
    print(f"Processed python files from '{input_directory}' to '{output_directory}'.")


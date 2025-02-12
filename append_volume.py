import sys
import os
import shutil
import subprocess

def process_python_files(input_dir, output_dir):
    """
    Processes Python files in the input directory, performs actions as described,
    and saves modified files to the output directory.

    Args:
        input_dir (str): Path to the input directory.
        output_dir (str): Path to the output directory.
    """

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".py") and os.path.isfile(os.path.join(input_dir, filename)):
            input_filepath = os.path.join(input_dir, filename)
            filename_stem, filename_ext = os.path.splitext(filename)
            output_filepath_temp = os.path.join(output_dir, filename_stem + "_temp" + filename_ext)
            output_filepath_original = os.path.join(output_dir, filename)

            try:
                # 1. Copy to output directory with "_temp"
                shutil.copy2(input_filepath, output_filepath_temp)
                print(f"Copied '{filename}' to '{output_filepath_temp}'")

                # 2. Copy to output directory with original name
                shutil.copy2(input_filepath, output_filepath_original)
                print(f"Copied '{filename}' to '{output_filepath_original}'")

                # 3. Append print(part.volume) to _temp file and run
                with open(output_filepath_temp, "a") as temp_file:
                    temp_file.write("\nprint(part.volume)\n")

                try:
                    # Execute the _temp file and capture output
                    process = subprocess.run(
                        [sys.executable, output_filepath_temp], # Use sys.executable to ensure we use the same python
                        capture_output=True,
                        text=True,
                        check=True # Raise exception for non-zero exit codes
                    )
                    captured_output = process.stdout.strip()
                    print(f"Executed '{output_filepath_temp}' and captured output: '{captured_output}'")

                except subprocess.CalledProcessError as e:
                    print(f"Error executing '{output_filepath_temp}': {e}")
                    captured_output = "Error during execution" # Or handle error as needed

                # 4. Modify the original file in output directory
                with open(output_filepath_original, "a") as original_file:
                    original_file.write(f"\n# Volume: {captured_output} mm^3\n")
                print(f"Modified '{output_filepath_original}' with volume comment.")

                # 5. Delete the _temp file
                os.remove(output_filepath_temp)
                print(f"Deleted '{output_filepath_temp}'")

            except Exception as e:
                print(f"Error processing file '{filename}': {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_directory> <output_directory>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.isdir(input_directory):
        print(f"Error: Input directory '{input_directory}' is not a valid directory.")
        sys.exit(1)

    process_python_files(input_directory, output_directory)
    print("Python file processing complete.")
from pathlib import Path
import argparse

def append_files_to_output(input_dir: Path, output_file: Path) -> None:
    """
    Appends the contents of all files in the input directory to the output file.
    
    Args:
        input_dir (Path): The directory containing input files to process.
        output_file (Path): The file where the contents will be appended.
    """
    # Ensure the input directory exists
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    if not input_dir.is_dir():
        raise ValueError(f"Input path '{input_dir}' is not a directory.")
    
    # Open the output file in append mode
    with output_file.open("a") as outfile:
        # Iterate over all files in the input directory
        for file_path in sorted(input_dir.glob('*')):  # Sort files for consistent order
            if file_path.is_file():  # Process only files, ignore subdirectories
                print(f"Appending {file_path.name} to {output_file}")
                
                # Append a separator and the file name as a comment
                outfile.write(f"\n\n# Contents of {file_path.name}\n")
                
                # Append the file's contents
                outfile.write(file_path.read_text())

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Append contents of files from an input directory into a single output file.")
    
    # Add arguments for input directory and output file with defaults
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="examples_executed",
        help="Path to the input directory (default: examples_executed)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="examples_final.py",
        help="Path to the output file (default: examples_final.py)"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Convert input directory and output file to Path objects
    input_dir: Path = Path(args.input)
    output_file: Path = Path(args.output)

    # Call the function to append files
    append_files_to_output(input_dir, output_file)
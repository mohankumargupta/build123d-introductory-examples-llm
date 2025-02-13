from pathlib import Path
import re
import argparse
from typing import List, NamedTuple

# Define a NamedTuple to represent the parsed arguments
class Args(NamedTuple):
    input: Path  # Input file path
    output: Path  # Output directory path

def extract_examples(input_file: Path, output_dir: Path) -> None:
    # Remove the output directory if it exists
    if output_dir.exists():
        if not output_dir.is_dir():
            raise ValueError(f"Output path '{output_dir}' is not a directory.")
        
        for file in output_dir.glob('*'):  # Remove all files and subdirectories
            if file.is_file() or file.is_symlink():
                file.unlink()  # Delete the file or symbolic link
            elif file.is_dir():
                raise ValueError(f"Directory '{file}' inside output directory is not empty.")
        
        output_dir.rmdir()  # Remove the now-empty directory

    # Create the output directory
    output_dir.mkdir()

    # Ensure the input file exists
    if not input_file.exists():
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
    
    if not input_file.is_file():
        raise ValueError(f"Input path '{input_file}' is not a file.")

    # Read the content of the input file
    content: str = input_file.read_text()

    # Split the content into individual examples using the delimiter "##########"
    examples: List[str] = re.split(r'#{3,}\n', content)

    # Filter out any empty strings from the split operation
    examples = [example.strip() for example in examples if example.strip()]

    # Process each example
    for i, example in enumerate(examples, start=1):
        # Generate the filename for the example
        filename: str = f"example-{i:02d}.py"

        # Write the example to its own file in the output directory
        (output_dir / filename).write_text(example)

        print(f"Created {filename}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract examples from a Python source file into separate files.")
    
    # Add arguments for input file and output directory with defaults
    parser.add_argument(
        "-i", "--input",
        type=Path,  # Use Path as the type for input
        default=Path("general_examples5.py"),
        help="Path to the input Python source file (default: general_examples5.py)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,  # Use Path as the type for output
        default=Path("examples"),
        help="Path to the output directory (default: examples)"
    )

    # Parse the arguments and cast them to the Args NamedTuple
    args = Args(**vars(parser.parse_args()))

    # Call the function to extract examples
    extract_examples(args.input, args.output)
import os
import re

def extract_examples(source_code):
    """
    Extracts individual examples from the source code.
    
    Args:
        source_code (str): The full content of the source code file.
    
    Returns:
        list: A list of tuples, where each tuple contains the example number,
              title, and the corresponding code block.
    """
    # Regular expression to match the separator lines
    separator_pattern = r'^#{3,}$'
    
    # Split the source code into sections based on separator lines
    sections = re.split(separator_pattern, source_code, flags=re.MULTILINE)
    
    # Regular expression to match the example header (e.g., "# 1. Simple Rectangular Plate")
    header_pattern = re.compile(r'^#\s*(\d+)\.\s*(.+)$', re.MULTILINE)
    
    examples = []
    for section in sections:
        # Strip leading/trailing whitespace from the section
        section = section.strip()
        if not section:
            continue
        
        # Try to match the header in the current section
        header_match = header_pattern.match(section)
        if header_match:
            example_number = header_match.group(1)
            example_title = header_match.group(2).strip()
            
            # Extract the code block (everything after the header line)
            code_block = section[header_match.end():].strip()
            
            examples.append((example_number, example_title, code_block))
    
    return examples

def save_examples(examples, folder="examples"):
    """
    Saves the extracted examples into separate files in the specified folder.
    
    Args:
        examples (list): A list of tuples containing the example number, title,
                         and code block.
        folder (str): The folder where the example files will be saved.
    """
    # Create the examples folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    for number, title, code in examples:
        # Generate a filename based on the example number and title
        filename = f"{number.zfill(2)}-{title.replace(' ', '-')}.py"
        filepath = os.path.join(folder, filename)
        
        # Write the code block to the file
        with open(filepath, "w") as file:
            file.write(code)
        
        print(f"Saved: {filepath}")

def main(input_file):
    """
    Main function to read a Python source code file, extract examples, and save them.
    
    Args:
        input_file (str): Path to the input Python source code file.
    """
    # Read the source code from the input file
    with open(input_file, "r") as file:
        source_code = file.read()
    
    # Extract examples from the source code
    examples = extract_examples(source_code)
    
    # Save the extracted examples into separate files
    save_examples(examples)

if __name__ == "__main__":
    # Specify the path to the input Python source code file
    input_file = "general_examples4.py"
    
    # Run the main function
    main(input_file)
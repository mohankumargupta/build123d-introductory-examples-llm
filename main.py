import os
import re
import sys

def create_examples_folder():
    """Creates the 'examples' folder if it does not exist."""
    if not os.path.exists("examples"):
        os.makedirs("examples")

def generate_filename(example_number, example_title):
    """Generates a filename from the example number and title."""
    title_part = example_title.strip().lower().replace(" ", "-")
    title_part = re.sub(r'[^\w\-]+', '', title_part) # remove non-alphanumeric except hyphen
    return f"{example_number:02d}-{title_part}.py"

def extract_code_block(example_text):
    """Extracts the python code block from the example text."""
    lines = example_text.strip().splitlines()
    code_lines = []
    start_code = False
    for line in lines:
        if line.startswith("#"):
            if start_code: # ignore comment lines after example description
                continue
            if re.match(r"#\s*\d+\.\s", line): # if title line, skip
                continue
            else: # if other comment line before code, skip
                continue
        else:
            start_code = True
            code_lines.append(line)
    return "\n".join(code_lines).strip()

def process_example(example_text):
    """Processes a single example text and creates a python file."""
    title_line = ""
    for line in example_text.strip().splitlines():
        if line.startswith("#") and re.match(r"#\s*\d+\.\s", line):
            title_line = line
            break

    if not title_line:
        return  # Skip if no title line found

    match = re.match(r"#\s*(\d+)\.\s*(.*)", title_line)
    if match:
        example_number = int(match.group(1))
        example_title = match.group(2).strip()
        filename = generate_filename(example_number, example_title)
        code_block = extract_code_block(example_text)

        if code_block: # only create file if code block is not empty
            filepath = os.path.join("examples", filename)
            with open(filepath, "w") as f:
                f.write(code_block)
            print(f"Created file: {filepath}")
        else:
            print(f"Warning: No code block found for example: {example_title}")
    else:
        print(f"Warning: Could not parse title line: {title_line.strip()}")


def main(input_file: str):
    create_examples_folder()

    with open(input_file, "r") as f:
        input_content = f.read()

    examples = input_content.split("##########################################")

    for example_text in examples:
        if example_text.strip(): # process only non-empty example blocks
            process_example(example_text)

    print("Example file creation completed.")


if __name__ == "__main__":
    input_file = "general_examples5.py"
    main(input_file)
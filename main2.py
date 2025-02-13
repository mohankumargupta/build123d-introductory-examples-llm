import os

def split_examples_to_files(input_file_path):
    """
    Splits a file containing multiple examples separated by '#########################################'
    into individual example files in an 'examples' folder.

    Args:
        input_file_path (str): Path to the input file containing examples.
    """

    examples_dir = "examples"
    os.makedirs(examples_dir, exist_ok=True)  # Create 'examples' folder if it doesn't exist

    try:
        with open(input_file_path, 'r') as infile:
            content = infile.readlines()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file_path}'")
        return

    example_count = 0
    current_example_content = []
    in_example = False

    for line in content:
        if line.strip() == "##########################################":
            if in_example:
                # Write the previous example to a file
                if current_example_content:
                    example_number = example_count
                    example_filename = os.path.join(examples_dir, f"example-{example_number:02d}.py")
                    with open(example_filename, 'w') as outfile:
                        outfile.writelines(current_example_content)
                    print(f"Example {example_number} written to '{example_filename}'")

                current_example_content = []  # Reset for the new example
                in_example = False

            example_count += 1
            in_example = True
            current_example_content.append(line) # Include separator in the example file
        elif in_example:
            current_example_content.append(line)
        else:
            pass # Ignore lines before the first example if any

    # Write the last example if any
    if in_example and current_example_content:
        example_number = example_count
        example_filename = os.path.join(examples_dir, f"example-{example_number:02d}.py")
        with open(example_filename, 'w') as outfile:
            outfile.writelines(current_example_content)
        print(f"Example {example_number} written to '{example_filename}'")

    if example_count == 0:
        print("No examples found in the input file.")
    else:
        print(f"Successfully processed {example_count} examples.")


if __name__ == "__main__":
    input_file = "general_examples5.py"  # Change this to your input file name if different
    split_examples_to_files(input_file)
    #print(f"Examples are saved in the '{os.path.basename(os.path.dirname(os.path.join(os.getcwd(), 'examples/example-01.py')))}' folder.")
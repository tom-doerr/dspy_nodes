#!/usr/bin/env python3

import json
import argparse

def create_dataset(input_file, output_file, chars_per_section):
    # Read the entire input file
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into sections
    sections = [text[i:i+chars_per_section] for i in range(0, len(text), chars_per_section)]

    # Create the dataset
    dataset = []
    for section in sections:
        # Strip leading/trailing whitespace and skip empty sections
        section = section.strip()
        if section:
            item = {
                "input": {
                    "source_text": section
                }
            }
            dataset.append(item)

    # Write the dataset to a JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(dataset, file, indent=4, ensure_ascii=False)

    print(f"Created dataset with {len(dataset)} items in {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a dataset JSON file from a large text file.")
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("output_file", help="Path to the output JSON file")
    parser.add_argument("chars_per_section", type=int, help="Number of characters per section")

    args = parser.parse_args()

    create_dataset(args.input_file, args.output_file, args.chars_per_section)

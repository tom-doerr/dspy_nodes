import json
import os
from server import PromptServer
# from nodes import BaseNode

# class DatasetReader(BaseNode):
class DatasetReader:
    def __init__(self):
        self.current_index = 0
        self.data = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "dataset.json"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "read_dataset"
    OUTPUT_NODE = True
    CATEGORY = "Dataset"

    def read_dataset(self, file_path):
        # Print the absolute path of the file being accessed
        abs_file_path = os.path.abspath(file_path)
        print(f"Attempting to read file from: {abs_file_path}")

        # Reset index if file path changed
        if not hasattr(self, 'last_file_path') or self.last_file_path != file_path:
            self.current_index = 0
            self.last_file_path = file_path

        # Read file if not already read
        if not self.data:
            try:
                with open(abs_file_path, 'r') as file:
                    self.data = json.load(file)
                print(f"Successfully read file: {abs_file_path}")
            except Exception as e:
                print(f"Error reading file {abs_file_path}: {str(e)}")
                return (f"Error reading file: {str(e)}",)

        # Get current item
        if self.current_index < len(self.data):
            current_item = self.data[self.current_index]
            source_text = current_item['input']['source_text']
            
            # Increment index for next execution
            self.current_index += 1
            if self.current_index >= len(self.data):
                self.current_index = 0  # Reset to beginning if we've reached the end
            
            return (source_text,)
        else:
            return ("No more items",)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

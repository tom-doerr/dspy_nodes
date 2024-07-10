import textwrap

class StringSplitter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {"multiline": True, "forceInput": True}),
                "number_of_parts": ("INT", {"default": 2, "min": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Split Strings",)
    OUTPUT_NODE = True
    FUNCTION = "split_string"
    CATEGORY = "Text"

    # Add this line to set the color
    OUTPUT_IS_LIST = (True,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def split_string(self, input_string, number_of_parts):
        part_length = max(1, len(input_string) // number_of_parts)
        parts = textwrap.wrap(input_string, part_length)

        while len(parts) < number_of_parts:
            parts.append("")

        if len(parts) > number_of_parts:
            parts = parts[:number_of_parts-1] + [''.join(parts[number_of_parts-1:])]

        return (parts,)

# Add the node to ComfyUI
NODE_CLASS_MAPPINGS = {
    "StringSplitter": StringSplitter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringSplitter": "String Splitter"
}

# Add this to set the color
StringSplitter.color = "#ff00ff"

# MANIFEST = {
    # "custom_nodes": [
        # {
            # "display_name": "String Splitter",
            # "name": "StringSplitter",
            # "output": [
                # {
                    # "name": "STRING_SPLIT",
                    # "type": "STRING_SPLIT",
                    # "color": "#ff00ff"  # Magenta color for the connection
                # }
            # ]
        # }
    # ]
# }

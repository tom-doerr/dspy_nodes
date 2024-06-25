class StringReverser:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"default": "Hello, ComfyUI!"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "reverse_string"
    CATEGORY = "string_operations"

    def reverse_string(self, input_string):
        reversed_string = input_string[::-1]
        print(f"Input: {input_string}, Output: {reversed_string}")
        return (reversed_string,)

    @classmethod
    def TITLE(s):
        return "String Reverser 🔄"

    @classmethod
    def IS_CHANGED(s, widget):
        return True

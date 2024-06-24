class DynamicOptionsNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "category": (["fruits", "colors", "animals"],),
                "selection": (s.get_options("fruits"), {"default": "apple"}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "custom"

    @classmethod
    def get_options(cls, category):
        if category == "fruits":
            return ["apple", "banana", "orange"]
        elif category == "colors":
            return ["red", "green", "blue"]
        elif category == "animals":
            return ["dog", "cat", "bird"]
        return []

    def process(self, category, selection):
        return (selection,)

    @classmethod
    def VALIDATE_INPUTS(cls, category, selection):
        if selection not in cls.get_options(category):
            return "Invalid selection for the chosen category"
        return True

# NODE_CLASS_MAPPINGS = {
    # "DynamicOptionsNode": DynamicOptionsNode
# }

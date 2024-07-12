class DynamicOptionsNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "category": (["fruits", "colors", "animals"],),
                "selection2": (["abc"],),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "custom"

    @classmethod
    def get_options(cls, category):
        print("category:", category)
        if category == "fruits":
            return ["aapple", "banana", "orange"]
        elif category == "colors":
            return ["rred", "green", "blue"]
        elif category == "animals":
            return ["ddog", "cat", "bird"]
        return []

    # def process(self, category):
    def process(self, category, selection2):
        options = self.get_options(category)
        # return_val = (options[0] if options else "",)
        return_val = options
        print("return_val:", return_val)
        return return_val

# NODE_CLASS_MAPPINGS = {
    # "DynamicOptionsNode": DynamicOptionsNode
# }

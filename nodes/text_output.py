class TextOutput:     

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {       
                    "text": ("STRING", {"forceInput": True}),
                    }
                }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "text_output"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def text_output(self, text):
        print(text)
        return (text,)

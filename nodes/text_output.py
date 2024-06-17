class TextOutput:     

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {       
                    "text": ("STRING", {"forceInput": True}),
                    }
                }

    RETURN_TYPES = ("STRING",)
    # RETURN_TYPES = ()
    FUNCTION = "text_output"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def text_output(self, text='test123'):
        # print(text)
        text_joined = ''.join(text)
        text = text_joined
        print(f'text output input text: {text}')
        # return (text,)
        # return {"ui": {"text": (text,)}}
        return {"ui": {"text": text}, "result": (text,)}

from custom_nodes.dspy_nodes.nodes.global_file import server_settings

class TextField:     

    @classmethod
    def INPUT_TYPES(cls):
               
        return {"required": {       
                    "text": ("STRING", {"multiline": True, "default": ""}),
                    }
                }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "text_input"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def text_input(self, text):
        server_settings['test'] = 'abc'
        return (text,)

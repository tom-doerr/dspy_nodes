from custom_nodes.dspy_nodes.nodes.global_file import server_settings
import dspy

class Model:     

    @classmethod
    def INPUT_TYPES(cls):
               
        return {"required": {       
                    "model": ("STRING", {"default": "microsoft/Phi-3-medium-128k-instruct"}),
                    "max_tokens": ("INT", {"default": 100, "min": 1}),
                    "api_base": ("STRING", {"default": "http://localhost:8000/v1/"})
                    }
                }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "set_params"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def set_params(self, model, max_tokens, api_base):
        server_settings['model'] = model
        print("====== model file server_settings:", server_settings)
        lm = dspy.OpenAI(model=model, api_base=api_base, api_key="EMPTY", max_tokens=max_tokens)
        return [lm]

from custom_nodes.dspy_nodes.nodes.global_file import server_settings
import dspy

class Model:     

    @classmethod
    def INPUT_TYPES(cls):
               
        return {"required": {       
                    "model": ("STRING", {"default": "microsoft/Phi-3-medium-128k-instruct"}),
                    "max_tokens": ("INT", {"default": 100, "min": 1}),
                    }
                }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "set_params"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def set_params(self, model, max_tokens):
        server_settings['model'] = model
        print("====== model file server_settings:", server_settings)
        # lm = dspy.HFClientVLLM(model=server_settings['model'], port=38242, url="http://localhost", max_tokens=200)
        # lm = dspy.HFClientVLLM(model=model, port=38242, url="http://localhost", max_tokens=200)
        lm = dspy.OpenAI(model=model, api_base="http://localhost:38242/v1/", api_key="EMPTY", max_tokens=max_tokens)
        return [lm]

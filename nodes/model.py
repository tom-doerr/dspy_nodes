from custom_nodes.dspy_nodes.nodes.global_file import server_settings
import dspy

class Model:     

    @classmethod
    def INPUT_TYPES(cls):
               
        return {"required": {       
                    "model": ("STRING", {"default": "microsoft/Phi-3-medium-128k-instruct"}),
                    }
                }

    # RETURN_TYPES = ()
    # RETURN_TYPES = ("STRING",)
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "set_params"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def set_params(self, model):
        server_settings['model'] = model
        print("====== model file server_settings:", server_settings)
        # lm = dspy.HFClientVLLM(model=server_settings['model'], port=38242, url="http://localhost", max_tokens=200)
        lm = dspy.HFClientVLLM(model=model, port=38242, url="http://localhost", max_tokens=200)
        # return 'text'
        return [lm]

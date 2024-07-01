# from custom_nodes.dspy_nodes.nodes.global_file import server_settings
from custom_nodes.dspy_nodes.nodes.global_file import global_values
import dspy

class FewShotControl:

    @classmethod
    def INPUT_TYPES(cls):
               
        return {"required": {       
                    "module_id": ("STRING", {}),
                    "test": (['abc', 'def', 'jkl'], {}),
                    "test2": (['abkjlsfdjkalfsjlksjflkjfsalkjfaslkjfsalkjflkajflksajflskajflksac', 'dajslkfdjflksjlkajfslkjsalkfjlksajlkafjkjlalkjef', 'jkl jklsfajlk ajfslka alkjfjlk a alkjjlk a askljalj a lkjdsjlsajla'], {}),
                    }
                }

    # RETURN_TYPES = ()
    # RETURN_TYPES = ("STRING",)
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "set_params"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    # def set_params(self, model):
    def set_params(self, module_id, test, test2):
        print("global_values:", global_values)
        # global_values[module_id]['test'] = test
        if not module_id in global_values:
            global_values[module_id] = {}
        global_values[module_id]['test'] = test
        print("global_values:", global_values)
        server_settings['model'] = model
        print("====== model file server_settings:", server_settings)
        # lm = dspy.HFClientVLLM(model=server_settings['model'], port=38242, url="http://localhost", max_tokens=200)
        lm = dspy.HFClientVLLM(model=model, port=38242, url="http://localhost", max_tokens=200)
        # return 'text'
        return [lm]

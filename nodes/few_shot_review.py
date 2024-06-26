from custom_nodes.dspy_nodes.nodes.global_file import global_values
import dspy
from dspy.teleprompt import BootstrapFewShot, LabeledFewShot
from dspy.evaluate.evaluate import Evaluate
from random import randint
import time

class FewShotReview:

    @classmethod
    def INPUT_TYPES(cls):
        if 'predictions' in global_values:
            module_keys = list(global_values['predictions'].keys()) 
        else:
            module_keys = [None]
        return {"required": {       
                    # "model": ("MODEL", {}),
                    # "input_text": ("STRING", {"force_input": True}),
                    # "output_description": ("STRING", {}),
                    # "module_id": ("STRING", {"default": '123'})
                    "module_id": (module_keys, {}),
                    "time_int": ("INT", {"default": int(time.time())}),
                    }
                }

    # RETURN_TYPES = ("STRING","STRING")
    # RETURN_TYPES = ("STRING",)
    RETURN_TYPES = ()
    FUNCTION = "main"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def __init__(self):
        # self.MODULE_ID = str(randint(100000, 999999))
        #base 64
        import base64
        import os
        self.MODULE_ID = base64.b64encode(os.urandom(6)).decode('utf-8')

    def IS_CHANGED(self, module_id, time_int):
        return time.time()

    # def main(self, model, input_text):
    # def main(self, model, input_text, output_description):
    # def main(self, module_id):
    def main(self, module_id, time_int):
        return []




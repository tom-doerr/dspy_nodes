from custom_nodes.dspy_nodes.nodes.global_file import global_values
import dspy
from dspy.teleprompt import BootstrapFewShot, LabeledFewShot
from dspy.evaluate.evaluate import Evaluate
from random import randint

class FewShotCoT:

    @classmethod
    def INPUT_TYPES(cls):
               
        return {"required": {       
                    "model": ("MODEL", {}),
                    "input_text": ("STRING", {"force_input": True}),
                    "output_description": ("STRING", {}),
                    # "module_id": ("STRING", {"default": '123'})
                    }
                }

    RETURN_TYPES = ("STRING","STRING")
    # RETURN_TYPES = ("STRING",)
    FUNCTION = "main"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def __init__(self):
        # self.MODULE_ID = str(randint(100000, 999999))
        #base 64
        import base64
        import os
        self.MODULE_ID = base64.b64encode(os.urandom(6)).decode('utf-8')

        # self.input_types = self.modify_input_types()

    # def modify_input_types(self):
        # input_types = self.INPUT_TYPES()
        # input_types['required']['module_id'] = ("STRING", {"default": self.module_id})
        # return input_types







    # def main(self, model, input_text):
    def main(self, model, input_text, output_description):
    # def main(self, model, input_text, output_description, module_id):
        dspy.settings.configure(lm=model, trace=[], temperature=0.7)

        class GenerationSignature(dspy.Signature):
            """"""
            input_text = dspy.InputField()
            output_text = dspy.OutputField(desc=output_description)

        class GenerationModule(dspy.Module):
            def __init__(self):
                super().__init__()
                self.signature = GenerationSignature
                self.predictor_cot  = dspy.ChainOfThought(self.signature)

            def forward(self, input_text):
                predictions = []
                result = self.predictor_cot(input_text=input_text)
                output_text = result.output_text.split('---')[0].strip()

                return dspy.Prediction(
                    input_text=input_text,
                    output_text=output_text
                )

        generation_module = GenerationModule()
        prediction = generation_module(input_text=input_text)
        # global_values[self.MODULE_ID]['test'] = prediction.output_text
        if not 'predictions' in global_values:
            global_values['predictions'] = {}
        # global_values[self.MODULE_ID] = prediction.output_text
        # global_values['predictions'][self.MODULE_ID] = prediction.output_text
        global_values['predictions'][self.MODULE_ID] = [prediction]
        # return prediction.output_text
        return [prediction.output_text, self.MODULE_ID]
        # return [prediction.output_text]




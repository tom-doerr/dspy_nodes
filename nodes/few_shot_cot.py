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
                    }
                }

    RETURN_TYPES = ("STRING","STRING")
    FUNCTION = "main"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def __init__(self):
        self.MODULE_ID = str(randint(100000, 999999))


    # def main(self, model, input_text):
    def main(self, model, input_text, output_description):
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
        global_values[self.MODULE_ID] = prediction.output_text
        # return prediction.output_text
        return [prediction.output_text, self.MODULE_ID]




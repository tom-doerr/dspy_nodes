from custom_nodes.dspy_nodes.nodes.global_file import global_values
import dspy
from dspy.teleprompt import BootstrapFewShot
import base64
import os

class FewShotCoT:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {       
                    "model": ("MODEL", {}),
                    "input_text": ("STRING", {"multiline": True}),
                    "output_description": ("STRING", {"multiline": True}),
                    "use_accepted_examples": (["yes", "no"], {}),
                    }
                }
    RETURN_TYPES = ("STRING", "STRING")  # output_text, module_id
    RETURN_NAMES = ("output_text", "module_id")

    FUNCTION = "main"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def __init__(self):
        self.MODULE_ID = base64.b64encode(os.urandom(6)).decode('utf-8')

    def main(self, model, input_text, output_description, use_accepted_examples):
        dspy.settings.configure(lm=model, trace=[], temperature=0.7)

        class GenerationSignature(dspy.Signature):
            input_text = dspy.InputField()
            output_text = dspy.OutputField(desc=output_description)

        class GenerationModule(dspy.Module):
            def __init__(self, accepted_examples=None):
                super().__init__()
                self.signature = GenerationSignature
                if accepted_examples:
                    self.predictor_cot = BootstrapFewShot(GenerationSignature, n_boostrap=5, n_demos=3)
                    self.predictor_cot.boostrap(accepted_examples)
                else:
                    self.predictor_cot = dspy.ChainOfThought(self.signature)

            def forward(self, input_text):
                result = self.predictor_cot(input_text=input_text)
                output_text = result.output_text.split('---')[0].strip()
                return dspy.Prediction(
                    input_text=input_text,
                    output_text=output_text
                )

        accepted_examples = None
        if use_accepted_examples == "yes" and 'accepted_predictions' in global_values:
            accepted_examples = [pred for preds in global_values['accepted_predictions'].values() for pred in preds]

        generation_module = GenerationModule(accepted_examples)
        prediction = generation_module(input_text=input_text)

        import random
        # global_values['random_value'] = random.randint(0, 1000000)
        random_value = random.randint(0, 1000000)
        # print(f"=== Random value set in CoT: {random_value}")
        global_values['random_value'] = random_value

        if 'predictions' not in global_values:
            global_values['predictions'] = {}
        if self.MODULE_ID not in global_values['predictions']:
            global_values['predictions'][self.MODULE_ID] = []
        global_values['predictions'][self.MODULE_ID].append(prediction)

        # print(f"Stored prediction for module ID: {self.MODULE_ID}")
        # print(f"Number of predictions: {len(global_values['predictions'][self.MODULE_ID])}")

        return [prediction.output_text, self.MODULE_ID]

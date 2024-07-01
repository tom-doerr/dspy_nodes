import os
# dspy_cachebool = True
dspy_cachebool = False
os.environ["DSP_CACHEBOOL"] = str(dspy_cachebool)

from custom_nodes.dspy_nodes.nodes.global_file import global_values
import dspy
from dspy.teleprompt import BootstrapFewShot, LabeledFewShot
import base64
import os
import random

def predictions_to_examples(predictions):
    examples = []
    for prediction in predictions:
        example = dspy.Example(**prediction).with_inputs('input_text')
        examples.append(example)

    return examples

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

    def IS_CHANGED(self, unique_id):
        return float("NaN")  # Always re-run

    def main(self, model, input_text, output_description, use_accepted_examples):
        temperature = 0.7 + (1 * random.random())
        dspy.settings.configure(lm=model, trace=[], temperature=temperature)
        if 'accepted_predictions' in global_values:
            print("global_values['accepted_predictions']:", global_values['accepted_predictions'])

        class GenerationSignature(dspy.Signature):
            input_text = dspy.InputField()
            output_text = dspy.OutputField(desc=output_description)

        class GenerationModule(dspy.Module):
            def __init__(self, accepted_examples=None):
                super().__init__()
                self.signature = GenerationSignature
                predictor_uncompiled = dspy.ChainOfThought(self.signature)

                self.predictor_cot = dspy.ChainOfThought(self.signature)

            def forward(self, input_text):
                temperature = 2.7 + (1 * random.random())
                print("temperature:", temperature)
                with dspy.settings.context(lm=model, trace=[], temperature=temperature):
                    # result = self.predictor_cot(input_text=input_text, temperature=temperature)
                    result = self.predictor_cot(input_text=input_text)
                output_text = result.output_text.split('---')[0].strip()
                return dspy.Prediction(
                    input_text=input_text,
                    output_text=output_text
                )

        if use_accepted_examples == "yes" and 'accepted_predictions' in global_values:
            accepted_examples = [pred for preds in global_values['accepted_predictions'].values() for pred in preds]
            compile_examples = predictions_to_examples(global_values['accepted_predictions'][self.MODULE_ID])
        else:
            accepted_examples = []
            compile_examples = []

        generation_module_uncompiled = GenerationModule(accepted_examples)
        teleprompter = BootstrapFewShot(GenerationSignature, max_bootstrapped_demos=0)
        # teleprompter = LabeledFewShot(GenerationSignature)
        # self.predictor_cot = teleprompter.compile(student=predictor_uncompiled, trainset=compile_examples)
        print("compile_examples:", compile_examples)



        if compile_examples:
            generation_module = teleprompter.compile(student=generation_module_uncompiled, trainset=compile_examples)
        else:
            generation_module = generation_module_uncompiled

        prediction = generation_module(input_text=input_text)

        # global_values['random_value'] = random.randint(0, 1000000)
        random_value = random.randint(0, 1000000)
        # print(f"=== Random value set in CoT: {random_value}")
        global_values['random_value'] = random_value

        if 'predictions' not in global_values:
            global_values['predictions'] = {}
        if self.MODULE_ID not in global_values['predictions']:
            global_values['predictions'][self.MODULE_ID] = []
        global_values['predictions'][self.MODULE_ID].append(prediction)


        return [prediction.output_text, self.MODULE_ID]

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
from concurrent.futures import ThreadPoolExecutor, as_completed


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
                    # "input_text": ("STRING", {"multiline": True}),
                    "input_texts": ("STRING", {"forceInput": True, "multiline": True}),
                    "output_description": ("STRING", {"multiline": True}),
                    # "use_accepted_examples": (["yes", "no"], {}),
                    "use_accepted_examples": ("BOOLEAN", {"default": True}), 
                    }
                }
    RETURN_TYPES = ("STRING", "STRING")  # output_text, module_id
    RETURN_NAMES = ("output_text", "module_id")
    # RETURN_NAMES = ("Custom Output 1", "Custom Output 2")

    FUNCTION = "main"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"
    # INPUT_IS_LIST = (True,)
    # INPUT_IS_LIST = (False, True, False, False)
    INPUT_IS_LIST = (True,)
    OUTPUT_IS_LIST = (True, False)
    # INPUT_IS_LIST = True

    def __init__(self):
        self.MODULE_ID = base64.b64encode(os.urandom(6)).decode('utf-8')

    def IS_CHANGED(self, unique_id):
        return float("NaN")  # Always re-run


    def process_single_input(self, input_text, model, output_description, use_accepted_examples):
        temperature = 0.7 + (1 * random.random())
        dspy.settings.configure(lm=model, trace=[], temperature=temperature)

        class GenerationSignature(dspy.Signature):
            input_text = dspy.InputField()
            output_text = dspy.OutputField(desc=output_description)

        class GenerationModule(dspy.Module):
            def __init__(self, accepted_examples=None):
                super().__init__()
                self.signature = GenerationSignature
                self.predictor_cot = dspy.ChainOfThought(self.signature)

            def forward(self, input_text):
                temperature = 2.7 + (1 * random.random())
                print(f"Temperature for input '{input_text[:30]}...': {temperature}")
                with dspy.settings.context(lm=model, trace=[], temperature=temperature):
                    result = self.predictor_cot(input_text=input_text)
                output_text = result.output_text.split('---')[0].strip()
                return dspy.Prediction(
                    input_text=input_text,
                    output_text=output_text
                )

        if use_accepted_examples and 'accepted_predictions' in global_values and self.MODULE_ID in global_values['accepted_predictions']:
            compile_examples = self.predictions_to_examples(global_values['accepted_predictions'][self.MODULE_ID])
        else:
            compile_examples = []

        generation_module_uncompiled = GenerationModule()
        teleprompter = BootstrapFewShot(GenerationSignature, max_bootstrapped_demos=0)

        if compile_examples:
            generation_module = teleprompter.compile(student=generation_module_uncompiled, trainset=compile_examples)
        else:
            generation_module = generation_module_uncompiled

        prediction = generation_module(input_text=input_text)
        return prediction.output_text

    def main(self, model, input_texts, output_description, use_accepted_examples):
        print(f"cot: Input texts: {input_texts}")
        print(f"cot: Type of input_texts: {type(input_texts)}")
        print(f"cot: Model: {model}")
        print(f"cot: Type of model: {type(model)}")
        print(f"cot: use_accepted_examples: {use_accepted_examples}")
        print(f"cot: Type of use_accepted_examples: {type(use_accepted_examples)}")

        # Ensure all inputs are lists
        if not isinstance(input_texts, list):
            input_texts = [input_texts]
        if not isinstance(model, list):
            model = [model]
        if not isinstance(output_description, list):
            output_description = [output_description]
        if not isinstance(use_accepted_examples, list):
            use_accepted_examples = [use_accepted_examples]

        # Use the first item from each input list
        model = model[0]
        output_description = output_description[0]
        use_accepted_examples = use_accepted_examples[0]

        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
            future_to_input = {executor.submit(self.process_single_input, text, model, output_description, use_accepted_examples): text for text in input_texts}
            for future in as_completed(future_to_input):
                input_text = future_to_input[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    print(f'Input {input_text[:30]}... generated an exception: {exc}')
                    results.append(f"Error processing input: {str(exc)}")

        # Update global_values with all predictions
        if 'predictions' not in global_values:
            global_values['predictions'] = {}
        global_values['predictions'][self.MODULE_ID] = [
            dspy.Prediction(input_text=input_text, output_text=output_text)
            for input_text, output_text in zip(input_texts, results)
        ]

        return [results, self.MODULE_ID]

    @staticmethod
    def predictions_to_examples(predictions):
        return [dspy.Example(**prediction).with_inputs('input_text') for prediction in predictions]

import dspy
from dspy.teleprompt import BootstrapFewShot, LabeledFewShot
from dspy.evaluate.evaluate import Evaluate

class Predict:     

    @classmethod
    def INPUT_TYPES(cls):
               
        return {"required": {       
                    "text": ("STRING", {"multiline": False, "default": "Hello World", "forceInput": True}),
                    }
                }

    # RETURN_TYPES = ()
    RETURN_TYPES = ("STRING",)
    FUNCTION = "predict"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"
    # INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def predict(self, text):
        print(f"Tutorial Text : {text}")

        lm = dspy.HFClientVLLM(model="microsoft/Phi-3-medium-128k-instruct", port=38242, url="http://localhost", max_tokens=200)
        dspy.settings.configure(lm=lm, trace=[], temperature=0.7)

        # generate_answer = dspy.ChainOfThought("input -> output")
        generate_answer = dspy.Predict("input -> output")
        generated_text = generate_answer(input=text)
        print("generated_text:", generated_text)
        
        # return {}
        # return {generated_text}
        # return (generated_text,)
        # return (str(generated_text),)
        text = generated_text.output
        print(f'predict output text: {text}')
        # return text
        return (text,)
        # return {"ui": {"text": text}, "result": (text,)}


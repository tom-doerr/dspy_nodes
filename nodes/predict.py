import dspy
from dspy.teleprompt import BootstrapFewShot, LabeledFewShot
from dspy.evaluate.evaluate import Evaluate
from custom_nodes.dspy_nodes.nodes.global_file import server_settings

class Predict:     

    @classmethod
    def INPUT_TYPES(cls):
               
        return {
                # "required": {       
                    # "text": ("STRING", {"multiline": False, "forceInput": True}),
                    # "signature": ("STRING", {"multiline": False, "default": "input -> output", "forceInput": False}),
                    # }
 
			"required": {
                    "text": ("STRING", {"multiline": False, "forceInput": True}),
                    "model": ("MODEL", {}),
                    "signature": ("STRING", {"multiline": False, "default": "input -> output", "forceInput": False}),
				# "_query": ("STRING", {
					# "default": ">data; <data",
					# "multiline": False
				# }),
			},
			# "optional": {
				# "_way_in": ("HIGHWAY_PIPE", ),
			# },
			# "hidden": {
				# "_prompt": "PROMPT",
				# "_id": "UNIQUE_ID",
				# "_workflow": "EXTRA_PNGINFO" # Unfortunately EXTRA_PNGINFO does not get exposed during IS_CHANGED
			# }

                }

#    # RETURN_TYPES = ()
    RETURN_TYPES = ("STRING",)
    FUNCTION = "predict"

    # RETURN_TYPES = lib0246.ByPassTypeTuple(("HIGHWAY_PIPE", ))
    # RETURN_NAMES = lib0246.ByPassTypeTuple(("_way_out", ))
    # FUNCTION = "execute"


    OUTPUT_NODE = True
    CATEGORY = "DSPy"
    # INPUT_IS_LIST = True
    # OUTPUT_IS_LIST = (True,)

    # def predict(self, text, signature):
    def predict(self, text, model, signature):
        # print("text:", text)

        # lm = dspy.HFClientVLLM(model="microsoft/Phi-3-medium-128k-instruct", port=38242, url="http://localhost", max_tokens=200)
        # print("= predict file server_settings:", server_settings)
        # lm = dspy.HFClientVLLM(model=server_settings['model'], port=38242, url="http://localhost", max_tokens=200)
        lm = model
        dspy.settings.configure(lm=lm, trace=[], temperature=0.7)

        # generate_answer = dspy.ChainOfThought("input -> output")
        # generate_answer = dspy.Predict("input -> output")
        generate_answer = dspy.Predict(signature)
        generated_text = generate_answer(input=text)
        # print("generated_text:", generated_text)
        
        # return {}
        # return {generated_text}
        # return (generated_text,)
        # return (str(generated_text),)
        text = generated_text.output
        # print(f'predict output text: {text}')
        # return text
        # print("server_settings:", server_settings)
        return (text,)
        # return {"ui": {"text": text}, "result": (text,)}

    def execute(self, _id = None, _prompt = None, _workflow = None, _way_in = None, _query = None, **kwargs):
        return highway_impl(_prompt, _id, _workflow, _way_in, False, kwargs)
	
    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        return lib0246.check_update(kwargs["_query"])




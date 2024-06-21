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
        print("text:", text)

        # lm = dspy.HFClientVLLM(model="microsoft/Phi-3-medium-128k-instruct", port=38242, url="http://localhost", max_tokens=200)
        print("= predict file server_settings:", server_settings)
        # lm = dspy.HFClientVLLM(model=server_settings['model'], port=38242, url="http://localhost", max_tokens=200)
        lm = model
        dspy.settings.configure(lm=lm, trace=[], temperature=0.7)

        # generate_answer = dspy.ChainOfThought("input -> output")
        # generate_answer = dspy.Predict("input -> output")
        generate_answer = dspy.Predict(signature)
        generated_text = generate_answer(input=text)
        print("generated_text:", generated_text)
        
        # return {}
        # return {generated_text}
        # return (generated_text,)
        # return (str(generated_text),)
        text = generated_text.output
        print(f'predict output text: {text}')
        # return text
        print("server_settings:", server_settings)
        return (text,)
        # return {"ui": {"text": text}, "result": (text,)}

    def execute(self, _id = None, _prompt = None, _workflow = None, _way_in = None, _query = None, **kwargs):
        return highway_impl(_prompt, _id, _workflow, _way_in, False, kwargs)
	
    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        return lib0246.check_update(kwargs["_query"])



def highway_impl(_prompt, _id, _workflow, _way_in, flag, kwargs):
    if isinstance(_prompt, list):
        _prompt = _prompt[0]
    if isinstance(_id, list):
        _id = _id[0]
    if isinstance(_workflow, list):
        _workflow = _workflow[0]

    if isinstance(_way_in, list):
        _way_in = _way_in[0]

    if _way_in is None:
        _way_in = lib0246.RevisionDict()
    else:
        _way_in = lib0246.RevisionDict(_way_in)

    # _way_in._id = _id
    # _way_in.purge(_way_in.find(lambda item: item.id == _id))

    # Time to let the magic play out

    curr_node = next(_ for _ in _workflow["workflow"]["nodes"] if str(_["id"]) == _id)

    for i, curr_input in enumerate(curr_node["inputs"]):
        if curr_input["name"] in kwargs:
            name = _workflow["workflow"]["extra"]["0246.__NAME__"][_id]["inputs"][str(i)]["name"][1:]
            if flag:
                _way_in[("data", name)] = lib0246.RevisionBatch(*kwargs[curr_input["name"]])
            else:
                _way_in[("data", name)] = kwargs[curr_input["name"]]
            _way_in[("type", name)] = curr_input.get("type", "*") # Sometimes this does not exist. Weird.

    res = []

    for i, curr_output in enumerate(curr_node["outputs"]):
        if curr_output.get("links") and curr_output["name"] not in lib0246.BLACKLIST:
            name = _workflow["workflow"]["extra"]["0246.__NAME__"][_id]["outputs"][str(i)]["name"][1:]
            if ("data", name) in _way_in:
                if curr_output["type"] == "*" or _way_in[("type", name)] == "*" or curr_output["type"] == _way_in[("type", name)]:
                    res.append(_way_in[("data", name)])
                else:
                    raise Exception(f"Output \"{name}\" is not defined or is not of type \"{curr_output['type']}\". Expected \"{_way_in[('type', name)]}\".")

    _way_in[("kind")] = "highway"
    _way_in[("id")] = _id

    return (_way_in, ) + tuple(res)

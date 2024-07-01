from server import PromptServer
from aiohttp import web
from custom_nodes.dspy_nodes.nodes.global_file import global_values

class AcceptedExamplesViewer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "module_id": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def IS_CHANGED(self, unique_id):
        return float("NaN")  # Always re-run

    def run(self, module_id, unique_id):
        accepted_predictions = global_values.get('accepted_predictions', {}).get(module_id, [])
        
        examples_data = [
            {
                "id": i,
                "input_text": pred.input_text,
                "output_text": pred.output_text
            } for i, pred in enumerate(accepted_predictions)
        ]
        
        PromptServer.instance.send_sync("update_accepted_examples", {
            "node_id": unique_id,
            "module_id": module_id,
            "examples": examples_data
        })
        
        return (module_id,)

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
    
    RETURN_TYPES = ()
    FUNCTION = "run"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def IS_CHANGED(self, unique_id):
        return float("NaN")  # Always re-run

    def run(self, module_id, unique_id):
        accepted_predictions = global_values.get('accepted_predictions', {}).get(module_id, [])
        
        predictions = accepted_predictions
        review_data = [
            {
                "id": i,
                "module_id": module_id,
                "input_text": pred.input_text,
                "output_text": pred.output_text
            } for i, pred in enumerate(predictions)
        ]
        
        PromptServer.instance.send_sync("update_node", {
            "node_id": unique_id,
            "predictions": review_data,
        })

        return []



@PromptServer.instance.routes.post("/accepted_examples_viewer/remove_prediction")
async def remove_prediction(request):
    try:
        data = await request.json()
        module_id = data.get('module_id')
        output_text = data.get('output_text')
        
        if not module_id or not output_text:
            return web.json_response({"status": "error", "message": "Missing module_id or output_text"}, status=400)
        
        if not 'accepted_predictions' in global_values:
            global_values['accepted_predictions'] = {}
        if not module_id in global_values['accepted_predictions']:
            global_values['accepted_predictions'][module_id] = []
        accepted_predictions = global_values['accepted_predictions'][module_id]
        
        matching_prediction = next((pred for pred in accepted_predictions if pred.output_text == output_text), None)
        
        if matching_prediction:
            accepted_predictions.remove(matching_prediction)
            print(f"Removed prediction from accepted_predictions for module {module_id}")
            return web.json_response({"status": "success", "message": "Prediction removed from accepted"})
        else:
            return web.json_response({"status": "error", "message": "Matching prediction not found"}, status=404)
    
    except json.JSONDecodeError:
        return web.json_response({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"Error in remove_prediction: {str(e)}")
        return web.json_response({"status": "error", "message": str(e)}, status=500)
        
    return web.json_response({"status": "error", "message": "Unknown error"}, status=500)        



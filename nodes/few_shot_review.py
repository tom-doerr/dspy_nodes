from server import PromptServer
from aiohttp import web
import json
from custom_nodes.dspy_nodes.nodes.global_file import global_values

class FewShotReview:
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
        print("global_values:", global_values)
        print("=== global_values['predictions']:", global_values['predictions'])
        if 'accepted_predictions' in global_values:
            print("global_values['accepted_predictions']:", global_values['accepted_predictions'])
        
        predictions = global_values.get('predictions', {}).get(module_id, [])
        
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
        
        return (module_id,)


@PromptServer.instance.routes.post("/fewshotreview/print")
async def print_string(request):
    print('=== print_string ===', flush=True)
    try:
        data = await request.json()
        text = data.get('text', '')
        print(f"FewShotReview received: {text}")
        return web.json_response({"status": "success", "message": f"Printed: {text}"})
    except json.JSONDecodeError:
        return web.json_response({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"Error in print_string: {str(e)}")
        return web.json_response({"status": "error", "message": str(e)}, status=500)

@PromptServer.instance.routes.get("/fewshotreview/test")
async def test_endpoint(request):
    print("FewShotReview test endpoint hit")
    return web.json_response({"status": "ok"})


@PromptServer.instance.routes.post("/fewshotreview/mark_good")
async def mark_good(request):
    try:
        data = await request.json()
        module_id = data.get('module_id')
        output_text = data.get('output_text')
        
        if not module_id or not output_text:
            return web.json_response({"status": "error", "message": "Missing module_id or output_text"}, status=400)
        
        predictions = global_values.get('predictions', {}).get(module_id, [])
        # accepted_predictions = global_values.setdefault('accepted_predictions', {}).setdefault(module_id, [])
        if not 'accepted_predictions' in global_values:
            global_values['accepted_predictions'] = {}
        if not module_id in global_values['accepted_predictions']:
            global_values['accepted_predictions'][module_id] = []
        accepted_predictions = global_values['accepted_predictions'][module_id]
        
        matching_prediction = next((pred for pred in predictions if pred.output_text == output_text), None)
        
        if matching_prediction:
            if matching_prediction not in accepted_predictions:
                accepted_predictions.append(matching_prediction)
                print(f"Added prediction to accepted_predictions for module {module_id}")
                return web.json_response({"status": "success", "message": "Prediction marked as good"})
            else:
                return web.json_response({"status": "info", "message": "Prediction already marked as good"})
        else:
            return web.json_response({"status": "error", "message": "Matching prediction not found"}, status=404)
    
    except json.JSONDecodeError:
        return web.json_response({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"Error in mark_good: {str(e)}")
        return web.json_response({"status": "error", "message": str(e)}, status=500)



def print_registered_routes():
    print("Registered routes:")
    for route in PromptServer.instance.routes._items:
        if hasattr(route, 'method') and hasattr(route, 'path'):
            print(f"  {route.method} {route.path}")
        elif hasattr(route, '_method') and hasattr(route, '_path'):
            print(f"  {route._method} {route._path}")
        else:
            print(f"  {route}")

# Call this at the end of your file or in your initialization code
print_registered_routes()

NODE_CLASS_MAPPINGS = {
    "FewShotReview": FewShotReview
}

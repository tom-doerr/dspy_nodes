from server import PromptServer
from aiohttp import web
import json

class FewShotReview:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "module_id": ("STRING", {}),
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
        from custom_nodes.dspy_nodes.nodes.global_file import global_values
        
        predictions = global_values.get('predictions', {}).get(module_id, [])
        
        review_data = [
            {
                "id": i,
                "module_id": module_id,
                "input_text": pred.input_text,
                "output_text": pred.output_text
            } for i, pred in enumerate(predictions)
        ]
        
        # PromptServer.instance.send_sync("update_few_shot_review", {
            # "node_id": unique_id,
            # "module_id": module_id,
            # "predictions": review_data
        # })
        some_selected_text = 'test 1234'
        PromptServer.instance.send_sync("update_node", {
            "node_id": unique_id,
            "predictions": review_data,
            "selectedText": some_selected_text  # if applicable
        })
        
        return (module_id,)


# @PromptServer.instance.routes.get("/fewshotreview/test")
# async def test_endpoint(request):
    # print("Test endpoint hit")
    # return {"status": "ok"}


# PromptServer.instance.routes.post("/fewshotreview/print")
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

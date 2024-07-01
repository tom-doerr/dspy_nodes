import json
from server import PromptServer
from aiohttp import web

class FewShotReviewServer:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"module_id": ("STRING", {})}}
    
    RETURN_TYPES = ()
    FUNCTION = "run"
    OUTPUT_NODE = True
    CATEGORY = "DSPy"

    def run(self, module_id):
        # This method is called when the node is executed
        # It doesn't need to do anything, as the actual logic is in the API routes
        return ()

    @classmethod
    def setup_routes(cls):
        server = PromptServer.instance
        
        @server.routes.get("/get_review_predictions")
        async def get_review_predictions(request):
            from .global_file import global_values
            return web.json_response(global_values.get('review_predictions', []))

        @server.routes.post("/accept_prediction")
        async def accept_prediction(request):
            from .global_file import global_values
            data = await request.json()
            index = data['index']
            if 'review_predictions' in global_values and index < len(global_values['review_predictions']):
                pred = global_values['review_predictions'][index]
                if 'accepted_predictions' not in global_values:
                    global_values['accepted_predictions'] = {}
                if pred['module_id'] not in global_values['accepted_predictions']:
                    global_values['accepted_predictions'][pred['module_id']] = []
                global_values['accepted_predictions'][pred['module_id']].append(pred)
                print(f"Accepted prediction {index} from module {pred['module_id']}")
            return web.json_response({"status": "success"})

        @server.routes.post("/reject_prediction")
        async def reject_prediction(request):
            from .global_file import global_values
            data = await request.json()
            index = data['index']
            if 'review_predictions' in global_values and index < len(global_values['review_predictions']):
                pred = global_values['review_predictions'][index]
                print(f"Rejected prediction {index} from module {pred['module_id']}")
            return web.json_response({"status": "success"})

# This will be called by ComfyUI when loading the custom node
NODE_CLASS_MAPPINGS = {
    "FewShotReviewServer": FewShotReviewServer
}

# Call setup_routes when this file is loaded
FewShotReviewServer.setup_routes()

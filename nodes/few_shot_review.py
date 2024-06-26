from server import PromptServer
from aiohttp import web
import time

class MessageHolder:
    messages = {}

    @classmethod
    def addMessage(cls, id, message):
        cls.messages[str(id)] = message

    @classmethod
    def waitForMessage(cls, id, period=0.1):
        sid = str(id)
        start_time = time.time()
        while not (sid in cls.messages):
            time.sleep(period)
            if time.time() - start_time > 60:  # 1-minute timeout
                return None
        message = cls.messages.pop(str(id), None)
        return message

class FewShotReview:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FewShotReview, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True

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
        from .global_file import global_values
        
        if module_id not in global_values.get('predictions', {}):
            print(f"No predictions available for module ID: {module_id}")
            return (module_id,)
        
        predictions = global_values['predictions'][module_id]
        review_data = [
            {
                "module_id": module_id,
                "input_text": pred.input_text,
                "output_text": pred.output_text
            } for pred in predictions
        ]
        
        PromptServer.instance.send_sync("few_shot_review", {
            "id": unique_id,
            "module_id": module_id,
            "predictions": review_data
        })
        
        result = MessageHolder.waitForMessage(unique_id)
        if result is None:
            print("Timed out waiting for review")
            return (module_id,)
        
        # Process accepted predictions
        accepted_predictions = result.get('accepted_predictions', [])
        if 'accepted_predictions' not in global_values:
            global_values['accepted_predictions'] = {}
        if module_id not in global_values['accepted_predictions']:
            global_values['accepted_predictions'][module_id] = []
        global_values['accepted_predictions'][module_id].extend(accepted_predictions)
        
        print(f"Processed {len(accepted_predictions)} accepted predictions for module ID: {module_id}")
        return (module_id,)

# Add this at the end of the file
NODE_CLASS_MAPPINGS = {
    "FewShotReview": FewShotReview
}

from server import PromptServer
from aiohttp import web

def add_route_once(path, handler):
    existing_route = next((route for route in PromptServer.instance.routes if route.path == path and route.method == "POST"), None)
    if existing_route is None:
        PromptServer.instance.routes.append(web.post(path, handler))
    else:
        print(f"Route {path} already exists, skipping addition.")

async def few_shot_review_handle(request):
    post = await request.json()
    MessageHolder.addMessage(post["unique_id"], post["result"])
    return web.json_response({"status": "ok"})

# Use the new function to add the route
add_route_once('/few_shot_review_reply', few_shot_review_handle)

from server import PromptServer

class StringListViewer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_list": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            }
        }
    
    # RETURN_TYPES = ()
    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    OUTPUT_NODE = True
    CATEGORY = "Text"
    INPUT_IS_LIST = (True,)
    OUTPUT_IS_LIST = (True,)

    def IS_CHANGED(self, unique_id):
        return float("NaN")  # Always re-run

    def run(self, string_list, unique_id):
        print('=== slv: run')
        if isinstance(string_list, str):
            string_list = [string_list]
        
        view_data = [
            {
                "id": i,
                "text": text
            } for i, text in enumerate(string_list)
        ]
        print(f'=== slv: view_data: {view_data}')
        
        PromptServer.instance.send_sync("update_string_list", {
            "node_id": unique_id,
            "string_list": view_data,
        })
        # return []
        # return string_list
        return (string_list,)

# Add the node to ComfyUI
# NODE_CLASS_MAPPINGS = {
    # "StringListViewer": StringListViewer
# }

# NODE_DISPLAY_NAME_MAPPINGS = {
    # "StringListViewer": "String List Viewer"
# }

from .nodes.hello_world import *
from .nodes.predict import *
from .nodes.text_field import *
from .nodes.text_output import *
from .nodes.model import *
# from .nodes.show_text import *


NODE_CLASS_MAPPINGS = {
    "Print Hello World": PrintHelloWorld,
    "Predict": Predict,
    "Text Field": TextField,
    "Text Output": TextOutput,
    "Model": Model,
    # "Show Text": ShowText,
    }
    
print("\033[34mComfyUI Tutorial Nodes: \033[92mLoaded\033[0m")

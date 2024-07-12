import os
# dspy_cachebool = True
dspy_cachebool = False
os.environ["DSP_CACHEBOOL"] = str(dspy_cachebool)
import dspy
dspy.configure(experimental=True)

from .nodes.hello_world import *
from .nodes.predict import *
from .nodes.text_field import *
from .nodes.text_output import *
from .nodes.model import *
from .nodes.few_shot_control import *
from .nodes.few_shot_cot import *
from .nodes.few_shot_review import *
from .py.test import *
from .nodes.string_reverser import *
from .nodes.accepted_examples_viewer import *
from .nodes.dataset_reader import *
from .nodes.string_splitter import *
from .nodes.string_list_viewer import *

# from .nodes.show_text import *


NODE_CLASS_MAPPINGS = {
    "Print Hello World": PrintHelloWorld,
    "Predict": Predict,
    "Text Field": TextField,
    "Text Output": TextOutput,
    "Model": Model,
    "Few Shot Control": FewShotControl,
    "Few Shot CoT": FewShotCoT,
    "Few Shot Review": FewShotReview,
    "DynamicOptionsNode": DynamicOptionsNode,
    "StringReverser": StringReverser,
    "Accepted Examples Viewer": AcceptedExamplesViewer,
    "Dataset Reader": DatasetReader,
    "String Splitter": StringSplitter,
    "String List Viewer": StringListViewer,
    # "Show Text": ShowText,
    }
    
print("\033[34mComfyUI Tutorial Nodes: \033[92mLoaded\033[0m")

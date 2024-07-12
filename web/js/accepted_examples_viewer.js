import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "Accepted Examples Viewer",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "Accepted Examples Viewer") {

            nodeType.prototype.populate = function(predictions) {
                if (this.widgets) {
                    for (let i = 1; i < this.widgets.length; i++) {
                        this.widgets[i].onRemove?.();
                    }
                    this.widgets.length = 1;
                }

                predictions.forEach((prediction, index) => {
                    const textWidget = ComfyWidgets["STRING"](this, `prediction_${index}`, ["STRING", { multiline: true }], app).widget;
                    textWidget.inputEl.readOnly = false;
                    textWidget.inputEl.style.opacity = 1;
                    textWidget.value = `Input: ${prediction.input_text}\nOutput: ${prediction.output_text}`;
                    
                    // Increase the size of the textbox
                    textWidget.inputEl.style.width = "300px";
                    textWidget.inputEl.style.height = "100px";

                    // Add event listener for text changes
                    textWidget.inputEl.addEventListener("change", () => {
                        updatePrediction(this.module_id, prediction.id, textWidget.value);
                    });

                    const buttonWidget = this.addWidget("button", `Remove`, `Remove ${index + 1}`, () => {
                        removePrediction(this.module_id, prediction.output_text);
                    });
                });

                this.onResize?.(this.computeSize());
                app.graph.setDirtyCanvas(true, false);
            }

            nodeType.prototype.onNodeCreated = function() {
                this.addWidget("button", "Refresh", "refresh", () => {
                    app.graph.setDirtyCanvas(true, true);
                    this.populate(this.predictions || []);
                });
            };

            nodeType.prototype.onExecuted = function(message) {
                this.updateExamples(message.examples || []);
            };

            nodeType.prototype.updateWidgets = function() {
                this.populate(this.predictions || []);
                this.setDirtyCanvas(true, true);
            };

            nodeType.prototype.updateExamples = function(examples) {
                console.log("Updating examples:", examples);
                if (this.widgets) {
                    // Remove old example widgets
                    for (let i = this.widgets.length - 1; i >= 0; i--) {
                        if (this.widgets[i].name.startsWith("example_")) {
                            this.widgets.splice(i, 1);
                        }
                    }
                }

                // Add new example widgets
                examples.forEach((example, index) => {
                    console.log(`Example ${index}:`, example);
                    const w = ComfyWidgets.STRING(this, `example_${index}`, ["STRING", { multiline: true }], app).widget;
                    w.inputEl.readOnly = false;
                    w.inputEl.style.opacity = 1;
                    w.value = `Input: ${example.input_text}\nOutput: ${example.output_text}`;
                    
                    // Increase the size of the textbox
                    w.inputEl.style.width = "300px";
                    w.inputEl.style.height = "100px";

                    // Add event listener for text changes
                    w.inputEl.addEventListener("change", () => {
                        updatePrediction(this.module_id, index, w.value);
                    });
                });

                this.setSize(this.computeSize());
                app.graph.setDirtyCanvas(true, true);
            };

            // Add computeSize method to adjust node size
            nodeType.prototype.computeSize = function() {
                return [350, 200 + this.widgets.length * 120]; // Adjust these numbers as needed
            };
        }
    }
});

api.addEventListener("update_node", (event) => {
    const data = event.detail;
    const node = app.graph.getNodeById(data.node_id);
    if (node && node.type === "Accepted Examples Viewer") {
        updateNodeData(node, data);
    }
});

async function removePrediction(module_id, output_text) {
    try {
        const response = await fetch('/accepted_examples_viewer/remove_prediction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ module_id, output_text }),
        });
        const responseData = await response.json();
        if (!response.ok) {
            throw new Error(responseData.message || `HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error removing prediction:', error);
    }
}

async function updatePrediction(module_id, prediction_id, new_text) {
    try {
        const response = await fetch('/accepted_examples_viewer/update_prediction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ module_id, prediction_id, new_text }),
        });
        const responseData = await response.json();
        if (!response.ok) {
            throw new Error(responseData.message || `HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error updating prediction:', error);
    }
}

function updateNodeData(node, data) {
    if (data.predictions) {
        node.predictions = data.predictions;
        node.module_id = data.predictions[0]?.module_id; // Store module_id
        node.populate(data.predictions);
    }
}

api.addEventListener("update_accepted_examples", ({ detail }) => {
    console.log("Received update_accepted_examples event:", detail);
    const node = app.graph.getNodeById(detail.node_id);
    if (node && node.comfyClass === "Accepted Examples Viewer") {
        node.updateExamples(detail.examples);
    }
});

import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "AcceptedExamplesViewer",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "AcceptedExamplesViewer") {

            nodeType.prototype.populate = function(predictions) {
                //console.log('fsr: populate with predictions:', predictions);
                if (this.widgets) {
                    for (let i = 1; i < this.widgets.length; i++) {
                        this.widgets[i].onRemove?.();
                    }
                    this.widgets.length = 1;
                }

                predictions.forEach((prediction, index) => {
                    const textWidget = ComfyWidgets["STRING"](this, `prediction_${index}`, ["STRING", { multiline: true }], app).widget;
                    textWidget.inputEl.readOnly = true;
                    textWidget.inputEl.style.opacity = 0.6;
                    textWidget.value = `Input: ${prediction.input_text}\nOutput: ${prediction.output_text}`;

                    const buttonWidget = this.addWidget("button", `Remove ${index + 1}`, `Remove`, () => {
                        //console.log(`fsr: Mark Good button clicked for prediction ${index}`);
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


            //nodeType.prototype.onNodeCreated = function() {
                //console.log("fsr: onNodeCreated");
                //this.addWidget("button", "Refresh", "Refresh", () => {
                    //console.log("fsr: Refresh button clicked");
                    //this.populate(this.predictions || []);
                //});
            //};

            nodeType.prototype.updateWidgets = function() {
                //console.log("fsr: updateWidgets");
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
                    w.inputEl.readOnly = true;
                    w.inputEl.style.opacity = 0.6;
                    w.value = `Input: ${example.input_text}\nOutput: ${example.output_text}`;
                });

                this.setSize(this.computeSize());
                app.graph.setDirtyCanvas(true, true);
            };
        }
    }
});

api.addEventListener("update_node", (event) => {
    //console.log("fsr: triggered update_node event", event);
    const data = event.detail;
    const node = app.graph.getNodeById(data.node_id);
    //console.log("fsr: node.type", node.type);
    if (node && node.type === "AcceptedExamplesViewer") {
        updateNodeData(node, data);
    }
});


async function removePrediction(module_id, output_text) {
    //console.log("fsr: Marking prediction as good:", output_text);
    try {
        const response = await fetch('/accepted_examples_viewer/remove_prediction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ module_id, output_text }),
        });
        //console.log("fsr: Mark Good response status:", response.status);
        const responseData = await response.json();
        //console.log('fsr: Mark Good response:', responseData);
        if (!response.ok) {
            throw new Error(responseData.message || `HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        //console.error('fsr: Error marking prediction as good:', error);
    }
}



function updateNodeData(node, data) {
    //console.log("fsr: Updating node data", data);
    if (data.predictions) {
        node.predictions = data.predictions;
        node.module_id = data.predictions[0]?.module_id; // Store module_id
        node.populate(data.predictions);
    }
}


api.addEventListener("update_accepted_examples", ({ detail }) => {
    console.log("Received update_accepted_examples event:", detail);
    const node = app.graph.getNodeById(detail.node_id);
    if (node && node.comfyClass === "AcceptedExamplesViewer") {
        node.updateExamples(detail.examples);
    }
});

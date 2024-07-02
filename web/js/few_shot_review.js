import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

console.log('fsr: init');

app.registerExtension({
    name: "FewShotReview",
    init() {
        // Any initialization code can go here
    },
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "Few Shot Review") {
            console.log('fsr: setting populate');
            nodeType.prototype.populate = function(predictions) {
                console.log('fsr: populate with predictions:', predictions);
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

                    //const buttonWidget = this.addWidget("button", `Mark Good ${index + 1}`, `Mark Good ${index + 1}`, () => {
                    const buttonWidget = this.addWidget("button", `Mark Good ${index + 1}`, `Mark Good`, () => {
                        console.log(`fsr: Mark Good button clicked for prediction ${index}`);
                        markGoodPrediction(this.module_id, prediction.output_text);
                    });
                });

                this.onResize?.(this.computeSize());
                app.graph.setDirtyCanvas(true, false);
            }

            nodeType.prototype.onNodeCreated = function() {
                console.log("fsr: onNodeCreated");
                this.addWidget("button", "Refresh", "Refresh", () => {
                    console.log("fsr: Refresh button clicked");
                    this.populate(this.predictions || []);
                });
            };

            nodeType.prototype.updateWidgets = function() {
                console.log("fsr: updateWidgets");
                this.populate(this.predictions || []);
                this.setDirtyCanvas(true, true);
            };
        }
    },
});

// Add the event listener
api.addEventListener("update_node", (event) => {
    console.log("fsr: triggered update_node event", event);
    const data = event.detail;
    const node = app.graph.getNodeById(data.node_id);
    console.log("fsr: node.type", node.type);
    if (node && node.type === "Few Shot Review") {
        updateNodeData(node, data);
    }
});

function updateNodeData(node, data) {
    console.log("fsr: Updating node data", data);
    if (data.predictions) {
        node.predictions = data.predictions;
        node.module_id = data.predictions[0]?.module_id; // Store module_id
        node.populate(data.predictions);
    }
}

async function markGoodPrediction(module_id, output_text) {
    console.log("fsr: Marking prediction as good:", output_text);
    try {
        const response = await fetch('/fewshotreview/mark_good', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ module_id, output_text }),
        });
        console.log("fsr: Mark Good response status:", response.status);
        const responseData = await response.json();
        console.log('fsr: Mark Good response:', responseData);
        if (!response.ok) {
            throw new Error(responseData.message || `HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('fsr: Error marking prediction as good:', error);
    }
}

async function callPrintEndpoint(text) {
    console.log("fsr: Attempting to send:", text);
    try {
        const jsonBody = JSON.stringify({ text: text });
        console.log("fsr: JSON being sent:", jsonBody);
        const response = await fetch('/fewshotreview/print', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: jsonBody,
        });
        console.log("fsr: Response status:", response.status);
        const responseData = await response.json();
        console.log('fsr: Print endpoint response:', responseData);
        if (!response.ok) {
            throw new Error(responseData.message || `HTTP error! status: ${response.status}`);
        }
    } catch (error) {
        console.error('fsr: Error calling print endpoint:', error);
    }
}

console.log('fsr: done');

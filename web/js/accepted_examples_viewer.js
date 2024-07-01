import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "AcceptedExamplesViewer",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "AcceptedExamplesViewer") {
            const onDrawForeground = nodeType.prototype.onDrawForeground;
            nodeType.prototype.onDrawForeground = function (ctx) {
                const ret = onDrawForeground?.apply?.(this, arguments);
                
                if (this.examples) {
                    ctx.save();
                    ctx.font = "bold 12px sans-serif";
                    ctx.fillStyle = "white";
                    ctx.textAlign = "left";
                    ctx.fillText(`Accepted Examples: ${this.examples.length}`, 10, 30);
                    ctx.restore();
                }
                
                return ret;
            };

            nodeType.prototype.onNodeCreated = function() {
                this.updateExamples = this.updateExamples.bind(this);
                this.addWidget("button", "Refresh", "refresh", () => {
                    api.executeNode(this.id);
                });
            };

            nodeType.prototype.updateExamples = function(examples) {
                this.examples = examples;
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
                    this.addWidget("text", `example_${index}`, `Example ${index + 1}`, () => {}, {
                        multiline: true,
                        value: `Input: ${example.input_text}\nOutput: ${example.output_text}`,
                        readonly: true
                    });
                });

                this.setSize([350, 30 + examples.length * 100]); // Adjust size based on number of examples
                app.graph.setDirtyCanvas(true, true);
            };
        }
    }
});

api.addEventListener("update_accepted_examples", ({ detail }) => {
    const node = app.graph.getNodeById(detail.node_id);
    if (node && node.type === "AcceptedExamplesViewer") {
        node.updateExamples(detail.examples);
    }
});

import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

console.log("slv: loaded");

app.registerExtension({
    name: "String List Viewer",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "String List Viewer") {

            nodeType.prototype.populate = function(stringList) {
                if (this.widgets) {
                    for (let i = 1; i < this.widgets.length; i++) {
                        this.widgets[i].onRemove?.();
                    }
                    this.widgets.length = 1;
                }

                stringList.forEach((item, index) => {
                    const textWidget = ComfyWidgets["STRING"](this, `string_${index}`, ["STRING", { multiline: true }], app).widget;
                    textWidget.inputEl.readOnly = true;
                    textWidget.inputEl.style.opacity = 0.8;
                    textWidget.value = item.text;
                    
                    // Increase the size of the textbox
                    textWidget.inputEl.style.width = "300px";
                    textWidget.inputEl.style.height = "100px";
                });

                this.onResize?.(this.computeSize());
                app.graph.setDirtyCanvas(true, false);
            }

            nodeType.prototype.onNodeCreated = function() {
                this.addWidget("button", "Refresh", "refresh", () => {
                    app.graph.setDirtyCanvas(true, true);
                    this.populate(this.stringList || []);
                });
            };

            nodeType.prototype.updateWidgets = function() {
                this.populate(this.stringList || []);
                this.setDirtyCanvas(true, true);
            };

            // Add computeSize method to adjust node size
            nodeType.prototype.computeSize = function() {
                return [350, 200 + this.widgets.length * 120]; // Adjust these numbers as needed
            };
        }
    }
});

api.addEventListener("update_string_list", (event) => {
    const data = event.detail;
    const node = app.graph.getNodeById(data.node_id);
    if (node && node.type === "String List Viewer") {
        updateNodeData(node, data);
    }
});

function updateNodeData(node, data) {
    console.log("slv: updateNodeData", node, data);
    if (data.string_list) {
        node.stringList = data.string_list;
        node.populate(data.string_list);
    }
}

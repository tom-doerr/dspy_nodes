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



                                     //function populate(text) {
                                    //console.log('fsr: populate');
				//if (this.widgets) {
					//for (let i = 1; i < this.widgets.length; i++) {
						//this.widgets[i].onRemove?.();
					//}
					//this.widgets.length = 1;
				//}

				//const v = [...text];
				//if (!v[0]) {
					//v.shift();
				//}
				//for (const list of v) {
					//const w = ComfyWidgets["STRING"](this, "text", ["STRING", { multiline: true }], app).widget;
					//w.inputEl.readOnly = true;
					//w.inputEl.style.opacity = 0.6;
					//w.value = list;
				//}

				//requestAnimationFrame(() => {
					//const sz = this.computeSize();
					//if (sz[0] < this.size[0]) {
						//sz[0] = this.size[0];
					//}
					//if (sz[1] < this.size[1]) {
						//sz[1] = this.size[1];
					//}
					//this.onResize?.(sz);
					//app.graph.setDirtyCanvas(true, false);
				//});
			//}


 			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
                                console.log('fsr: onExecuted');
				onExecuted?.apply(this, arguments);
				//populate.call(this, message.text);
			};
                                 
			const onConfigure = nodeType.prototype.onConfigure;
			nodeType.prototype.onConfigure = function () {
                                console.log('fsr: onConfigure');
				onConfigure?.apply(this, arguments);
				if (this.widgets_values?.length) {
					//populate.call(this, this.widgets_values);
				}
			};



                                     //function populate(text) {
            console.log('fsr: setting populate');
            nodeType.prototype.populate = function(text) {
                                    console.log('fsr: populate');
				if (this.widgets) {
					for (let i = 1; i < this.widgets.length; i++) {
						this.widgets[i].onRemove?.();
					}
					this.widgets.length = 1;
				}

				const v = [...text];
				if (!v[0]) {
					v.shift();
				}
				for (const list of v) {
					const w = ComfyWidgets["STRING"](this, "text", ["STRING", { multiline: true }], app).widget;
					w.inputEl.readOnly = true;
					w.inputEl.style.opacity = 0.6;
					w.value = list;
				}

				requestAnimationFrame(() => {
					const sz = this.computeSize();
					if (sz[0] < this.size[0]) {
						sz[0] = this.size[0];
					}
					if (sz[1] < this.size[1]) {
						sz[1] = this.size[1];
					}
					this.onResize?.(sz);
					app.graph.setDirtyCanvas(true, false);
				});
			}


            const onDrawForeground = nodeType.prototype.onDrawForeground;
            nodeType.prototype.onDrawForeground = function (ctx) {
                const r = onDrawForeground?.apply?.(this, arguments);
                // Add any custom drawing code here
                return r;
            };

            nodeType.prototype.createWidgets = function() {
                this.addInfoWidget();
                this.addSelectedTextWidget();
                this.addPredictionsWidget();
            };

            nodeType.prototype.addInfoWidget = function() {
                let w = this.widgets?.find((w) => w.name === "info");
                if (w === undefined) {
                    w = ComfyWidgets["STRING"](this, "info", ["STRING", { multiline: true }], app).widget;
                    w.inputEl.readOnly = true;
                    w.inputEl.style.opacity = 0.6;
                    w.inputEl.style.fontSize = "9pt";
                }
                w.value = "FewShotReview Node Info";
                this.onResize?.(this.size);
            };

            nodeType.prototype.addSelectedTextWidget = function() {
                let w = this.widgets?.find((w) => w.name === "selectedText");
                if (w === undefined) {
                    w = ComfyWidgets["STRING"](this, "selectedText", ["STRING", { multiline: true }], app).widget;
                }
                w.value = this.properties?.selectedText || "";
                this.onResize?.(this.size);
            };


            nodeType.prototype.addButton = function() {
                const reverseButton = this.addWidget("button", "Reverse", "Reverse", () => {
                    console.log("fsr: Reverse button clicked");
                    console.log("Reverse button clicked");
                    callPrintEndpoint("test jkl");  // Call the new endpoint

                });
            };




            nodeType.prototype.addPredictionsWidget = function() {
                let w = this.widgets?.find((w) => w.name === "predictions");
                if (w === undefined) {
                    w = ComfyWidgets["COMBO"](this, "predictions", ["COMBO", { values: [] }], app).widget;
                }
                w.options.values = this.properties?.predictions?.map(p => p.text) || [];
                w.value = this.properties?.predictions?.[0]?.text || "";
                this.onResize?.(this.size);
            };

            nodeType.prototype.removeWidget = function(widget_name) {
                const w = this.widgets?.findIndex((w) => w.name === widget_name);
                if (w >= 0) {
                    const wid = this.widgets[w];
                    this.widgets.splice(w, 1);
                    wid?.onRemove?.();
                    this.size = this.computeSize();
                    this.setDirtyCanvas(true, true);
                }
            };

            nodeType.prototype.updateWidgets = function() {
                console.log("fsr: updateWidgets");
                this.removeWidget("selectedText");
                this.removeWidget("predictions");
                this.addSelectedTextWidget();
                this.addPredictionsWidget();
                this.addButton();
                this.setDirtyCanvas(true, true);
            };

            //const onNodeCreated = nodeType.prototype.onNodeCreated;
            //nodeType.prototype.onNodeCreated = function() {
                //console.log("fsr: onNodeCreated");
                //onNodeCreated?.apply(this, arguments);
                //const reverseButton = this.addWidget("button", "Reverse", "Reverse", () => {
                    //console.log("fsr: Reverse button clicked");
                    //console.log("Reverse button clicked");
                    //callPrintEndpoint("test jkl");  // Call the new endpoint


                //});
            //};
        }
    },
});

// Add the event listener
api.addEventListener("update_node", (event) => {
    console.log("fsr: triggered update_node event", event);
    const data = event.detail;
    const node = app.graph.getNodeById(data.node_id);
    //console.log("fsr: Found node", node);
    console.log("fsr: node.type", node.type);
    if (node && node.type === "Few Shot Review") {
    //if (node) {
        updateNodeData(node, data);
    }
});

function updateNodeData(node, data) {
    console.log("fsr: Updating node data", data);
    if (data.predictions) {
        node.properties.predictions = data.predictions;
    }
    if (data.selectedText) {
        node.properties.selectedText = data.selectedText;
    }
    console.log("fsr: Calling populate");
    node.populate([data.selectedText]);
    console.log("fsr: Calling updateWidgets");
    node.updateWidgets();
    //node.populate(data.selectedText);
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

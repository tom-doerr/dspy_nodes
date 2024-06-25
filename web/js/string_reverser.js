import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "org.example.StringReverser",
    async setup(app) {
        console.log("StringReverser setup function called");
    },
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "StringReverser") {
            console.log("Modifying StringReverser node");
            
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                onNodeCreated?.apply(this, arguments);
                console.log("StringReverser node created");

                const reverseButton = this.addWidget("button", "Reverse", "Reverse", () => {
                    console.log("Reverse button clicked");
                    if (this.widgets[0] && this.widgets[0].type === "string") {
                        const inputText = this.widgets[0].value;
                        const reversedText = inputText.split('').reverse().join('');
                        this.widgets[0].value = reversedText;
                        this.onResize?.(this.size);  // Ensure the node resizes if needed
                        app.graph.setDirtyCanvas(true, true);
                    }
                });

                // Move the button widget to be right after the input widget
                this.widgets.splice(1, 0, this.widgets.pop());
            };

            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                onExecuted?.apply(this, arguments);
                console.log("StringReverser node executed", message);
            };
        }
    },
});

console.log("StringReverser extension file loaded");

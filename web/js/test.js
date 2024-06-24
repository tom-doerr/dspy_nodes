import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "org.example.dynamic_options",
    async nodeCreated(node) {
        if (node.comfyClass === "DynamicOptionsNode") {
            const updateOptions = async () => {
                const category = node.widgets[0].value;
                const resp = await api.fetchApi('/object_info/DynamicOptionsNode', {
                    method: 'POST',
                    body: JSON.stringify({
                        "required": {
                            "category": category
                        }
                    })
                });
                const data = await resp.json();
                const options = data.input.required.selection[0];
                node.widgets[1].options.values = options;
                node.widgets[1].value = options[0] || "";
            };

            node.widgets[0].callback = () => {
                updateOptions();
            };

            // Initial update
            updateOptions();
        }
    }
});

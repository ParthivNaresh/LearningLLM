import React from "react";

interface ModelSelectorProps {
    models: string[];
    selectedModel: string;
    onSelectModel: (model: string) => void;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ models, selectedModel, onSelectModel }) => {
    return (
        <div className="flex flex-col w-full">
            <label className="font-semibold mb-1">Select Model:</label>
            <select
                className="border rounded p-2 text-black"
                value={selectedModel}
                onChange={(e) => onSelectModel(e.target.value)}
            >
                {models.length > 0 ? (
                    models.map((model) => (
                        <option key={model} value={model}>{model}</option>
                    ))
                ) : (
                    <option>Select a Model</option>
                )}
            </select>
        </div>
    );
};

export default ModelSelector;

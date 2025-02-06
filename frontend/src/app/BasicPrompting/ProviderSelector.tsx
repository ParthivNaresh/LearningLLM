import React from "react";

interface ProviderSelectorProps {
    apiKeys: { [key: string]: string };
    selectedProvider: string;
    onSelectProvider: (provider: string) => void;
}

const ProviderSelector: React.FC<ProviderSelectorProps> = ({ apiKeys, selectedProvider, onSelectProvider }) => {
    return (
        <div className="flex flex-col w-full mt-4">
            <label className="font-semibold mb-1">Select Provider:</label>
            <select
                className="border rounded p-2 text-black"
                value={selectedProvider}
                onChange={(e) => onSelectProvider(e.target.value)}
            >
                <option value="">Select a Provider</option>
                {Object.keys(apiKeys).map((provider) => (
                    <option key={provider} value={provider}>{provider}</option>
                ))}
            </select>
        </div>
    );
};

export default ProviderSelector;

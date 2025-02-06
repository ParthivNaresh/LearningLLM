import React from "react";
import FileUpload from "./FileUpload";
import ProviderSelector from "./ProviderSelector";
import ModelSelector from "./ModelSelector";
import PromptInput from "./PromptInput";
import ResponseOutput from "./ResponseOutput";

interface BasicPromptingPageProps {
    apiKeys: { [key: string]: string };
    selectedProvider: string;
    selectedModel: string;
    models: string[];
    prompt: string;
    result: string;
    onApiKeysLoaded: (apiKeys: { [key: string]: string }) => void;
    onSelectProvider: (provider: string) => void;
    onSelectModel: (model: string) => void;
    onPromptChange: (prompt: string) => void;
    onResult: (result: string) => void;
}

const BasicPromptingPage: React.FC<BasicPromptingPageProps> = ({
    apiKeys,
    selectedProvider,
    selectedModel,
    models,
    prompt,
    result,
    onApiKeysLoaded,
    onSelectProvider,
    onSelectModel,
    onPromptChange,
    onResult,
}) => {

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const currentApiKey = apiKeys[selectedProvider];
        const requestData = {
            prompt,
            provider: selectedProvider,
            model: selectedModel,
        };

        try {
            const response = await fetch("http://localhost:8000/api/v1/generate", {
                method: "POST",
                mode: "cors",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': `Bearer ${currentApiKey}`,
                },
                body: JSON.stringify(requestData),
            });
            const data = await response.json();
            onResult(data.content);
        } catch (error) {
            console.error("Error calling backend:", error);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-col w-1/2 gap-4">
            <FileUpload onApiKeysLoaded={onApiKeysLoaded} />
            <ProviderSelector
                apiKeys={apiKeys}
                selectedProvider={selectedProvider}
                onSelectProvider={onSelectProvider}
            />
            <ModelSelector
                models={models}
                selectedModel={selectedModel}
                onSelectModel={onSelectModel}
            />
            <PromptInput prompt={prompt} onPromptChange={onPromptChange} />
            <button type="submit" className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">
                Generate
            </button>
            <ResponseOutput result={result} />
        </form>
    );
};

export default BasicPromptingPage;

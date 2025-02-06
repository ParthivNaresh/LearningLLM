"use client";
import React, {useEffect, useState} from "react";
import BasicPromptingPage from "./BasicPrompting/BasicPromptingPage";
import Tabs from "@/app/Tabs";
import RAGPage from "@/app/RAG/RAGPage";

export default function Home() {
    const [activeTab, setActiveTab] = useState<string>("Basic Prompting");
    const [apiKeys, setApiKeys] = useState<{ [key: string]: string }>({});
    const [prompt, setPrompt] = useState("");
    const [result, setResult] = useState("");
    const [selectedModel, setSelectedModel] = useState("");
    const [selectedProvider, setSelectedProvider] = useState<string>("");
    const [models, setModels] = useState([]);

    useEffect(() => {
        if (!selectedProvider || !apiKeys[selectedProvider]) {
            setModels([]);
            return;
        }

        const fetchModels = async () => {
            const currentApiKey = apiKeys[selectedProvider];
            try {
                const response = await fetch(
                    `http://localhost:8000/api/v1/models?provider=${selectedProvider}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${currentApiKey}`,
                        },
                    }
                );
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                if (!Array.isArray(data.models)) {
                    console.error("Unexpected response format for models:", data);
                    return;
                }
                setModels(data.models);
                if (data.models.length > 0) {
                    setSelectedModel(data.models[0]);
                }
            } catch (error) {
                console.error("Error getting models:", error);
            }
        };

        fetchModels();
    }, [selectedProvider, apiKeys]);

    return (
        <div className="flex flex-col min-h-screen p-8 gap-6">
            <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
            <div className="flex flex-row gap-6 p-4">
                {activeTab === "Basic Prompting" && (
                    <BasicPromptingPage
                        apiKeys={apiKeys}
                        selectedProvider={selectedProvider}
                        selectedModel={selectedModel}
                        models={models}
                        prompt={prompt}
                        result={result}
                        onApiKeysLoaded={setApiKeys}
                        onSelectProvider={setSelectedProvider}
                        onSelectModel={setSelectedModel}
                        onPromptChange={setPrompt}
                        onResult={setResult}
                    />
                )}
                {activeTab === "RAG" && <RAGPage />}
                {activeTab === "Agentic AI"}
                {activeTab === "Model Comparison"}

                {/*{activeTab === "RAG" && <RAGPlayground apiKeys={apiKeys} />}*/}
                {/*{activeTab === "Agentic AI" && <AgentSimulator />}*/}
                {/*{activeTab === "Model Comparison" && <ModelComparison />}*/}
            </div>
        </div>
    );
}

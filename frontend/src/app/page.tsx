"use client";
import React, {useEffect, useState} from "react";

export default function Home() {
    const [prompt, setPrompt] = useState("");
    const [result, setResult] = useState("");
    const [providers, setProviders] = useState([]);
    const [models, setModels] = useState([]);
    const [selectedProvider, setSelectedProvider] = useState("anthropic");
    const [selectedModel, setSelectedModel] = useState("");
    const [apiKey, setApiKey] = useState("");

    useEffect(() => {
        async function getProviders() {
            try {
                const response = await fetch("http://localhost:8000/api/v1/providers", {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                const data = await response.json();
                setProviders(data.providers);
            } catch (error) {
                console.error("Error getting providers.", error);
            }
        }
        getProviders();
    }, []);

    useEffect(() => {
        async function getModels() {
            try {
                const response = await fetch(`http://localhost:8000/api/v1/models?provider=${selectedProvider}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': apiKey ? `Bearer ${apiKey}` : "",
                    },
                });
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
                console.error("Error getting models.", error);
            }
        }
        getModels();
    }, [providers, selectedProvider, apiKey]);

    console.log("🚀 Sending API Key:", apiKey);
    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        if (!apiKey) {
            alert("Please enter your API key.");
            return;
        }

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
                    'Authorization': apiKey ? `Bearer ${apiKey}` : "",
                },
                body: JSON.stringify(requestData),
            });
            const data = await response.json();
            setResult(data.content);
        } catch (error) {
            console.error("Error calling backend:", error);
        }
    }

    return (
        <div className="flex flex-row min-h-screen p-8 gap-6">
            <div className="flex flex-col items-start w-1/2 p-8 gap-6">
                <h1 className="text-2xl font-bold">LLM Playground</h1>
                <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-md">
                    <div className="flex flex-col w-full">
                        <label className="font-semibold mb-1">Enter Your API Key:</label>
                        <input
                            type="password"
                            className="border rounded p-2 text-black"
                            placeholder="Enter API Key"
                            value={apiKey}
                            onChange={(e) => setApiKey(e.target.value)}
                        />
                    </div>

                    <div className="flex flex-col w-full">
                        <label className="font-semibold mb-1">Select Provider:</label>
                        <select
                            className="border rounded p-2 text-black"
                            value={selectedProvider}
                            onChange={(e) => setSelectedProvider(e.target.value)}
                        >
                            {providers.length > 0 ? (
                                providers.map((provider) => (
                                    <option key={provider} value={provider}>{provider}</option>
                                ))
                            ) : (
                                <option>Loading providers...</option>
                            )}
                        </select>
                    </div>

                    <div className="flex flex-col w-full">
                        <label className="font-semibold mb-1">Select Model:</label>
                        <select
                            className="border rounded p-2 text-black"
                            value={selectedModel}
                            onChange={(e) => setSelectedModel(e.target.value)}
                        >
                            {models.length > 0 ? (
                                models.map((model) => (
                                    <option key={model} value={model}>{model}</option>
                                ))
                            ) : (
                                <option>Loading models...</option>
                            )}
                        </select>
                    </div>

                    <div className="flex flex-col w-full">
                        <label className="font-semibold mb-1">Enter your prompt:</label>
                        <textarea
                            className="border rounded p-2 min-h-[100px] text-black"
                            placeholder="Type your prompt here..."
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
                    >
                        Generate
                    </button>

                    <div className="flex flex-col w-full">
                        <label className="font-semibold mb-1">Model Response:</label>
                        <textarea
                            className="border rounded p-2 min-h-[200px] text-black"
                            placeholder="Type your prompt here..."
                            value={result}
                            onChange={(e) => setPrompt(e.target.value)}
                        />
                    </div>
                </form>
            </div>

            <div className="w-1/2 p-4 border-l border-gray-300">
                <h2 className="text-xl font-bold mb-2">Additional Content</h2>
                <p className="text-gray-600">This is where you can add extra components, such as:</p>
                <ul className="list-disc pl-4">
                    <li>Settings</li>
                    <li>Instructions</li>
                    <li>Chat History</li>
                    <li>Other Tools</li>
                </ul>
            </div>
        </div>
    );
}

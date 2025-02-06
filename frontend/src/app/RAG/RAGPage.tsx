import React, { useState } from "react";
import RAGUpload from "./RAGUpload";
import SegmentationOptions from "./SegmentationOptions";
import VectorStoreSelection from "./VectorStoreSelection";
import RAGQuery from "./RAGQuery";

const RAGPage: React.FC = () => {
    // State for file, segmentation, vector store, and query
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [segmentationMethod, setSegmentationMethod] = useState<string>("Fixed Size");
    const [vectorStore, setVectorStore] = useState<string>("FAISS");
    const [retrievedContext, setRetrievedContext] = useState<string>("");

    // Upload file handler
    const handleFileUpload = async (file: File) => {
        setUploadedFile(file);

        // Prepare file for upload
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:8000/upload", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            console.log("File processed:", data);
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    // Query retrieval handler
    const handleQuery = async (query: string) => {
        try {
            const response = await fetch(`http://localhost:8000/query?query=${query}`, {
                method: "GET",
            });

            const data = await response.json();
            setRetrievedContext(data.retrieved_context);
        } catch (error) {
            console.error("Error querying RAG:", error);
        }
    };

    return (
        <div className="flex flex-col w-full gap-4">
            <h1 className="text-2xl font-bold text-white">RAG Playground</h1>

            <RAGUpload onFileUpload={handleFileUpload} />
            <SegmentationOptions
                segmentationMethod={segmentationMethod}
                onSegmentationChange={setSegmentationMethod}
            />
            <VectorStoreSelection
                vectorStore={vectorStore}
                onSelectVectorStore={setVectorStore}
            />
            <RAGQuery onQuery={handleQuery} />

            {retrievedContext && (
                <div className="p-4 border rounded bg-gray-100">
                    <h2 className="text-lg font-semibold">Retrieved Context:</h2>
                    <p className="text-gray-700">{retrievedContext}</p>
                </div>
            )}
        </div>
    );
};

export default RAGPage;

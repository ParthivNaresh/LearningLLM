import React from "react";

interface VectorStoreSelectionProps {
    vectorStore: string;
    onSelectVectorStore: (store: string) => void;
}

const VectorStoreSelection: React.FC<VectorStoreSelectionProps> = ({ vectorStore, onSelectVectorStore }) => {
    const stores = ["FAISS", "Pinecone", "ChromaDB"];

    return (
        <div className="border border-gray-600 rounded-lg p-6 bg-gray-800 shadow-md">
            <h2 className="text-xl font-bold text-white mb-4">Select Vector Database</h2>
            <select
                className="w-full p-3 bg-gray-900 border border-gray-600 text-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={vectorStore}
                onChange={(e) => onSelectVectorStore(e.target.value)}
            >
                {stores.map((store) => (
                    <option key={store} value={store} className="bg-gray-900 text-white">
                        {store}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default VectorStoreSelection;

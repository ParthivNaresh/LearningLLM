import React, { useState } from "react";

interface RAGQueryProps {
    onQuery: (query: string) => void;
}

const RAGQuery: React.FC<RAGQueryProps> = ({ onQuery }) => {
    const [query, setQuery] = useState("");

    return (
        <div className="border border-gray-600 rounded-lg p-6 bg-gray-800 shadow-md">
            <h2 className="text-xl font-bold text-white mb-4">Ask a Question</h2>
            <input
                type="text"
                className="w-full p-3 bg-gray-900 border border-gray-600 text-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-500"
                placeholder="Type your query..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button
                className="bg-blue-600 text-white px-4 py-3 rounded-md mt-4 hover:bg-blue-700 transition-all duration-200 w-full"
                onClick={() => onQuery(query)}
                disabled={!query.trim()}
            >
                Retrieve Context
            </button>
        </div>
    );
};

export default RAGQuery;

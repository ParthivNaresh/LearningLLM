import React, { useState } from "react";

interface RAGUploadProps {
    onFileUpload: (file: File) => void;
}

const RAGUpload: React.FC<RAGUploadProps> = ({ onFileUpload }) => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files?.[0]) {
            setSelectedFile(event.target.files[0]);
            onFileUpload(event.target.files[0]);
        }
    };

    return (
        <div className="border border-gray-600 rounded-lg p-6 bg-gray-800 shadow-md">
            <h2 className="text-xl font-bold text-white mb-4">Upload Documents</h2>
            <input
                type="file"
                accept=".pdf,.txt,.csv,.md"
                className="block w-full text-sm text-gray-300
                           file:mr-4 file:py-2 file:px-4
                           file:rounded-md file:border-0
                           file:text-sm file:font-semibold
                           file:bg-blue-500 file:text-white
                           hover:file:bg-blue-600"
                onChange={handleFileChange}
            />
            {selectedFile && (
                <p className="mt-4 text-sm text-gray-400">
                    <span className="font-medium text-white">Selected File:</span> {selectedFile.name}
                </p>
            )}
        </div>
    );
};

export default RAGUpload;

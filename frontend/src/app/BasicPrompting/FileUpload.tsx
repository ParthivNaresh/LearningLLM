import React from "react";

interface FileUploadProps {
    onApiKeysLoaded: (apiKeys: { [key: string]: string }) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onApiKeysLoaded }) => {
    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                if (e.target?.result) {
                    const json = JSON.parse(e.target.result as string);
                    onApiKeysLoaded(json); // Send parsed data back to parent
                }
            } catch (error) {
                alert("Invalid JSON file format.");
            }
        };
        reader.readAsText(file);
    };

    return (
        <div className="flex flex-col w-full">
            <label className="font-semibold mb-1">Upload a JSON file with provider API keys:</label>
            <input
                type="file"
                accept=".json"
                className="border rounded p-2 text-black"
                onChange={handleFileUpload}
            />
        </div>
    );
};

export default FileUpload;

import React from "react";

interface PromptInputProps {
    prompt: string;
    onPromptChange: (prompt: string) => void;
}

const PromptInput: React.FC<PromptInputProps> = ({ prompt, onPromptChange }) => {
    return (
        <div className="flex flex-col w-full">
            <label className="font-semibold mb-1">Enter your prompt:</label>
            <textarea
                className="border rounded p-2 min-h-[100px] text-black"
                placeholder="Type your prompt here..."
                value={prompt}
                onChange={(e) => onPromptChange(e.target.value)}
            />
        </div>
    );
};

export default PromptInput;

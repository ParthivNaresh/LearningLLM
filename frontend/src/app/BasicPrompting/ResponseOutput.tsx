import React from "react";

interface ResponseOutputProps {
    result: string;
}

const ResponseOutput: React.FC<ResponseOutputProps> = ({ result }) => {
    return (
        <div className="flex flex-col w-full">
            <label className="font-semibold mb-1">Model Response:</label>
            <textarea
                className="border rounded p-2 min-h-[200px] text-black"
                value={result}
                readOnly
            />
        </div>
    );
};

export default ResponseOutput;

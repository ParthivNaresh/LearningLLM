import React from "react";

interface SegmentationOptionsProps {
    segmentationMethod: string;
    onSegmentationChange: (method: string) => void;
}

const SegmentationOptions: React.FC<SegmentationOptionsProps> = ({ segmentationMethod, onSegmentationChange }) => {
    const methods = ["Fixed Size", "Sentence-based", "Overlapping Chunks"];

    return (
        <div className="border border-gray-600 rounded-lg p-6 bg-gray-800 shadow-md">
            <h2 className="text-xl font-bold text-white mb-4">Choose Segmentation</h2>
            <select
                className="w-full p-3 bg-gray-900 border border-gray-600 text-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={segmentationMethod}
                onChange={(e) => onSegmentationChange(e.target.value)}
            >
                {methods.map((method) => (
                    <option key={method} value={method} className="bg-gray-900 text-white">
                        {method}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default SegmentationOptions;

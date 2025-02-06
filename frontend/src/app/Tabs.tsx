import React from "react";

interface TabsProps {
    activeTab: string;
    setActiveTab: (tab: string) => void;
}

const Tabs: React.FC<TabsProps> = ({ activeTab, setActiveTab }) => {
    const tabs = ["Basic Prompting", "RAG", "Agentic AI", "Model Comparison"];

    return (
        <div className="flex border-b border-gray-300">
            {tabs.map((tab) => (
                <button
                    key={tab}
                    className={`py-2 px-4 text-lg font-semibold ${
                        activeTab === tab ? "border-b-2 border-blue-500 text-blue-600" : "text-gray-500"
                    } hover:text-blue-500 transition-colors`}
                    onClick={() => setActiveTab(tab)}
                >
                    {tab}
                </button>
            ))}
        </div>
    );
};

export default Tabs;



PROVIDER_MAP = {
    "anthropic": ("langchain_anthropic", "ChatAnthropic"),
    "openai": ("langchain_openai", "ChatOpenAI"),
    "vertex": ("langchain_google_vertexai", "ChatVertexAI"),
    "cohere": ("langchain_cohere", "ChatCohere"),
    "nvidia": ("langchain_nvidia_ai_endpoints", "ChatNVIDIA"),
    "groq": ("langchain_groq", "ChatGroq"),
    "mistral": ("langchain_mistralai", "ChatMistralAI"),
    "databricks": ("databricks_langchain", "ChatDatabricks"),
    "aws": ("langchain_aws", "ChatBedrock"),
    "azure": ("langchain_openai", "AzureChatOpenAI"),
    "fireworks": ("langchain_fireworks", "ChatFireworks"),
    "together": ("langchain_together", "ChatTogether"),
    "google": ("langchain_google_genai", "ChatGoogleGenerativeAI"),
    "huggingface": ("langchain_huggingface", "ChatHuggingFace"),
    "ollama": ("langchain_ollama", "ChatOllama"),
    "upstage": ("langchain_upstage", "ChatUpstage"),
    "ibm": ("langchain_ibm", "ChatWatsonx"),
    "xai": ("langchain_xai", "ChatXAI"),
}



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
    "fireworks": ("langchain-fireworks", "ChatFireworks"),
    "together": ("langchain-together", "ChatTogether"),
    "google": ("langchain-google-genai", "ChatGoogleGenerativeAI"),
    "huggingface": ("langchain-huggingface", "ChatHuggingFace"),
    "ollama": ("langchain-ollama", "ChatOllama"),
    "ai21": ("langchain-ai21", "ChatAI21"),
    "upstage": ("langchain-upstage", "ChatUpstage"),
    "ibm": ("langchain-ibm", "ChatWatsonx"),
    "xai": ("langchain-xai", "ChatXAI"),
}
import httpx
from fastapi import FastAPI, APIRouter, HTTPException, Query, Header
from threading import Lock

from langchain_core.messages import SystemMessage, HumanMessage

from backend.utils import load_chat_provider, fetch_models
from backend.utils.api_body_definitions import ModelsResponse, GenerateRequest, GenerateResponse, ProvidersResponse
from backend.utils.constants import PROVIDER_MAP
from starlette.middleware.cors import CORSMiddleware


def generate_response(prompt: str, provider: str, model: str, api_key: str):
    provider_class = load_chat_provider(provider)
    class_instance = provider_class(model=model, api_key=api_key)
    messages = [
        SystemMessage("Answer the following question:"),
        HumanMessage(prompt),
    ]
    return class_instance.invoke(messages)


def list_available_providers():
    return PROVIDER_MAP.keys()


async def list_available_models(provider: str, api_key: str):
    url, headers = fetch_models(provider, api_key=api_key)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                if provider != "huggingface":
                    return [model["id"] for model in response.json().get("data", [])]
                else:
                    return [model["id"] for model in response.json()]
            else:
                return [f"Error fetching {provider}: {response.status_code}"]
        except Exception as e:
            return [f"Error: {str(e)}"]


class API:
    def __init__(self, app: FastAPI, queue_lock: Lock):
        self.app = app
        self.queue_lock = queue_lock
        # Middleware (CORS, logging, etc.)
        self.setup_middleware()
        self.router = APIRouter()

        # API Routes
        self.router.add_api_route(
            "/api/v1/providers",
            self.get_providers,
            methods=["GET"],
            response_model=ProvidersResponse
        )
        self.router.add_api_route(
            "/api/v1/models",
            self.get_models,
            methods=["GET"],
            response_model=ModelsResponse
        )
        self.router.add_api_route(
            "/api/v1/generate",
            self.generate_text,
            methods=["POST"],
            response_model=GenerateResponse
        )

        # Register routes
        self.app.include_router(self.router)

    def setup_middleware(self):
        """Add middleware (CORS, logging, etc.)"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    async def get_providers(self) -> ProvidersResponse:
        """Return available models"""
        return ProvidersResponse(providers=list_available_providers())

    async def get_models(self, provider: str = Query(...), authorization: str = Header(None)) -> ModelsResponse:
        """Return available models"""
        print(f"Received Authorization Header: {authorization}")  # Debug print
        if not authorization:
            raise HTTPException(status_code=401, detail="Missing API key")

        api_key = authorization.split("Bearer ")[1]

        if provider not in PROVIDER_MAP:
            raise HTTPException(status_code=400, detail="Invalid provider selection")
        models = await list_available_models(provider, api_key)
        return ModelsResponse(models=models)

    async def generate_text(self, request: GenerateRequest, authorization: str = Header(None)) -> GenerateResponse:
        """Generate text using the selected model"""
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing API key")
        if request.provider not in list_available_providers():
            raise HTTPException(status_code=400, detail="Invalid provider selection")

        api_key = authorization.replace("Bearer ", "", 1).strip()
        available_models = await list_available_models(request.provider, api_key)
        if request.model not in available_models:
            raise HTTPException(status_code=400, detail="Invalid model selection")

        #result_data = generate_response(request.prompt, request.provider, request.model, api_key)
        result_data = {}
        response_dict = dict(result_data)

        return GenerateResponse(
            content=response_dict.get("content", f"This is a sample mock response from the prompt '{request.prompt}'"),
            response_metadata=response_dict.get("response_metadata"),
            type=response_dict.get("type", ""),
            name=response_dict.get("name"),
            id=response_dict.get("id", ""),
            example=response_dict.get("example", False),
            tool_calls=response_dict.get("tool_calls", []),
            invalid_tool_calls=response_dict.get("invalid_tool_calls", []),
            usage_metadata=response_dict.get("usage_metadata")
        )


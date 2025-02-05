from typing import List, Optional

from pydantic import BaseModel


class ModelsRequest(BaseModel):
    provider: str
    api_key: str


class GenerateRequest(BaseModel):
    prompt: str
    provider: str
    model: str


class ProvidersResponse(BaseModel):
    providers: List[str]


class ModelsResponse(BaseModel):
    models: List[str]


class TokenUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_time: Optional[float] = None
    prompt_time: Optional[float] = None
    queue_time: Optional[float] = None
    total_time: Optional[float] = None


class ResponseMetadata(BaseModel):
    token_usage: TokenUsage
    model_name: str
    system_fingerprint: str
    finish_reason: str
    logprobs: Optional[dict] = None


class UsageMetadata(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class GenerateResponse(BaseModel):
    content: str
    response_metadata: Optional[ResponseMetadata] = None
    type: str
    name: Optional[str]
    id: str
    example: bool
    tool_calls: List[dict]
    invalid_tool_calls: List[dict]
    usage_metadata: Optional[UsageMetadata] = None

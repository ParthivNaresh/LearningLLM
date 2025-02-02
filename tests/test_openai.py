import os
import pytest
from LearningLLM.providers.openai_provider import OpenAIProvider


@pytest.fixture(scope="module")
def openai_provider():
    """
    Pytest fixture to instantiate the provider once for all tests.
    If no API key is found, we skip these tests.
    """
    api_key = ""
    if not api_key:
        pytest.skip("No OPENAI_API_KEY set. Skipping OpenAIProvider tests.")
    provider = OpenAIProvider(api_key=api_key, model_name="gpt-3.5-turbo")
    return provider


def test_list_models(openai_provider):
    """
    Verify that list_models returns a list of model IDs (strings).
    """
    model_ids = openai_provider.list_models()
    assert isinstance(model_ids, list), "list_models() should return a list."
    if len(model_ids) > 0:
        assert isinstance(model_ids[0], str), "Each model ID should be a string."
    print(model_ids)


def test_set_model(openai_provider):
    """
    Ensure we can switch models (though many OpenAI model IDs might be hidden).
    We'll do a basic check that the model name is updated internally.
    """
    model_name = "gpt-3.5-turbo"
    openai_provider.set_model(model_name)
    assert openai_provider.model_name == model_name, "Model name should be set."


def test_generate(openai_provider):
    """
    Verify text generation produces a non-empty string.
    """
    prompt = "Hello, how are you?"
    output = openai_provider.generate(prompt=prompt, max_tokens=50)
    assert isinstance(output, str), "generate() should return a string."
    assert len(output.strip()) > 0, "Generated text should not be empty."


def test_count_tokens(openai_provider):
    """
    (Optional) If you've added a count_tokens method or something similar.
    Check that it returns an integer > 0 for a non-empty string.
    """
    if not hasattr(openai_provider, "count_tokens"):
        pytest.skip("No count_tokens method in OpenAIProvider. Skipping test.")

    text = "This is a test prompt."
    token_count = openai_provider.count_tokens(text)
    assert isinstance(token_count, int), "count_tokens() should return an integer."
    assert token_count > 0, "Token count should be greater than zero."

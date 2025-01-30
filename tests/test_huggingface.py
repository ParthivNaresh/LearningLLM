import pytest

from LearningLLM.providers import HuggingFaceProvider


@pytest.fixture(scope="module")
def hf_provider():
    """
    Pytest fixture to instantiate the provider once for all tests.
    Note: If you need a different device or token, customize here.
    """
    provider = HuggingFaceProvider()
    return provider


def test_list_models(hf_provider):
    """
    Verify that list_models returns a list of model IDs (strings).
    """
    model_ids = hf_provider.list_models()
    assert isinstance(model_ids, list), "list_models() should return a list."
    print(model_ids)
    if len(model_ids) > 0:
        assert isinstance(model_ids[0], str), "Each model ID should be a string."


def test_set_model(hf_provider):
    """
    Test setting a small, public model to ensure it loads correctly.
    """
    model_name = "gpt2"
    hf_provider.set_model(model_name)
    assert hf_provider.model_name == model_name, "Model name should be set."
    assert hf_provider.model is not None, "Model should be loaded."
    assert hf_provider.tokenizer is not None, "Tokenizer should be loaded."


def test_generate(hf_provider):
    """
    Verify text generation produces a non-empty string.
    """
    model_name = "gpt2"
    hf_provider.set_model(model_name)
    prompt = "Hello, how are you?"
    output = hf_provider.generate(prompt=prompt, max_new_tokens=10)
    assert isinstance(output, str), "generate() should return a string."
    assert len(output) > 0, "Generated text should not be empty."

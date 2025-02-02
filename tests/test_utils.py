import pytest

from utils import PROVIDER_MAP, load_chat_provider


@pytest.mark.parametrize("provider_key", PROVIDER_MAP.keys())
def test_load_chat_provider(provider_key):
    provider_class = load_chat_provider(provider_key)
    print(provider_class)
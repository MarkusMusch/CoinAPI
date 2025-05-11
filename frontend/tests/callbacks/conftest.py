import pytest
from unittest.mock import patch

from backend.models.models_orm import Symbol


@pytest.fixture
def mock_symbol():
    return Symbol.BTCUSDT


@pytest.fixture
def mock_data():
    return {"active_carousel": 0}


@pytest.fixture
def mock_generate_graph():
    with patch('frontend.src.callbacks.load_carousel_callback.generate_graph') as mock_graph:
        yield mock_graph


@pytest.fixture
def mock_load_data_cumulative_funding():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_cumulative_funding') as mock_load:
        yield mock_load


@pytest.fixture
def mock_load_data_funding_rates():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_funding_rates') as mock_load:
        yield mock_load


@pytest.fixture
def mock_load_data_cumulative_funding_leveraged():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_cumulative_funding_leveraged') as mock_load:
        yield mock_load


@pytest.fixture
def mock_load_data_funding_rates_leveraged():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_funding_rates_leveraged') as mock_load:
        yield mock_load


@pytest.fixture
def mock_load_data_net_income_leveraged():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_net_income_leveraged') as mock_load:
        yield mock_load
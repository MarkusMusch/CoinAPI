import pytest
from unittest.mock import MagicMock, patch
from backend.data_access.api_client.bybit_client import ByBitClient
from backend.models.models_api import FundingRequest, OpenInterestRequest

# Define constants for mocking
MOCK_API_KEY = "test_api_key"
MOCK_API_SECRET = "test_api_secret"
MOCK_BASE_ENDPOINT = "https://api.bybit.com"
MOCK_ENDPOINT_FUNDING = "/funding"
MOCK_ENDPOINT_OPEN_INTEREST = "/open_interest"
MOCK_ENDPOINT_INTEREST = "/interest_rate"


@pytest.fixture
def mock_client():
    with patch('backend.data_access.api_client.bybit_client.backend_settings') as mock_settings:
        mock_settings.BYBIT_API_KEY = MOCK_API_KEY
        mock_settings.BYBIT_API_SECRET = MOCK_API_SECRET
        mock_settings.BASE_ENDPOINT_BYBIT = MOCK_BASE_ENDPOINT
        mock_settings.ENDPOINT_FUNDING_BYBIT = MOCK_ENDPOINT_FUNDING
        mock_settings.ENDPOINT_OPEN_INTEREST_BYBIT = MOCK_ENDPOINT_OPEN_INTEREST
        mock_settings.ENDPOINT_INTNEREST_BYBIT = MOCK_ENDPOINT_INTEREST
        yield ByBitClient()


@pytest.fixture
def mock_requests_get():
    with patch('backend.data_access.api_client.bybit_client.requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_time():
    with patch('backend.data_access.api_client.bybit_client.time.time') as mock_time_func:
        mock_time_func.return_value = 1700000000.0  # Fixed timestamp
        yield mock_time_func


@pytest.fixture
def mock_hmac():
    with patch('backend.data_access.api_client.bybit_client.hmac.new') as mock_hmac:
        yield mock_hmac


@pytest.fixture
def mock_hashlib():
    with patch('backend.data_access.api_client.bybit_client.hashlib.sha256') as mock_hashlib:
        yield mock_hashlib


@pytest.fixture
def mock_funding_history_response():
    with patch('backend.data_access.api_client.bybit_client.FundingHistoryResponse') as mock_response:
        yield mock_response


@pytest.fixture
def mock_open_interest_response():
    with patch('backend.data_access.api_client.bybit_client.OpenInterestResponse') as mock_response:
        yield mock_response


@pytest.fixture
def mock_interest_rate_response():
    with patch('backend.data_access.api_client.bybit_client.InterestRateResponse') as mock_response:
        yield mock_response


class TestByBitClient:
    def test_init(self, mock_client):
        assert mock_client.api_key == MOCK_API_KEY
        assert mock_client.api_secret == MOCK_API_SECRET
        assert mock_client.base_endpoint == MOCK_BASE_ENDPOINT
        assert mock_client.endpoint_funding == MOCK_ENDPOINT_FUNDING
        assert mock_client.endpoint_open_interest == MOCK_ENDPOINT_OPEN_INTEREST

    def test_sign_request(self, mock_client, mock_hmac, mock_hashlib):
        mock_hmac_instance = MagicMock()
        mock_hmac_instance.hexdigest.return_value = MagicMock()
        mock_hmac.return_value = mock_hmac_instance

        params = {'b': '2', 'a': '1'}
        signature = mock_client._sign_request(params)

        expected_param_str = "a=1&b=2"
        mock_hmac.assert_called_once_with(
            MOCK_API_SECRET.encode('utf-8'),
            expected_param_str.encode('utf-8'),
            mock_hashlib
        )
        mock_hmac.return_value.hexdigest.assert_called_once()
        assert signature == mock_hmac_instance.hexdigest.return_value

    def test_sign_request_exception(self, mock_client):
        mock_client.api_secret = None
        params = {'b': '2', 'a': '1'}
        with pytest.raises(Exception) as exc_info:
            mock_client._sign_request(params)
        assert "'NoneType' object has no attribute 'encode'" in str(exc_info.value)

    def test_get_funding_history_empty_list(self, mock_client, mock_requests_get, mock_funding_history_response):
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': {'category': 'test_category', 'list': []}}
        mock_requests_get.return_value = mock_response

        result = mock_client.get_funding_history(FundingRequest(category="test_category", symbol="BTCUSD", endTime=1700000000000))

        expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_FUNDING
        expected_params = {"category": "test_category", "symbol": "BTCUSD", "endTime": 1700000000000}
        mock_requests_get.assert_called_once_with(expected_url, params=expected_params)
        mock_funding_history_response.assert_called_once_with(category="test_category", list=[])
        assert result == mock_funding_history_response.return_value

    def test_get_funding_history_with_data(self, mock_client, mock_requests_get, mock_funding_history_response):
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': {'category': 'test_category', 'list': ['data1', 'data2']}}
        mock_requests_get.return_value = mock_response
        mock_funding_history_response.return_value = "FundingHistoryResponseInstance"

        result = mock_client.get_funding_history(FundingRequest(category="test_category", symbol="ETHUSD", endTime=1700000000000))

        expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_FUNDING
        expected_params = {"category": "test_category", "symbol": "ETHUSD", "endTime": 1700000000000}
        mock_requests_get.assert_called_once_with(expected_url, params=expected_params)
        mock_funding_history_response.assert_called_once_with(category="test_category", list=['data1', 'data2'])
        assert result == "FundingHistoryResponseInstance"

    def test_get_funding_rate_exceptions(self, mock_client):
        with patch('backend.data_access.api_client.bybit_client.RequestException') as mock_request_exception:
            mock_request_exception.side_effect = Exception("Test Error")
            with pytest.raises(Exception) as exc_info:
                mock_client.get_funding_history(FundingRequest(category="test_category", symbol="ETHUSD", endTime=1700000000000))
            assert 'catching classes that do not inherit from BaseException is not allowed' in str(exc_info.value)

    def test_get_open_interest_empty_list(self, mock_client, mock_requests_get, mock_open_interest_response):
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': {'category': 'test_category', 'list': []}}
        mock_requests_get.return_value = mock_response

        result = mock_client.get_open_interest(OpenInterestRequest(category="test_category", symbol="BTCUSD", intervalTime="1h", endTime=1700000000000))

        expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_OPEN_INTEREST
        expected_params = {"category": "test_category", "symbol": "BTCUSD", "intervalTime": "1h", "endTime": 1700000000000}
        mock_requests_get.assert_called_once_with(expected_url, params=expected_params)
        mock_open_interest_response.assert_called_once_with(category="test_category", list=[])
        assert result == mock_open_interest_response.return_value

    def test_get_open_interest_with_data(self, mock_client, mock_requests_get, mock_open_interest_response):
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': {'category': 'test_category', 'list': ['data1', 'data2']}}
        mock_requests_get.return_value = mock_response
        mock_open_interest_response.return_value = "OpenInterestResponseInstance"

        result = mock_client.get_open_interest(OpenInterestRequest(category="test_category", symbol="ETHUSD", intervalTime="1h", endTime=1700000000000))

        expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_OPEN_INTEREST
        expected_params = {"category": "test_category", "symbol": "ETHUSD", "intervalTime": "1h", "endTime": 1700000000000}
        mock_requests_get.assert_called_once_with(expected_url, params=expected_params)
        mock_open_interest_response.assert_called_once_with(category="test_category", list=['data1', 'data2'])
        assert result == "OpenInterestResponseInstance"

    def test_get_open_interest_exceptions(self, mock_client):
        with patch('backend.data_access.api_client.bybit_client.RequestException') as mock_request_exception:
            mock_request_exception.side_effect = Exception("Test Error")
            with pytest.raises(Exception) as exc_info:
                mock_client.get_open_interest(OpenInterestRequest(category="test_category", symbol="ETHUSD", intervalTime="1h", endTime=1700000000000))
            assert 'catching classes that do not inherit from BaseException is not allowed' in str(exc_info.value)

    def test_get_interest_rate_with_empty_result(self, mock_client, mock_requests_get, mock_time, mock_interest_rate_response):
        with patch.object(mock_client, '_sign_request', return_value=MagicMock()) as mock_sign:
            mock_response = MagicMock()
            mock_response.json.return_value = {'result': '{}'}
            mock_requests_get.return_value = mock_response

            result = mock_client.get_interest_rate("BTC", 1700000000000)

            expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_INTEREST
            expected_params = {
                "api_key": MOCK_API_KEY,
                "timestamp": 1700000000000,
                "currency": "BTC",
                "startTime": 1700000000000 - 30*24*60*60*1000,
                "endTime": 1700000000000,
                "sign": mock_sign.return_value
            }
            mock_requests_get.assert_called_once_with(expected_url, params=expected_params)
            mock_interest_rate_response.assert_called_once_with(list=[])
            assert result == mock_interest_rate_response.return_value

    def test_get_interest_rate_with_data(self, mock_client, mock_requests_get, mock_time, mock_interest_rate_response):
        with patch.object(mock_client, '_sign_request', return_value=MagicMock()) as mock_sign:
            mock_response = MagicMock()
            mock_response.json.return_value = {'result': {'data': 'some_data'}}
            mock_requests_get.return_value = mock_response
            mock_interest_rate_response.return_value = "InterestRateResponseInstance"

            result = mock_client.get_interest_rate("ETH", 1700000000000)

            expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_INTEREST
            expected_params = {
                "api_key": MOCK_API_KEY,
                "timestamp": 1700000000000,
                "currency": "ETH",
                "startTime": 1700000000000 - 30*24*60*60*1000,
                "endTime": 1700000000000,
                "sign": mock_sign.return_value
            }
            mock_requests_get.assert_called_once_with(expected_url, params=expected_params)
            mock_interest_rate_response.assert_called_once_with(**{'data': 'some_data'})
            assert result == "InterestRateResponseInstance"

    def test_get_interest_rate_exceptions(self, mock_client):
        with patch.object(mock_client, '_sign_request', side_effect=Exception("Test Error")) as mock_sign:
            with pytest.raises(Exception) as exc_info:
                mock_client.get_interest_rate("ETH", 1700000000000)
            assert "Test Error" in str(exc_info.value)

        with patch('backend.data_access.api_client.bybit_client.RequestException') as mock_request_exception:
            mock_request_exception.side_effect = Exception("Test Error")
            with pytest.raises(Exception) as exc_info:
                mock_client.get_interest_rate("ETH", 1700000000000)
            assert 'catching classes that do not inherit from BaseException is not allowed' in str(exc_info.value)
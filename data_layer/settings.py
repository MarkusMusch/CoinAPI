from pydantic_settings import BaseSettings


class BackendSettings(BaseSettings):

    # Bybit API
    BYBIT_API_KEY: str
    BYBIT_API_SECRET: str

    # API Endpoints
    BASE_ENDPOINT_BYBIT: str = 'https://api.bybit.com'
    ENDPOINT_FUNDING_BYBIT: str = '/v5/market/funding/history'
    ENDPOINT_OPEN_INTEREST_BYBIT: str = '/v5/market/open-interest'
    ENDPOINT_INTNEREST_BYBIT: str = '/v5/spot-margin-trade/interest-rate-history'

    class Config:
        case_sensitive = True
        env_file = '.env'


backend_settings = BackendSettings()
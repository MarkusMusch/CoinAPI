from pydantic_settings import BaseSettings


class FrontendSettings(BaseSettings):
    DEBUG_MODE: bool = False
    PORT: int = 8049
    HOST: str = "0.0.0.0"

    class Config:
        case_sensitive = True


frontend_settings = FrontendSettings()
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_user: str
    secret_key: str
    algorithm: str
    access_key_expiry: int


    model_config= SettingsConfigDict(env_file='.env')

settings=Settings()
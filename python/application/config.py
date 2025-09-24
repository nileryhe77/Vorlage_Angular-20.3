from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Basis
    port: int
    reload: bool = True
    client_origin_url: str = "http://localhost:4040"

    # Keycloak
    keycloak_url: str | None = None
    keycloak_realm: str | None = None
    keycloak_client_id: str | None = None

    # Datenbank
    postgres_host: str | None = None
    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None

    # Basepath
    basepath: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

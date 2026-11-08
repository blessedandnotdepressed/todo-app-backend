from dataclasses import dataclass

@dataclass(frozen = True)
class Settings:
    database_url: str
    cors_origins: list[str]

def get_settings() -> Settings:
    return Settings(database__url='postgresql+psycopg2://postgres:postgres@localhost:15432/postgres',
        cors_origins=["http://localhost:3000"])



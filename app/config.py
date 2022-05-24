from pydantic import BaseSettings

# define envrionment variables and these are case insensitive. This is to validate all our env vars. If default not 
# given and env variable not set then it will validate that
# class Settings(BaseSettings): 
#     database_password: str = "localhost"   # not mandatory to give default values
#     database_username: str = "postgres"
#     secret_key: str = "234ui2340892348"

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
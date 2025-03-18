from dotenv import load_dotenv, find_dotenv
import os

from pydantic_settings import BaseSettings

# Load .env
current_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_dir)

dotenv_path = find_dotenv(".env")
load_dotenv(dotenv_path)


class Settings(BaseSettings): 
    SECRET_KEY: str 
    ALGORITHM: str 

    MONGO_DB_HOST: str

    CACHED_UUIDS_KEY: str

    UPDATE_DB_TOPIC: str
    UPDATE_CACHE_TOPIC: str

    USERNAME: str
    PASSWORD: str

    @property 
    def MONGO_DB_URL(self): 
        return f"mongodb://{self.MONGO_DB_HOST}/" 
    
    class ConfigDict: 
        env_file = dotenv_path


settings = Settings()

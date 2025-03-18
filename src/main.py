from fastapi import FastAPI

from src.api import api_router
from src.logging import configure_logging


def create_app() -> FastAPI: 
    app = FastAPI() 
    return app 


app = create_app()

# configure the logging format
configure_logging()

# add all API routers
app.include_router(api_router)

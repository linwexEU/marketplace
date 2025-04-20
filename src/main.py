from fastapi import FastAPI

from api import api_router
from logger import configure_logging


def create_app() -> FastAPI: 
    app = FastAPI() 
    return app 


app = create_app()

# configure the logging format
configure_logging()

# add all API routers
app.include_router(api_router)

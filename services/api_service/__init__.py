
from fastapi import Depends, FastAPI
import uvicorn

from ..abstract_service import AbstractService
from .dependencies import get_query_token
from . import api


class ApiService(AbstractService):

    def __init__(self, config):
        super().__init__()

        self.app = FastAPI(dependencies=[
            #Depends(get_query_token)
        ])
        self.app.include_router(api.router)
        self.app.state.config = config

    def run(self):
        uvicorn.run(self.app, **vars(self.app.state.config.uvicorn))

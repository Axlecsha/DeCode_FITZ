
from typing import Annotated
from fastapi import Header, Request, HTTPException

async def get_query_token(request: Request, x_token: Annotated[str, Header()]):
    if x_token != request.app.state.config.access_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")

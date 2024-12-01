import types

# https://www.uvicorn.org/settings/
api_service = types.SimpleNamespace()
api_service.uvicorn = types.SimpleNamespace()
api_service.uvicorn.host: str = "0.0.0.0"
api_service.uvicorn.port: int = 8000
api_service.uvicorn.ws_max_queue: int = 32
api_service.uvicorn.ws_ping_interval: float | None = 20.0
api_service.uvicorn.ws_ping_timeout: float | None = 20.0
api_service.uvicorn.workers: int | None = None
api_service.uvicorn.limit_concurrency: int | None = None
api_service.uvicorn.limit_max_requests: int | None = None
api_service.uvicorn.timeout_keep_alive: int = 5
api_service.uvicorn.timeout_graceful_shutdown: int | None = None
api_service.uvicorn.use_colors: bool | None = True
api_service.uvicorn.app_dir: str | None = None
api_service.access_token: str | None = '5435554213:QWEeW4nfhDSqFDSFDSbFLbsHJdufHJwe26r'



telegram = types.SimpleNamespace()
telegram.token = '7825338414:AAFtW9zXzwfiUCR_2V49609XnlqQtrNCtJA'










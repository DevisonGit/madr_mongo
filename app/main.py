from fastapi import FastAPI

from app.api.v1.routers import router as router_v1

app = FastAPI()


app.include_router(router_v1, prefix='/api/v1')

from fastapi import FastAPI

from database import seed_if_empty
from routes import router

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    seed_if_empty()


app.include_router(router)

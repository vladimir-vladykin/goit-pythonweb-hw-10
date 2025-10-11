from fastapi import FastAPI
from src.api import contacts

app = FastAPI()
app.include_router(contacts.router, prefix="/api")


def run():
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run()

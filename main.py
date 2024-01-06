import uvicorn
from fastapi import FastAPI

from files.api import file_api

if __name__ == "__main__":
    app = FastAPI()
    app.include_router(file_api, prefix="/files")
    uvicorn.run(app, host="0.0.0.0", port=11109)

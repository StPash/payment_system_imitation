from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api import api_router

app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

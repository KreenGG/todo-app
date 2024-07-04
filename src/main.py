import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .api.v1 import router as v1_router
from .api.v1.schemas import PingResponse

app = FastAPI(
    title="ToDo App",
    debug=True,
    root_path="/api",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/api/docs")


@app.get("/ping")
def ping() -> PingResponse:
    return {"result": True}


app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run(app, reload=True)

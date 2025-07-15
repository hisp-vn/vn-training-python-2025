from fastapi import APIRouter, FastAPI

statusRouter = APIRouter()


@statusRouter.get("")
async def status():
    return {"status": "ok"}


app = FastAPI()
app.include_router(statusRouter, prefix="/api/status")


@app.get("/")
async def index():
    return {"message": "Hello, World!"}

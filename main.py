from fastapi import FastAPI, Depends
from routes import auth
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup():
    cache = redis.from_url('redis://18.118.226.162', port=6379, db=0)
    await FastAPILimiter.init(cache)

app.include_router(auth.auth_router, tags=["Autenticar usuario"], prefix="/auth",
dependencies=[Depends(RateLimiter(times=10, seconds=1))])



@app.get("/")
async def root():
    return {"message": "Hello World"}
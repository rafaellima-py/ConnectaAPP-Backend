from fastapi import FastAPI, Depends
from routes import auth, infos, funcs
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
    cache = redis.from_url('redis://18.118.226.162:6379/0', encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(cache)

app.include_router(auth.auth_router, tags=["Autenticar usuario"], prefix="/auth")
app.include_router(infos.info_router, tags=["Informações do usuario"], prefix="/info")
app.include_router(funcs.functions_router, tags=["Funções do usuario"], prefix="/funcs")

@app.get("/")
async def root():
    return {"message": "Hello World"}
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from scheema import *
from database import Database
from fastapi.security import OAuth2PasswordBearer
from security import *
from docs.info_docs import *
import base64
db = Database()
info_router = APIRouter()


@info_router.get("/get_user_info", responses=info_user_basic_response)
async def get_user_info(token: str = Depends(get_current_user)):
    user = await db.get_user(token)  # usando username

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user["_id"] = str(user["_id"])

    for item in user.get("contracts_info", []):
        if "contrato" in item:
            item["contrato"] = base64.b64encode(item["contrato"]).decode("utf-8")
        if "assinatura" in item:
            item["assinatura"] = base64.b64encode(item["assinatura"]).decode("utf-8")

    return JSONResponse(content=jsonable_encoder({
        "success": True,
        "detail": "Usuário encontrado com sucesso",
        "user_info": user
    }))
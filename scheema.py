from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Union
from enum import Enum
from validate_docbr import CPF  

class UserLogin(BaseModel):
    email: Union[EmailStr, str]
    password: str
    

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    cliente = "cliente"


class UserRegister(BaseModel):
    email: Union[EmailStr, str]
    username: str 
    password: str
    name: str
    last_name: str
    phone: Optional[str]
    cep: str
    cpf: str  # adicionamos o campo CPF
    cargo : Optional[str]
    rg : Optional[str]
    role: UserRole
    


    @validator("email")
    def validate_email(cls, v):
        try:
            _ = EmailStr.validate(v)
        except ValueError:
            pass  # se não for um email válido, apenas aceita como string
        return v

    @validator("cpf")
    def validate_cpf(cls, v):
        cpf_validator = CPF()
        if not cpf_validator.validate(v):
            raise ValueError("CPF inválido")
        return v
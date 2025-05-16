from pydantic import BaseModel, EmailStr, validator, TypeAdapter
from typing import Optional, Union
from enum import Enum
from validate_docbr import CPF, CNPJ

class UserLogin(BaseModel):
    email: Union[EmailStr, str]
    password: str
    

class UserRole(str, Enum):
    admin = "admin"
    user = "funcionario"
    cliente = "cliente"


class UserRegister(BaseModel):
    email: Union[EmailStr, str]
    username: str 
    password: str
    name: str
    last_name: str
    phone: Optional[str]
    cep: str
    cpf: str
    cargo: Optional[str]
    rg: Optional[str]
    role: UserRole
    rua: Optional[str]
    numero: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    valor: Optional[float] = 0.0
    servicos: Optional[list]
    projetos: Optional[list] 
    primeiro_login: Optional[bool] = True

    
    @validator("cpf")
    def validate_cpf(cls, v):
        cpf_validator = CPF()
        cnpj_validator = CNPJ()
        if not cpf_validator.validate(v) and not cnpj_validator.validate(v):
            raise ValueError("CPF ou CNPJ inválido")
        return v
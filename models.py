from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Union
from validate_docbr import CPF  

class UserLogin(BaseModel):
    email: Union[EmailStr, str]
    password: str
    


class UserRegister(BaseModel):
    email: Union[EmailStr, str]
    password: str
    name: str
    last_name: str
    phone: Optional[str]
    cep: str
    cpf: str  # adicionamos o campo CPF
    birth_date: str

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
auth_login_response = {
    200: {
        "description": "Login realizado com sucesso",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "detail": "Login realizado",
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "Bearer"
                }
            }
        }
    },
    401: {
        "description": "Usuário ou senha inválidos",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "detail": "Usuário ou senha inválidos"
                }
            }
        }
    },
    404: {
        "description": "Usuário não encontrado",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "detail": "Usuário não encontrado"
                }
            }
        }
    }
}

register_response = {
    200: {
        "description": "Usuário cadastrado com sucesso",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "detail": "Usuário cadastrado com sucesso"
                }
            }
        }       
},
    400: {
        "description": "Usuário já existe",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "detail": "Usuário já existe"
                }
            }
        }
    },
    
    401: {
        "description": "Token inválido ou não autorizado",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "detail": "Token inválido ou não autorizado"
                }
            }
        }
    }
}
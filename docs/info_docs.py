info_user_basic_response = {
    200: {
        "description": "Usuário encontrado com sucesso",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "detail": "Usuário encontrado com sucesso",
                    "user_info": {
                        "username": "rafaellima",
                        "role": "funcionario",
                        "nome": "Rafael Lima",
                        "lastName": "Lima",
                        "cpf": "123.456.789-00",
                        "phone": "(11) 99999-9999",
                        "cargo": "Funcionário",
                        "email": "rafaellima@gmail.com",
                        "cep": "12345678",
                        "rg": "12345678",
                        "rua": "Rua Teste",
                        "numero": "123",
                        "bairro": "Bairro Teste",
                        "cidade": "Cidade Teste",
                        "estado": "Estado Teste",
                        "projetos": [
                            {
                                "nome": "Projeto Teste",
                                "descricao": "Descrição do projeto",
                                "valor": 1000.0,
                                "periodo": "2021-01-01",
                                "status": "ativo"
                            }
                        ],
                        "servicos": [
                            {
                                "nome": "Serviço Teste",
                                "descricao": "Descrição do serviço",
                                "valor": 1000.0,
                                "periodo": "2021-01-01",
                                "status": "ativo"
                            }
                        ],
                        "periodo": "2021-01-01"
                    }
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
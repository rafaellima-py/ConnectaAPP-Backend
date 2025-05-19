import httpx

# Caminhos locais dos arquivos
pdf_path = "contrato_exemplo.pdf"
png_path = "assinatura_exemplo.png"

# Token JWT de autenticação
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3Nzg3MTU2MzV9.PqUTUb2NIfHRMdjXgBQHZjRgUhK6jFMAuTaxXfC7hPE"  # substitua pelo token real

# URL da sua API
url = "http://localhost:8000/funcs/send_contract"

# Abre os arquivos e envia como multipart/form-data
with open(pdf_path, "rb") as pdf_file, open(png_path, "rb") as png_file:
    files = [
        ("files", ("contrato_exemplo.pdf", pdf_file, "application/pdf")),
        ("files", ("assinatura_exemplo.png", png_file, "image/png")),
    ]

    headers = {
        "Authorization": token
    }

    response = httpx.post(url, files=files, headers=headers)

# Resultado
print("Status:", response.status_code)
print("Resposta:", response.text)

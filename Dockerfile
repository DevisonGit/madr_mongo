FROM python:3.13-slim
LABEL authors="devisono"

# Evita .pyc e buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia arquivos de dependência
COPY pyproject.toml uv.lock ./

# Instala uv
RUN pip install --no-cache-dir uv

# Instala dependências
RUN uv sync --frozen

# Copia o restante do código
COPY . .

CMD uv run uvicorn --host 0.0.0.0 app.main:app
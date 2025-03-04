FROM python:3.11-slim AS base

FROM base AS build
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt


FROM base AS production


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    mariadb-client && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --system user && \
   adduser --system --ingroup user user

COPY --from=build /opt/venv /opt/venv

WORKDIR /app

COPY . .

RUN chown -R user:user /app

RUN chmod +x /app/script/docker-entrypoint.sh

USER user

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

CMD ["/bin/bash", "/app/script/docker-entrypoint.sh"]

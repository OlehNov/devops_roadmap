FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    default-libmysqlclient-dev \
    wget \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -C /usr/local/bin --strip-components=1 -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz

RUN python -m venv /opt/venv
ENV PATH='/opt/venv/bin:$PATH'

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

# CMD ["dockerize", "-wait", "tcp://db:3306", "-timeout", "90s", "bash", "-c", "python src/manage.py makemigrations && python src/manage.py migrate && python src/manage.py runserver 0.0.0.0:8000"]
#CMD ["dockerize", "-wait", "tcp://db:3306", "-timeout", "90s", "bash", "-c", "python src/manage.py runserver 0.0.0.0:8000"]
CMD ["bash", "-c", "python src/manage.py runserver 0.0.0.0:8000"]

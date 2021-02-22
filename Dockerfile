FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV DEPENDENCY_VERSION=v0.1

ADD requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev 
    
RUN python3.7 -m pip install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/pip

ENV CODE_VERSION=v0.5

COPY ./app /app/app
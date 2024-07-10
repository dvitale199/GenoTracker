FROM python:3.11
LABEL maintainer="Dan Vitale <dan@datatecnica.com>"

RUN apt-get update -y && \
    apt-get install python3-dev -y && \
    apt-get install libevent-dev

RUN adduser --disabled-password --gecos "" gtuser

WORKDIR /backend
    
COPY . /backend

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["uvicorn", "fastapi_service.main:app", "--host", "0.0.0.0", "--port", "8080"]
FROM python:3.11
LABEL maintainer="Dan Vitale <dan@datatecnica.com>"

RUN apt-get update -y && \
    apt-get install python3-dev -y && \
    apt-get install libevent-dev

RUN adduser --disabled-password --gecos "" gtuser

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*
    
# Copy the application code to /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt \
    pip install --no-cache-dir .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
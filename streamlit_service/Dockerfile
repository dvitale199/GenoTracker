FROM python:3.11

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*
    
# Copy the application code to /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_service/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableWebsocketCompression=false", "--server.enableXsrfProtection=false", "--server.headless=true"]

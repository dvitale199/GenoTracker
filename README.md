# GenoTracker

GenoTracker is a FastAPI and Streamlit-based application for managing and visualizing genomic cohort data. The backend service is implemented using FastAPI, and the frontend is created with Streamlit. The application can read cohort data from both local CSV files and Google Cloud Storage (GCS).

## Features

- Load and visualize genomic cohort data.
- Supports reading data from local files and GCS.
- Interactive data exploration using Streamlit.
- Dockerized for easy deployment and scalability.
- Supports secure configuration using Docker secrets.

## Project Structure
```
genotracker/
│
├── genotracker/
│   ├── __init__.py
│   ├── api/
│   │   └── endpoints.py
│   ├── models/
│   │   └── cohort_data.py
│   ├── services/
│   │   └── data_service.py
│   │
│   ├── tests/
│   ├── __init__.py
│   ├── test_data_service.py
│   └── test_main.py
├── Dockerfile.fastapi
├── Dockerfile.streamlit
├── docker-compose.yml
├── pyproject.toml
└── README.md
```
## Getting Started

### Prerequisites

- Python 3.11+
- Docker
- Docker Compose
- Google Cloud SDK (for accessing GCS)

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/dvitale199/genotracker.git
    cd genotracker
    ```

2. **Install dependencies**:

    Using Poetry:

    ```bash
    poetry install
    ```

    Or using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up Google Cloud credentials**:

    Ensure you have a service account JSON key and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
    ```

### Running Locally

**Using Docker Compose**

1. **Build and start the services**:

    ```bash
    docker-compose up --build
    ```

2. **Access the services**:

    - FastAPI: [http://localhost:8000](http://localhost:8000)
    - Streamlit: [http://localhost:8501](http://localhost:8501)

### Running Tests

1. **Run tests using pytest**:

    ```bash
    pytest
    ```

### Configuration

#### Environment Variables

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to the Google Cloud service account JSON key.

#### Docker Secrets

For secure handling of sensitive information, Docker secrets are used. Ensure your `docker-compose.yml` is set up correctly to use the secret:

```yaml
secrets:
  gcloud-service-account:
    file: ./secrets/gp2-release-terra-e65c1b67820b.json
```
### Deploying to Google Cloud Run

1. **Build the Docker images**:

    ```bash
    docker build -t gcr.io/your-project-id/genotracker-fastapi -f Dockerfile.fastapi .
    docker build -t gcr.io/your-project-id/genotracker-streamlit -f Dockerfile.streamlit .
    ```

2. **Push the images to Google Container Registry**:

    ```bash
    docker push gcr.io/your-project-id/genotracker-fastapi
    docker push gcr.io/your-project-id/genotracker-streamlit
    ```

3. **Deploy the services to Cloud Run**:

    ```bash
    gcloud run deploy genotracker-fastapi --image gcr.io/your-project-id/genotracker-fastapi --platform managed --region your-region --service-account your-service-account@your-project-id.iam.gserviceaccount.com

    gcloud run deploy genotracker-streamlit --image gcr.io/your-project-id/genotracker-streamlit --platform managed --region your-region --service-account your-service-account@your-project-id.iam.gserviceaccount.com
    ```


### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [wait-for-it](https://github.com/vishnubob/wait-for-it/tree/master)
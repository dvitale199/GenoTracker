from fastapi import APIRouter, HTTPException, Depends, status
from genotracker.services.data_service import load_cohort_data_from_csv
from genotracker.models.data_models import CohortDataSchema
from fastapi.security.api_key import APIKeyHeader
from typing import List
import logging
from google.cloud import secretmanager

logger = logging.getLogger(__name__)

router = APIRouter()

def access_secret_version():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/776926281950/secrets/genotracker-api-key/versions/1"
    response = client.access_secret_version(name=secret_name)
    return response.payload.data.decode("UTF-8")

# Retrieve the API key from Secret Manager
API_KEY = access_secret_version()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key

@router.get("/")
async def root():
    return "Welcome to GenoTracker"

@router.get("/data", response_model=List[CohortDataSchema])
def get_cohort_data(
    from_gcs: bool = True, 
    api_key: str = Depends(get_api_key)
):
    try:
        if from_gcs:
            bucket_name = "genotracker"
            file_path = "data/genotracker_clean.csv"
            cohort_data = load_cohort_data_from_csv(file_path, from_gcs=True, bucket_name=bucket_name)
        else:
            file_path = "data/genotracker_clean.csv"
            cohort_data = load_cohort_data_from_csv(file_path)
        return cohort_data
    except Exception as e:
        logger.error(f"Error loading cohort data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
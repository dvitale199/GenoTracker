from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from genotracker.services.data_service import load_cohort_data_from_csv
from genotracker.models.data_models import CohortDataSchema
from typing import List
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )

router = APIRouter()

@router.get("/")
async def root():
    return "Welcome to GenoTracker"

@router.get("/data", response_model=List[CohortDataSchema])
def get_cohort_data(api_key: APIKey = Depends(get_api_key)):
    try:
        bucket_name = "genotracker"
        file_path = "data/genotracker_clean.csv"
        cohort_data = load_cohort_data_from_csv(file_path, from_gcs=True, bucket_name=bucket_name)
        return cohort_data
    
    except Exception as e:
        logger.error(f"Error loading cohort data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
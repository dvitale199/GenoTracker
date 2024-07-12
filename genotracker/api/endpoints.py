from fastapi import APIRouter, HTTPException
from genotracker.services.data_service import load_cohort_data_from_csv
from genotracker.models.data_models import CohortDataSchema
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def root():
    return "Welcome to GenoTracker"

@router.get("/data", response_model=List[CohortDataSchema])
def get_cohort_data(from_gcs: bool = False):
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
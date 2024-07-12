from fastapi import APIRouter
from genotracker.services.data_service import load_cohort_data_from_csv
from genotracker.models.data_models import CohortDataSchema
from typing import List

router = APIRouter()

@router.get("/")
async def root():
    return "Welcome to GenoTracker"

@router.get("/data", response_model=List[CohortDataSchema])
def get_cohort_data():
    file_path = '/Users/vitaled2/Desktop/Projects/GenoTracker/data/genotracker_clean.csv'
    cohort_data = load_cohort_data_from_csv(file_path)
    return cohort_data
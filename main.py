from fastapi import FastAPI
from google.cloud import storage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import pandas as pd
from load_data import CohortData
app = FastAPI()

BUCKET_NAME = 'genotracker'
DB_FILE_NAME = 'database/test.db'
LOCAL_DB_FILE_PATH = '/tmp/test.db'

def download_db_file():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(DB_FILE_NAME)
    blob.download_to_filename(LOCAL_DB_FILE_PATH)

download_db_file()

DATABASE_URL = f"sqlite:///{LOCAL_DB_FILE_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/")
async def root():
    return "Welcome to GenoTracker"

class CohortDataSchema(BaseModel):
    study_code: Optional[str] = ''
    monogenic_complex_mixed: Optional[str] = ''
    city: Optional[str] = ''
    geographic_locality: Optional[str] = ''
    n_dna_samples_attempted: Optional[int] = 0
    total_qc_pass: Optional[int] = 0
    callrate_fails: Optional[int] = 0
    sex_fails: Optional[int] = 0
    het_fails: Optional[int] = 0
    duplicates: Optional[int] = 0
    genotyping_complete: Optional[bool] = False
    imputation_panel: Optional[str] = ''
    imputation_complete: Optional[bool] = False
    genotypes_shareable: Optional[bool] = False
    gdpr: Optional[bool] = False
    site: Optional[str] = ''
    afr_case: Optional[int] = 0
    afr_control: Optional[int] = 0
    afr_other: Optional[int] = 0
    aac_case: Optional[int] = 0
    aac_control: Optional[int] = 0
    aac_other: Optional[int] = 0
    aj_case: Optional[int] = 0
    aj_control: Optional[int] = 0
    aj_other: Optional[int] = 0
    eas_case: Optional[int] = 0
    eas_control: Optional[int] = 0
    eas_other: Optional[int] = 0
    eur_case: Optional[int] = 0
    eur_control: Optional[int] = 0
    eur_other: Optional[int] = 0
    fin_case: Optional[int] = 0
    fin_control: Optional[int] = 0
    fin_other: Optional[int] = 0
    amr_case: Optional[int] = 0
    amr_control: Optional[int] = 0
    amr_other: Optional[int] = 0
    sas_case: Optional[int] = 0
    sas_control: Optional[int] = 0
    sas_other: Optional[int] = 0
    cas_case: Optional[int] = 0
    cas_control: Optional[int] = 0
    cas_other: Optional[int] = 0
    mde_case: Optional[int] = 0
    mde_control: Optional[int] = 0
    mde_other: Optional[int] = 0
    cah_case: Optional[int] = 0
    cah_control: Optional[int] = 0
    cah_other: Optional[int] = 0
    total: Optional[int] = 0
    new: Optional[bool] = True
    date_last_update: Optional[date] = Field(default_factory=date.today)

    class Config:
        orm_mode = True
        from_attributes = True

@app.get("/data", response_model=List[CohortDataSchema])
async def get_all_data():
    session = SessionLocal()
    try:
        data = session.query(CohortData).all()
        return [CohortDataSchema.model_validate(item) for item in data]
    finally:
        session.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
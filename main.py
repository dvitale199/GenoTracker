from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import os
import logging

app = FastAPI()

CSV_FILE_PATH = 'data/genotracker_clean.csv'

@app.get("/")
async def root():
    return "Welcome to GenoTracker"

data = []

class GeneticData(BaseModel):
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
    AFR: Optional[int] = 0
    AAC: Optional[int] = 0
    AJ: Optional[int] = 0
    EAS: Optional[int] = 0
    EUR: Optional[int] = 0
    FIN: Optional[int] = 0
    AMR: Optional[int] = 0
    SAS: Optional[int] = 0
    CAS: Optional[int] = 0
    MDE: Optional[int] = 0
    CAH: Optional[int] = 0
    total: Optional[int] = 0
    genotyping_complete: Optional[bool] = False
    imputation_panel: Optional[str] = ''
    imputation_complete: Optional[bool] = False
    genotypes_shareable: Optional[bool] = False
    gdpr: Optional[bool] = False
    site: Optional[str] = ''

def read_csv() -> pd.DataFrame:
    if os.path.exists(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    else:
        return pd.DataFrame(columns=[field for field in GeneticData.__annotations__])

@app.get("/data", response_model=List[GeneticData], operation_id="get_all_data")
def get_data():
    try:
        df = read_csv()
        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
        raise HTTPException(status_code=500, detail="Error reading data")

@app.get("/data/{study_code}", response_model=GeneticData, operation_id="get_data_by_study_code")
def get_data_by_study_code(study_code: str):
    try:
        df = read_csv()
        # Debugging print statements
        print(f"Available study codes: {df['study_code'].values}")
        print(f"Looking for study_code: '{study_code}'")
        if study_code in df['study_code'].values:
            record = df[df['study_code'] == study_code].to_dict(orient='records')[0]
            return record
        raise HTTPException(status_code=404, detail="Data not found")
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
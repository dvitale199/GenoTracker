from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
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
    study_code: str
    monogenic_complex_mixed: str
    city: str
    geographic_locality: str
    n_dna_samples_received_at_site: int
    n_dna_samples_attempted: int
    total_qc_pass: int
    callrate_fails: int
    sex_fails: int
    het_fails: int
    duplicates: int
    related: int
    AFR: int
    AAC: int
    AJ: int
    EAS: int
    EUR: int
    FIN: int
    AMR: int
    SAS: int
    CAS: int
    MDE: int
    CAH: int
    total: int
    genotyping_complete: bool
    imputation_panel: str
    imputation_complete: bool
    genotypes_shareable: bool
    gdpr: bool
    site: str

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
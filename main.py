from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from database import engine, CohortData
from datetime import date

app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to GenoTracker"

# Pydantic model for data serialization
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
    session = Session(engine)
    try:
        data = session.query(CohortData).all()
        return [CohortDataSchema.model_validate(item) for item in data]
    finally:
        session.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
# def read_csv() -> pd.DataFrame:
#     if os.path.exists(CSV_FILE_PATH):
#         return pd.read_csv(CSV_FILE_PATH)
#     else:
#         return pd.DataFrame(columns=[field for field in GeneticData.__annotations__])

# @app.get("/data", response_model=List[GeneticData], operation_id="get_all_data")
# def get_data():
#     try:
#         df = read_csv()
#         return df.to_dict(orient="records")
#     except Exception as e:
#         logging.error(f"Error reading CSV: {e}")
#         raise HTTPException(status_code=500, detail="Error reading data")

# @app.get("/data/{study_code}", response_model=GeneticData, operation_id="get_data_by_study_code")
# def get_data_by_study_code(study_code: str):
#     try:
#         df = read_csv()
#         # Debugging print statements
#         print(f"Available study codes: {df['study_code'].values}")
#         print(f"Looking for study_code: '{study_code}'")
#         if study_code in df['study_code'].values:
#             record = df[df['study_code'] == study_code].to_dict(orient='records')[0]
#             return record
#         raise HTTPException(status_code=404, detail="Data not found")
#     except Exception as e:
#         logging.error(f"Error processing request: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
import pandas as pd
from typing import List, Optional
from google.cloud import storage
import io
from genotracker.models.data_models import CohortDataSchema

def load_cohort_data_from_csv(file_path: str, from_gcs: Optional[bool] = False, bucket_name: Optional[str] = None) -> List[CohortDataSchema]:
    if from_gcs and bucket_name:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        data = blob.download_as_string()
        df = pd.read_csv(io.BytesIO(data))
    else:
        df = pd.read_csv(file_path)
    
    df.fillna({
        'study_code': '',
        'monogenic_complex_mixed': '',
        'city': '',
        'geographic_locality': '',
        'n_dna_samples_attempted': 0,
        'total_qc_pass': 0,
        'callrate_fails': 0,
        'sex_fails': 0,
        'het_fails': 0,
        'duplicates': 0,
        'genotyping_complete': False,
        'imputation_panel': '',
        'imputation_complete': False,
        'genotypes_shareable': False,
        'gdpr': False,
        'site': '',
        'afr_case': 0,
        'afr_control': 0,
        'afr_other': 0,
        'aac_case': 0,
        'aac_control': 0,
        'aac_other': 0,
        'aj_case': 0,
        'aj_control': 0,
        'aj_other': 0,
        'eas_case': 0,
        'eas_control': 0,
        'eas_other': 0,
        'eur_case': 0,
        'eur_control': 0,
        'eur_other': 0,
        'fin_case': 0,
        'fin_control': 0,
        'fin_other': 0,
        'amr_case': 0,
        'amr_control': 0,
        'amr_other': 0,
        'sas_case': 0,
        'sas_control': 0,
        'sas_other': 0,
        'cas_case': 0,
        'cas_control': 0,
        'cas_other': 0,
        'mde_case': 0,
        'mde_control': 0,
        'mde_other': 0,
        'cah_case': 0,
        'cah_control': 0,
        'cah_other': 0,
        'total': 0,
        'new': True,
        'date_last_update': pd.to_datetime('today').date(),
        'compliance': False
    }, inplace=True)
    
    return [CohortDataSchema(**row.to_dict()) for _, row in df.iterrows()]
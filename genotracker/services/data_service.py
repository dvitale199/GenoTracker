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
        'institution': '',
        'city': '',
        'location': '',
        'territory': '',
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
        'shared_to_amppd': False,
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
        'new': False,
        'date_last_update': pd.to_datetime('today').date(),
        'compliance': False
    }, inplace=True)

    df = df.astype({
        'study_code': 'str',
        'monogenic_complex_mixed': 'str',
        'institution': 'str',
        'city': 'str',
        'location': 'str',
        'territory': 'str',
        'n_dna_samples_attempted': 'int',
        'total_qc_pass': 'int',
        'callrate_fails': 'int',
        'sex_fails': 'int',
        'het_fails': 'int',
        'duplicates': 'int',
        'genotyping_complete': 'bool',
        'imputation_panel': 'str',
        'imputation_complete': 'bool',
        'genotypes_shareable': 'bool',
        'shared_to_amppd': 'bool',
        'gdpr': 'bool',
        'site': 'str',
        'afr_case': 'int',
        'afr_control': 'int',
        'afr_other': 'int',
        'aac_case': 'int',
        'aac_control': 'int',
        'aac_other': 'int',
        'aj_case': 'int',
        'aj_control': 'int',
        'aj_other': 'int',
        'eas_case': 'int',
        'eas_control': 'int',
        'eas_other': 'int',
        'eur_case': 'int',
        'eur_control': 'int',
        'eur_other': 'int',
        'fin_case': 'int',
        'fin_control': 'int',
        'fin_other': 'int',
        'amr_case': 'int',
        'amr_control': 'int',
        'amr_other': 'int',
        'sas_case': 'int',
        'sas_control': 'int',
        'sas_other': 'int',
        'cas_case': 'int',
        'cas_control': 'int',
        'cas_other': 'int',
        'mde_case': 'int',
        'mde_control': 'int',
        'mde_other': 'int',
        'cah_case': 'int',
        'cah_control': 'int',
        'cah_other': 'int',
        'total': 'int',
        'new': 'bool',
        'date_last_update': 'datetime64[ns]',
        'compliance': 'bool'
    })

    df['date_last_update'] = df['date_last_update'].dt.date
    
    return [CohortDataSchema(**row.to_dict()) for _, row in df.iterrows()]
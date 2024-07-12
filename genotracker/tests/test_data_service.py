import pytest
import pandas as pd
from genotracker.services.data_service import load_cohort_data_from_csv
from genotracker.models.data_models import CohortDataSchema
from google.cloud import storage
import io

@pytest.fixture
def local_csv_file(tmp_path):
    data = {
        'study_code': ['S1', 'S2'],
        'monogenic_complex_mixed': ['mono', 'complex'],
        'city': ['City1', 'City2'],
        'geographic_locality': ['Loc1', 'Loc2'],
        'n_dna_samples_attempted': [100, 200],
        'total_qc_pass': [90, 190],
        'callrate_fails': [5, 5],
        'sex_fails': [2, 3],
        'het_fails': [1, 1],
        'duplicates': [1, 1],
        'genotyping_complete': [True, False],
        'imputation_panel': ['Panel1', 'Panel2'],
        'imputation_complete': [True, False],
        'genotypes_shareable': [True, True],
        'gdpr': [False, False],
        'site': ['Site1', 'Site2'],
        'afr_case': [10, 20],
        'afr_control': [5, 10],
        'afr_other': [3, 4],
        'aac_case': [7, 8],
        'aac_control': [2, 2],
        'aac_other': [1, 1],
        'aj_case': [4, 5],
        'aj_control': [2, 3],
        'aj_other': [1, 1],
        'eas_case': [6, 7],
        'eas_control': [3, 3],
        'eas_other': [2, 2],
        'eur_case': [15, 25],
        'eur_control': [10, 15],
        'eur_other': [5, 10],
        'fin_case': [3, 4],
        'fin_control': [2, 2],
        'fin_other': [1, 1],
        'amr_case': [8, 9],
        'amr_control': [4, 5],
        'amr_other': [2, 2],
        'sas_case': [9, 10],
        'sas_control': [5, 6],
        'sas_other': [3, 3],
        'cas_case': [1, 1],
        'cas_control': [0, 0],
        'cas_other': [0, 0],
        'mde_case': [2, 3],
        'mde_control': [1, 2],
        'mde_other': [1, 1],
        'cah_case': [1, 1],
        'cah_control': [1, 1],
        'cah_other': [0, 0],
        'total': [100, 200],
        'new': [True, False],
        'date_last_update': [pd.to_datetime('today').date(), pd.to_datetime('today').date()],
        'compliance': [True, False]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "test.csv"
    df.to_csv(file_path, index=False)
    return file_path

def test_load_cohort_data_from_local_csv(local_csv_file):
    cohort_data = load_cohort_data_from_csv(str(local_csv_file))
    assert len(cohort_data) == 2
    assert isinstance(cohort_data[0], CohortDataSchema)
    assert cohort_data[0].study_code == 'S1'
    assert cohort_data[1].study_code == 'S2'

def test_load_cohort_data_from_gcs(mocker):
    mock_client = mocker.patch('google.cloud.storage.Client')
    mock_bucket = mock_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value
    mock_data = io.BytesIO(b'study_code,monogenic_complex_mixed,city,geographic_locality,n_dna_samples_attempted,total_qc_pass,callrate_fails,sex_fails,het_fails,duplicates,genotyping_complete,imputation_panel,imputation_complete,genotypes_shareable,gdpr,site,afr_case,afr_control,afr_other,aac_case,aac_control,aac_other,aj_case,aj_control,aj_other,eas_case,eas_control,eas_other,eur_case,eur_control,eur_other,fin_case,fin_control,fin_other,amr_case,amr_control,amr_other,sas_case,sas_control,sas_other,cas_case,cas_control,cas_other,mde_case,mde_control,mde_other,cah_case,cah_control,cah_other,total,new,date_last_update,compliance\nS1,mono,City1,Loc1,100,90,5,2,1,1,True,Panel1,True,True,False,Site1,10,5,3,7,2,1,4,2,1,6,3,2,15,10,5,3,2,1,8,4,2,9,5,3,1,0,0,2,1,1,1,1,0,100,True,2023-07-11,True\nS2,complex,City2,Loc2,200,190,5,3,1,1,False,Panel2,False,True,False,Site2,20,10,4,8,2,1,5,3,1,7,3,2,25,15,10,4,2,1,9,5,2,10,6,3,1,0,0,3,2,1,1,1,0,200,False,2023-07-11,False')
    mock_blob.download_as_string.return_value = mock_data.getvalue()

    bucket_name = "test-bucket"
    file_path = "test.csv"
    cohort_data = load_cohort_data_from_csv(file_path, from_gcs=True, bucket_name=bucket_name)

    assert len(cohort_data) == 2
    assert isinstance(cohort_data[0], CohortDataSchema)
    assert cohort_data[0].study_code == 'S1'
    assert cohort_data[1].study_code == 'S2'
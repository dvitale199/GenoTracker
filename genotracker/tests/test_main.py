from fastapi.testclient import TestClient
from genotracker.main import app

client = TestClient(app)

def test_read_data():
    response = client.get("/data")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check that the response is a list
    assert isinstance(data, list)
    
    # Check that the list is not empty
    assert len(data) > 0
    
    # Check the structure of the first item
    first_item = data[0]
    expected_keys = {
        'study_code', 'monogenic_complex_mixed', 'city', 'geographic_locality',
        'n_dna_samples_attempted', 'total_qc_pass', 'callrate_fails', 'sex_fails',
        'het_fails', 'duplicates', 'genotyping_complete', 'imputation_panel',
        'imputation_complete', 'genotypes_shareable', 'gdpr', 'site', 'afr_case',
        'afr_control', 'afr_other', 'aac_case', 'aac_control', 'aac_other', 'aj_case',
        'aj_control', 'aj_other', 'eas_case', 'eas_control', 'eas_other', 'eur_case',
        'eur_control', 'eur_other', 'fin_case', 'fin_control', 'fin_other', 'amr_case',
        'amr_control', 'amr_other', 'sas_case', 'sas_control', 'sas_other', 'cas_case',
        'cas_control', 'cas_other', 'mde_case', 'mde_control', 'mde_other', 'cah_case',
        'cah_control', 'cah_other', 'total', 'new', 'date_last_update', 'compliance'
    }
    assert set(first_item.keys()) == expected_keys
import pandas as pd
from sqlalchemy.orm import Session
from database.database import engine, CohortData
from database.crud import update_date_last_update

def load_data(file_path):
    df = pd.read_csv(file_path)
    
    df.fillna('', inplace=True)
    df.fillna(0, inplace=True)

    session = Session(engine)

    for _, row in df.iterrows():
        genetic_data = CohortData(
            study_code=row.get('study_code', ''),
            monogenic_complex_mixed=row.get('monogenic_complex_mixed', ''),
            city=row.get('city', ''),
            geographic_locality=row.get('geographic_locality', ''),
            n_dna_samples_attempted=row.get('n_dna_samples_attempted', 0),
            total_qc_pass=row.get('total_qc_pass', 0),
            callrate_fails=row.get('callrate_fails', 0),
            sex_fails=row.get('sex_fails', 0),
            het_fails=row.get('het_fails', 0),
            duplicates=row.get('duplicates', 0),
            # AFR=row.get('AFR', 0),
            # AAC=row.get('AAC', 0),
            # AJ=row.get('AJ', 0),
            # EAS=row.get('EAS', 0),
            # EUR=row.get('EUR', 0),
            # FIN=row.get('FIN', 0),
            # AMR=row.get('AMR', 0),
            # SAS=row.get('SAS', 0),
            # CAS=row.get('CAS', 0),
            # MDE=row.get('MDE', 0),
            # CAH=row.get('CAH', 0),
            # total=row.get('total', 0),
            genotyping_complete=bool(row.get('genotyping_complete', False)),
            imputation_panel=row.get('imputation_panel', ''),
            imputation_complete=bool(row.get('imputation_complete', False)),
            genotypes_shareable=bool(row.get('genotypes_shareable', False)),
            gdpr=bool(row.get('gdpr', False)),
            site=row.get('site', ''),
            afr_case=row.get('afr_case', 0),
            afr_control=row.get('afr_control', 0),
            afr_other=row.get('afr_other', 0),
            aac_case=row.get('aac_case', 0),
            aac_control=row.get('aac_control', 0),
            aac_other=row.get('aac_other', 0),
            aj_case=row.get('aj_case', 0),
            aj_control=row.get('aj_control', 0),
            aj_other=row.get('aj_other', 0),
            eas_case=row.get('eas_case', 0),
            eas_control=row.get('eas_control', 0),
            eas_other=row.get('eas_other', 0),
            eur_case=row.get('eur_case', 0),
            eur_control=row.get('eur_control', 0),
            eur_other=row.get('eur_other', 0),
            fin_case=row.get('fin_case', 0),
            fin_control=row.get('fin_control', 0),
            fin_other=row.get('fin_other', 0),
            amr_case=row.get('amr_case', 0),
            amr_control=row.get('amr_control', 0),
            amr_other=row.get('amr_other', 0),
            sas_case=row.get('sas_case', 0),
            sas_control=row.get('sas_control', 0),
            sas_other=row.get('sas_other', 0),
            cas_case=row.get('cas_case', 0),
            cas_control=row.get('cas_control', 0),
            cas_other=row.get('cas_other', 0),
            mde_case=row.get('mde_case', 0),
            mde_control=row.get('mde_control', 0),
            mde_other=row.get('mde_other', 0),
            cah_case=row.get('cah_case', 0),
            cah_control=row.get('cah_control', 0),
            cah_other=row.get('cah_other', 0),
            total=row.get('total', 0),
            new=True,
            compliance=False

        )
        session.add(genetic_data)
        update_date_last_update(row['study_code'])

    session.commit()
    session.close()

if __name__ == "__main__":
    load_data('data/genotracker_clean.csv')
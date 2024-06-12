import pandas as pd
from sqlalchemy.orm import Session
from database import engine, GeneticData

def load_data(file_path):
    df = pd.read_csv(file_path)
    
    df.fillna('', inplace=True)
    df.fillna(0, inplace=True)  

    session = Session(engine)

    for _, row in df.iterrows():
        genetic_data = GeneticData(
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
            AFR=row.get('AFR', 0),
            AAC=row.get('AAC', 0),
            AJ=row.get('AJ', 0),
            EAS=row.get('EAS', 0),
            EUR=row.get('EUR', 0),
            FIN=row.get('FIN', 0),
            AMR=row.get('AMR', 0),
            SAS=row.get('SAS', 0),
            CAS=row.get('CAS', 0),
            MDE=row.get('MDE', 0),
            CAH=row.get('CAH', 0),
            total=row.get('total', 0),
            genotyping_complete=bool(row.get('genotyping_complete', False)),
            imputation_panel=row.get('imputation_panel', ''),
            imputation_complete=bool(row.get('imputation_complete', False)),
            genotypes_shareable=bool(row.get('genotypes_shareable', False)),
            gdpr=bool(row.get('gdpr', False)),
            site=row.get('site', '')
        )
        session.add(genetic_data)

    session.commit()
    session.close()

if __name__ == "__main__":
    load_data('data/genotracker_clean.csv')

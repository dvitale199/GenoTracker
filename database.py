from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class GeneticData(Base):
    __tablename__ = "genetic_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    study_code = Column(String, index=True)
    monogenic_complex_mixed = Column(String)
    city = Column(String)
    geographic_locality = Column(String)
    n_dna_samples_attempted = Column(Integer)
    total_qc_pass = Column(Integer)
    callrate_fails = Column(Integer)
    sex_fails = Column(Integer)
    het_fails = Column(Integer)
    duplicates = Column(Integer)
    AFR = Column(Integer)
    AAC = Column(Integer)
    AJ = Column(Integer)
    EAS = Column(Integer)
    EUR = Column(Integer)
    FIN = Column(Integer)
    AMR = Column(Integer)
    SAS = Column(Integer)
    CAS = Column(Integer)
    MDE = Column(Integer)
    CAH = Column(Integer)
    total = Column(Integer)
    genotyping_complete = Column(Boolean)
    imputation_panel = Column(String)
    imputation_complete = Column(Boolean)
    genotypes_shareable = Column(Boolean)
    gdpr = Column(Boolean)
    site = Column(String)

Base.metadata.create_all(bind=engine)
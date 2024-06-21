from sqlalchemy.orm import Session
from database import engine, GeneticData

def update_new_field_by_study_code(study_code, new_status):
    """
    Update the 'new' field for entries with the given study_code.

    :param study_code: The study code of the entries to update.
    :param new_status: The new status (True or False) to set for the 'new' field.
    """
    session = Session(engine)

    # Update the 'new' field to the new_status for all entries with the specified study_code
    session.query(GeneticData).filter_by(study_code=study_code).update({"new": new_status})

    session.commit()
    session.close()
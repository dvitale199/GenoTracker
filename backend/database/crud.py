from sqlalchemy.orm import Session
from .database import engine, CohortData
from datetime import datetime


def update_fields_by_study_code(study_code, updates):
    """
    Update specific fields for entries with the given study_code.

    :param study_code: The study code of the entries to update.
    :param updates: A dictionary of fields to update with their new values.
    """
    session = Session(engine)
    
    # Update the specified fields for all entries with the specified study_code
    session.query(CohortData).filter_by(study_code=study_code).update(updates)
    
    session.commit()
    session.close()


def update_new_field_by_study_code(study_code, new_status):
    """
    Update the 'new' field for entries with the given study_code.

    :param study_code: The study code of the entries to update.
    :param new_status: The new status (True or False) to set for the 'new' field.
    """
    session = Session(engine)

    # Update the 'new' field to the new_status for all entries with the specified study_code
    session.query(CohortData).filter_by(study_code=study_code).update({"new": new_status})

    session.commit()
    session.close()


def update_date_last_update(study_code, custom_date=None):
    """
    Update the 'date_last_update' field for entries with the given study_code.

    :param study_code: The study code of the entries to update.
    :param custom_date: Optional. The custom date to set for the 'date_last_update' field.
    """
    session = Session(engine)

    # Use the current datetime if no custom date is provided
    date_to_use = custom_date if custom_date else datetime.today()

    # Update the 'date_last_update' field to the date_to_use for all entries with the specified study_code
    session.query(CohortData).filter_by(study_code=study_code).update({"date_last_update": date_to_use})

    session.commit()
    session.close()

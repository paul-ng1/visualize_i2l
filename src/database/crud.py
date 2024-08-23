import logging

from datetime import datetime

from src.database.models import GenerateOutput, Issue, CapturedHistory, GenerateHistory
from src.database.issues_database import Session as IssueSession
from src.database.i2l_database import Session as I2LSession


def get_capture_history(start_date: datetime, end_date: datetime, page: int=1, limit: int=10):
    try:
        with I2LSession() as session:
            rows = session.query(CapturedHistory).filter(CapturedHistory.created_at.between(start_date, end_date)).limit(limit).all()
        return rows
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()
    
def get_generate_history(section_source):
    try:
        with I2LSession() as session:
            row = session.query(GenerateHistory).filter(GenerateHistory.image_source == section_source).first()
        return row
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def insert_database(row: GenerateOutput):
    try:
        with IssueSession() as session:
            session.add(row)
            session.commit()
            session.refresh(row)
        return row
    except Exception as e:
        session.rollback()
        logging.error(f"Insert Database fail: {e}")
        return None
    finally:
        session.close()


def get_page_urls_by_checked_page(page: int=1, limit: int=10, checked: bool|None=None):
    try:
        offset = (page-1)*limit
        with IssueSession() as session:
            if checked is None:
                rows = session.query(GenerateOutput).offset(offset).limit(limit).all()
            else:
                rows = session.query(GenerateOutput).filter(GenerateOutput.checked == checked).offset(offset).limit(limit).all()
        return rows
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def get_capture_url_by_id(id: int):
    try:
        with IssueSession() as session:
            row = session.query(GenerateOutput.capture_url).filter(GenerateOutput.id == id).first()
        return row
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def get_sections_url_by_id(id: int):
    try:
        with IssueSession() as session:
            row = session.query(GenerateOutput.sections_url).filter(GenerateOutput.id == id).first()
        return row
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def get_atoms_url_by_id(id: int):
    try:
        with IssueSession() as session:
            row = session.query(GenerateOutput.atoms_url).filter(GenerateOutput.id == id).first()
        return row
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def get_codegens_url_by_id(id: int):
    try:
        with IssueSession() as session:
            row = session.query(GenerateOutput.codegens_url).filter(GenerateOutput.id == id).first()
        return row
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def convert_generate_output_to_checked(id: int):
    try:
        with IssueSession() as session:
            session.query(GenerateOutput).filter(GenerateOutput.id == id).update({GenerateOutput.checked: True})
        return id
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()


def create_issue(image_url: str, note: str, section_url: str|None=None, service: str="capture"):
    pass

def get_issue():
    pass

def delete_issue():
    pass

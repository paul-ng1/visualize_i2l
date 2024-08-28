import logging

from datetime import datetime

from src.database.models import GenerateOutput, Issue, CapturedHistory, GenerateHistory
from src.database.issues_database import Session as IssueSession
from src.database.i2l_database import Session as I2LSession
from src.database.utils import create_issue_row
from src.database.schemas import IssueTypeEnum


def get_capture_history(start_date: datetime, end_date: datetime, page: int=1, limit: int=10):
    try:
        offset = (page-1)*limit
        with I2LSession() as session:
            rows = session.query(CapturedHistory).filter(CapturedHistory.created_at.between(start_date, end_date)).order_by(CapturedHistory.id.asc()).offset(offset).limit(limit).all()
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

def insert_database(row: GenerateOutput | Issue):
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


def get_generate_outputs_by_checked_and_page(page: int=1, limit: int=10, checked: bool|None=None):
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

def get_generate_output_by_id(id: int):
    try:
        with IssueSession() as session:
            row = session.query(GenerateOutput).filter(GenerateOutput.id == id).first()
        return row
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def update_generate_output_to_checked(id: int):
    try:
        with IssueSession() as session:
            check = session.query(GenerateOutput).filter(GenerateOutput.id == id).update({GenerateOutput.checked: True})
            session.commit()
        return check
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()


def create_issue(generate_output_id: int, issue_image_url: str, issue_type: IssueTypeEnum, note: str):
    try:
        issue = create_issue_row(generate_output_id, issue_image_url, issue_type, note)
        row = insert_database(issue)
        return row
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None

def get_issues_by_page(page: int=1, limit: int=10):
    try:
        offset = (page-1)*limit
        with IssueSession() as session:
            rows = session.query(Issue).offset(offset).limit(limit).all()
        return rows
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def get_issue(id: int):
    try:
        with IssueSession() as session:
            row = session.query(Issue).filter(Issue.id == id).first()
        return row
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def update_issue(id: int):
    try:
        with IssueSession() as session:
            check = session.query(Issue).filter(Issue.id == id).update({Issue.checked: True})
            session.commit()
        return check
    except Exception as e:
        logging.error(f"Get Database fail: {e}")
        return None
    finally:
        session.close()

def delete_issue(id: int):
    try:
        with IssueSession() as session:
            session.query(Issue).filter(Issue.id == id).delete()
            session.commit()
        return id
    except Exception as e:
        session.rollback()
        logging.error(f"Delete Database fail: {e}")
        return None
    finally:
        session.close()

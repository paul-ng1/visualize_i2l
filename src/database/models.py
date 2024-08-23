import datetime

from src.database.issues_database import Base as IssueBase
from src.database.i2l_database import Base as I2LBase

from sqlalchemy import Column, String, Integer, DateTime, Enum, BigInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB


class GenerateOutput(IssueBase):
    __tablename__ = "generate_outputs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    capture_history_id = Column(Integer, unique=True, nullable=False)
    page_url = Column(String, nullable=False)
    capture_url = Column(String, unique=True, nullable=False)
    sections_url = Column(JSONB, nullable=False)
    atoms_url = Column(JSONB)
    codegens_url = Column(JSONB)
    checked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Issue(IssueBase):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, autoincrement=True)
    generate_output_id = Column(Integer, ForeignKey('generate_outputs.id'), nullable=False)
    issue_image_url = Column(String)
    issue_type = Column(Enum('capture', 'section', 'atoms', 'codegen', name='issue_type_enum', create_type=True))
    note = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class GenerateHistory(I2LBase):
    __tablename__ = "generate_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_source = Column(String, nullable=True)
    detected_url = Column(JSONB, nullable=True)
    output_detect = Column(String, nullable=True)
    output_builder = Column(String, nullable=True)
    shop_id = Column(BigInteger, nullable=True)
    page_id = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CapturedHistory(I2LBase):
    __tablename__ = "capture_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_source = Column(String, nullable=True)
    page_url = Column(String, nullable=True)
    page_type = Column(String, nullable=True)
    image_sections_capture = Column(JSONB, nullable=True)
    shop_id = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
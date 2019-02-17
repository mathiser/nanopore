import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Fast5(Base):
    __tablename__ = 'fast5'
    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    filepath = Column(String, nullable=False)
    filename = Column(String, nullable=False)


class Read(Base):
    __tablename__ = 'read'
    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    filepath = Column(String)
    
    filename = Column(String, nullable=True)
    read_id = Column(String, nullable=True)
    run_id = Column(String, nullable=True)
    channel = Column(String, nullable=True)
    start_time = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    num_events = Column(String, nullable=True)
    passes_filtering = Column(String, nullable=True)
    template_start = Column(String, nullable=True)
    num_events_template = Column(String, nullable=True)
    template_duration = Column(String, nullable=True)
    num_called_template = Column(String, nullable=True)
    sequence_length_template = Column(String, nullable=True)
    mean_qscore_template = Column(String, nullable=True)
    strand_score_template = Column(String, nullable=True)
    calibration_strand_genome_template = Column(String, nullable=True)
    calibration_strand_identity_template = Column(String, nullable=True)
    calibration_strand_accuracy_template = Column(String, nullable=True)
    calibration_strand_speed_bps_template = Column(String, nullable=True)
    barcode_arrangement = Column(String, nullable=True)
    barcode_score = Column(String, nullable=True)
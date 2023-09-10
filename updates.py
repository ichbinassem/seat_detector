

from sqlalchemy import create_engine, Column, Integer, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from schema import SeatStatus, engine
import time


Session = sessionmaker(bind=engine)
# Create a session
session = Session()


def query_vacant_seats():
    # Get the most recent vacancy_status for each table_id among the last 60 entries
    subquery = session.query(
        SeatStatus.table_id,
        func.max(SeatStatus.update_time).label('max_update_time')
    ).group_by(SeatStatus.table_id).order_by(func.max(SeatStatus.update_time).desc()).limit(60).subquery()

    result = session.query(
        SeatStatus.table_id,
        SeatStatus.vacancy_status
    ).join(
        subquery,
        SeatStatus.table_id == subquery.c.table_id,
    ).filter(
        SeatStatus.update_time == subquery.c.max_update_time
    ).all()

    for row in result:
        table_id, vacancy_status = row
        print(f"Table ID: {table_id}, Vacancy Status: {vacancy_status}")

while True:
    query_vacant_seats()
    time.sleep(180)  # Sleep for 180 seconds (3 minutes)


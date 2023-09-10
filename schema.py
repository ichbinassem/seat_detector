
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import sessionmaker


# Create an SQLite database file named 'real_estate.db' and enable echo to see the SQL statements
engine = create_engine('sqlite:///real_estate.db', echo=True)




Base = declarative_base()

class SeatStatus(Base):
    __tablename__ = 'seat_status'
    seat_id = Column(Integer, primary_key=True)
    table_id = Column(Integer)
    number_of_people = Column(Integer)
    vacancy_status = Column(Boolean)
    update_time = Column(TIMESTAMP)

# Create the table
Base.metadata.create_all(engine)

# Create a new entry
new_entry = SeatStatus(table_id = 0, number_of_people=4, vacancy_status=True, update_time=datetime.now())

# Insert the new entry into the database
Session = sessionmaker(bind=engine)
session = Session()
session.add(new_entry)
session.commit()

# Query data from the database
results = session.query(SeatStatus).all()
for result in results:
    print(result.seat_id, result.table_id, result.number_of_people, result.vacancy_status, result.update_time)

session.close()

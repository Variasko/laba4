from sqlalchemy import Column, Integer, String, ForeignKey, REAL, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.sql.schema import FetchedValue
from database import Base

class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    goverment_number = Column(String(10), nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    color = Column(String(25), nullable=False)
    production_year = Column(String(4), nullable=False)
    registration_date = Column(DateTime, nullable=False)
    driver_id = Column(Integer, ForeignKey('driver.id'), nullable=False)
    driver = relationship('Driver')

class District(Base):
    __tablename__ = 'district'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    name = Column(String(50), nullable=False)

class Driver(Base):
    __tablename__ = 'driver'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    licence_number = Column(String(20), nullable=False)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    registration_address = Column(String(100), nullable=False)
    phone = Column(String(12))

class Fine(Base):
    __tablename__ = 'fine'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    violation_id = Column(Integer, ForeignKey('violation.id'), nullable=False)
    date_time = Column(DateTime, nullable=False)
    district_id = Column(Integer, ForeignKey('district.id'), nullable=False)
    fine_amount = Column(REAL, nullable=False)
    is_paid = Column(Boolean, nullable=False)
    suspension_period = Column(Integer, nullable=False)
    inspector_id = Column(Integer, ForeignKey('inspector.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('driver.id'), nullable=False)
    violation = relationship('Violation')
    inspector = relationship('Inspector')
    driver = relationship('Driver')

class Inspector(Base):
    __tablename__ = 'inspector'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    service_number = Column(Integer, nullable=False)

class Violation(Base):
    __tablename__ = 'violation'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    min_fine = Column(REAL, nullable=False)
    max_fine = Column(REAL, nullable=False)
    warning_needed = Column(Boolean, nullable=False)
    min_suspension = Column(Integer, nullable=False)
    max_suspension = Column(Integer, nullable=False)
    violation_type_id = Column(Integer, ForeignKey('violation_type.id'), nullable=False)
    violation_code = Column(Integer, nullable=False)
    violation_type = relationship('ViolationType')

class ViolationType(Base):
    __tablename__ = 'violation_type'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, server_default=FetchedValue())
    name = Column(String(50), nullable=False)

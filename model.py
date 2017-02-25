# Model for xml response from NextBus sf-muni
# Adapted from Matt Conway's gtfsrdb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class VehiclePosition(Base):
    __tablename__ = 'vehicle_positions'
    oid = Column(Integer, primary_key=True)

    # Route and vehicle description
    veh_id = Column(String(25))
    route_tag = Column(String(100))
    dir_tag = Column(String(100))

    # Position description
    pos_lat = Column(Float)
    pos_lon = Column(Float)
    pos_speed = Column(Float)

    # Report
    last_report = Column(String(25))

    # Used for two-car trains, will want to remove to not have duplicates
    lead_veh = Column(String(25))

    # Time pulled
    timestamp = Column(DateTime)

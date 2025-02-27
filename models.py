from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship

from database import Base
from enum import Enum as PyEnum

class Role(str, PyEnum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)


class TruckInspectionItemsDB(Base):
    __tablename__ = "truck_inspection_items"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("inspection_reports.id"))
    air_compressor = Column(Boolean, default=False)
    air_compressor_photo = Column(String, nullable=True)
    air_lines = Column(Boolean, default=False)
    air_lines_photo = Column(String, nullable=True)
    battery = Column(Boolean, default=False)
    battery_photo = Column(String, nullable=True)
    belts_and_hoses = Column(Boolean, default=False)
    belts_and_hoses_photo = Column(String, nullable=True)
    body = Column(Boolean, default=False)
    body_photo = Column(String, nullable=True)
    brake_accessories = Column(Boolean, default=False)
    brake_accessories_photo = Column(String, nullable=True)
    brake_parking = Column(Boolean, default=False)
    brake_parking_photo = Column(String, nullable=True)
    brake_service = Column(Boolean, default=False)
    brake_service_photo = Column(String, nullable=True)
    clutch = Column(Boolean, default=False)
    clutch_photo = Column(String, nullable=True)
    coupling_devices = Column(Boolean, default=False)
    coupling_devices_photo = Column(String, nullable=True)
    defroster_heater = Column(Boolean, default=False)
    defroster_heater_photo = Column(String, nullable=True)
    drive_line = Column(Boolean, default=False)
    drive_line_photo = Column(String, nullable=True)
    engine = Column(Boolean, default=False)
    engine_photo = Column(String, nullable=True)
    exhaust = Column(Boolean, default=False)
    exhaust_photo = Column(String, nullable=True)
    fifth_wheel = Column(Boolean, default=False)
    fifth_wheel_photo = Column(String, nullable=True)
    fluid_levels = Column(Boolean, default=False)
    fluid_levels_photo = Column(String, nullable=True)
    frame_and_assembly = Column(Boolean, default=False)
    frame_and_assembly_photo = Column(String, nullable=True)
    front_axle = Column(Boolean, default=False)
    front_axle_photo = Column(String, nullable=True)
    fuel_tanks = Column(Boolean, default=False)
    fuel_tanks_photo = Column(String, nullable=True)
    horn = Column(Boolean, default=False)
    horn_photo = Column(String, nullable=True)
    lights_head_stop = Column(Boolean, default=False)
    lights_head_stop_photo = Column(String, nullable=True)
    lights_tail_dash = Column(Boolean, default=False)
    lights_tail_dash_photo = Column(String, nullable=True)
    lights_turn_indicators = Column(Boolean, default=False)
    lights_turn_indicators_photo = Column(String, nullable=True)
    lights_clearance_marker = Column(Boolean, default=False)
    lights_clearance_marker_photo = Column(String, nullable=True)
    mirrors = Column(Boolean, default=False)
    mirrors_photo = Column(String, nullable=True)
    muffler = Column(Boolean, default=False)
    muffler_photo = Column(String, nullable=True)
    oil_pressure = Column(Boolean, default=False)
    oil_pressure_photo = Column(String, nullable=True)
    radiator = Column(Boolean, default=False)
    radiator_photo = Column(String, nullable=True)
    rear_end = Column(Boolean, default=False)
    rear_end_photo = Column(String, nullable=True)
    reflectors = Column(Boolean, default=False)
    reflectors_photo = Column(String, nullable=True)
    safety_fire_extinguisher = Column(Boolean, default=False)
    safety_fire_extinguisher_photo = Column(String, nullable=True)
    safety_flags_flares_fusees = Column(Boolean, default=False)
    safety_flags_flares_fusees_photo = Column(String, nullable=True)
    safety_reflective_triangles = Column(Boolean, default=False)
    safety_reflective_triangles_photo = Column(String, nullable=True)
    safety_spare_bulbs_and_fuses = Column(Boolean, default=False)
    safety_spare_bulbs_and_fuses_photo = Column(String, nullable=True)
    safety_spare_seal_beam = Column(Boolean, default=False)
    safety_spare_seal_beam_photo = Column(String, nullable=True)
    starter = Column(Boolean, default=False)
    starter_photo = Column(String, nullable=True)
    steering = Column(Boolean, default=False)
    steering_photo = Column(String, nullable=True)
    suspension_system = Column(Boolean, default=False)
    suspension_system_photo = Column(String, nullable=True)
    tire_chains = Column(Boolean, default=False)
    tire_chains_photo = Column(String, nullable=True)
    tires = Column(Boolean, default=False)
    tires_photo = Column(String, nullable=True)
    transmission = Column(Boolean, default=False)
    transmission_photo = Column(String, nullable=True)
    trip_recorder = Column(Boolean, default=False)
    trip_recorder_photo = Column(String, nullable=True)
    wheels_and_rims = Column(Boolean, default=False)
    wheels_and_rims_photo = Column(String, nullable=True)
    windows = Column(Boolean, default=False)
    windows_photo = Column(String, nullable=True)
    windshield_wipers = Column(Boolean, default=False)
    windshield_wipers_photo = Column(String, nullable=True)
    other = Column(Boolean, default=False)
    other_photo = Column(String, nullable=True)
    other_description = Column(String, nullable=True)

    report = relationship("InspectionReportDB", back_populates="truck_inspection_items")


class TrailerInspectionItemsDB(Base):
    __tablename__ = "trailer_inspection_items"

    id = Column(Integer, primary_key=True, index=True)
    trailer_id = Column(Integer, ForeignKey("trailers.id"))
    brake_connections = Column(Boolean, default=False)
    brake_connections_photo = Column(String, nullable=True)
    brakes = Column(Boolean, default=False)
    brakes_photo = Column(String, nullable=True)
    coupling_devices = Column(Boolean, default=False)
    coupling_devices_photo = Column(String, nullable=True)
    coupling_king_pin = Column(Boolean, default=False)
    coupling_king_pin_photo = Column(String, nullable=True)
    doors = Column(Boolean, default=False)
    doors_photo = Column(String, nullable=True)
    hitch = Column(Boolean, default=False)
    hitch_photo = Column(String, nullable=True)
    landing_gear = Column(Boolean, default=False)
    landing_gear_photo = Column(String, nullable=True)
    lights_all = Column(Boolean, default=False)
    lights_all_photo = Column(String, nullable=True)
    reflectors_reflective_tape = Column(Boolean, default=False)
    reflectors_reflective_tape_photo = Column(String, nullable=True)
    roof = Column(Boolean, default=False)
    roof_photo = Column(String, nullable=True)
    suspension_system = Column(Boolean, default=False)
    suspension_system_photo = Column(String, nullable=True)
    tarpaulin = Column(Boolean, default=False)
    tarpaulin_photo = Column(String, nullable=True)
    tires = Column(Boolean, default=False)
    tires_photo = Column(String, nullable=True)
    wheels_and_rims = Column(Boolean, default=False)
    wheels_and_rims_photo = Column(String, nullable=True)
    other = Column(Boolean, default=False)
    other_photo = Column(String, nullable=True)
    other_description = Column(String, nullable=True)

    trailer = relationship("TrailerDB", back_populates="inspection_items")


class TrailerDB(Base):
    __tablename__ = "trailers"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("inspection_reports.id"))
    trailer_number = Column(String, index=True)

    report = relationship("InspectionReportDB", back_populates="trailers")
    inspection_items = relationship("TrailerInspectionItemsDB", uselist=False, back_populates="trailer", cascade="all, delete-orphan")


class InspectionReportDB(Base):
    __tablename__ = "inspection_reports"

    id = Column(Integer, primary_key=True, index=True)
    carrier = Column(String, index=True)
    address = Column(String)
    inspection_date = Column(DateTime)
    truck_number = Column(String, index=True)
    odometer_reading = Column(Integer)
    remarks = Column(Text, nullable=True)

    truck_inspection_items = relationship("TruckInspectionItemsDB", uselist=False, back_populates="report", cascade="all, delete-orphan")
    trailers = relationship("TrailerDB", back_populates="report", cascade="all, delete-orphan")
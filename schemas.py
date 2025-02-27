from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(BaseModel):
    username: str
    role: Role = Role.USER


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Role] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TruckInspectionItems(BaseModel):
    air_compressor: bool = False
    air_lines: bool = False
    battery: bool = False
    belts_and_hoses: bool = False
    body: bool = False
    brake_accessories: bool = False
    brake_parking: bool = False
    brake_service: bool = False
    clutch: bool = False
    coupling_devices: bool = False
    defroster_heater: bool = False
    drive_line: bool = False
    engine: bool = False
    exhaust: bool = False
    fifth_wheel: bool = False
    fluid_levels: bool = False
    frame_and_assembly: bool = False
    front_axle: bool = False
    fuel_tanks: bool = False
    horn: bool = False
    lights_head_stop: bool = False
    lights_tail_dash: bool = False
    lights_turn_indicators: bool = False
    lights_clearance_marker: bool = False
    mirrors: bool = False
    muffler: bool = False
    oil_pressure: bool = False
    radiator: bool = False
    rear_end: bool = False
    reflectors: bool = False
    safety_fire_extinguisher: bool = False
    safety_flags_flares_fusees: bool = False
    safety_reflective_triangles: bool = False
    safety_spare_bulbs_and_fuses: bool = False
    safety_spare_seal_beam: bool = False
    starter: bool = False
    steering: bool = False
    suspension_system: bool = False
    tire_chains: bool = False
    tires: bool = False
    transmission: bool = False
    trip_recorder: bool = False
    wheels_and_rims: bool = False
    windows: bool = False
    windshield_wipers: bool = False
    other: bool = False
    other_description: Optional[str] = None


class TrailerInspectionItems(BaseModel):
    brake_connections: bool = False
    brakes: bool = False
    coupling_devices: bool = False
    coupling_king_pin: bool = False
    doors: bool = False
    hitch: bool = False
    landing_gear: bool = False
    lights_all: bool = False
    reflectors_reflective_tape: bool = False
    roof: bool = False
    suspension_system: bool = False
    tarpaulin: bool = False
    tires: bool = False
    wheels_and_rims: bool = False
    other: bool = False
    other_description: Optional[str] = None


class Trailer(BaseModel):
    trailer_number: str
    inspection_items: TrailerInspectionItems


class VehicleInspectionReport(BaseModel):
    carrier: str
    address: str
    inspection_date: datetime
    truck_number: str
    odometer_reading: int
    truck_inspection_items: TruckInspectionItems
    trailers: List[Trailer] = []
    remarks: Optional[str] = None
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
    air_compressor_photo: Optional[str] = None
    air_lines: bool = False
    air_lines_photo: Optional[str] = None
    battery: bool = False
    battery_photo: Optional[str] = None
    belts_and_hoses: bool = False
    belts_and_hoses_photo: Optional[str] = None
    body: bool = False
    body_photo: Optional[str] = None
    brake_accessories: bool = False
    brake_accessories_photo: Optional[str] = None
    brake_parking: bool = False
    brake_parking_photo: Optional[str] = None
    brake_service: bool = False
    brake_service_photo: Optional[str] = None
    clutch: bool = False
    clutch_photo: Optional[str] = None
    coupling_devices: bool = False
    coupling_devices_photo: Optional[str] = None
    defroster_heater: bool = False
    defroster_heater_photo: Optional[str] = None
    drive_line: bool = False
    drive_line_photo: Optional[str] = None
    engine: bool = False
    engine_photo: Optional[str] = None
    exhaust: bool = False
    exhaust_photo: Optional[str] = None
    fifth_wheel: bool = False
    fifth_wheel_photo: Optional[str] = None
    fluid_levels: bool = False
    fluid_levels_photo: Optional[str] = None
    frame_and_assembly: bool = False
    frame_and_assembly_photo: Optional[str] = None
    front_axle: bool = False
    front_axle_photo: Optional[str] = None
    fuel_tanks: bool = False
    fuel_tanks_photo: Optional[str] = None
    horn: bool = False
    horn_photo: Optional[str] = None
    lights_head_stop: bool = False
    lights_head_stop_photo: Optional[str] = None
    lights_tail_dash: bool = False
    lights_tail_dash_photo: Optional[str] = None
    lights_turn_indicators: bool = False
    lights_turn_indicators_photo: Optional[str] = None
    lights_clearance_marker: bool = False
    lights_clearance_marker_photo: Optional[str] = None
    mirrors: bool = False
    mirrors_photo: Optional[str] = None
    muffler: bool = False
    muffler_photo: Optional[str] = None
    oil_pressure: bool = False
    oil_pressure_photo: Optional[str] = None
    radiator: bool = False
    radiator_photo: Optional[str] = None
    rear_end: bool = False
    rear_end_photo: Optional[str] = None
    reflectors: bool = False
    reflectors_photo: Optional[str] = None
    safety_fire_extinguisher: bool = False
    safety_fire_extinguisher_photo: Optional[str] = None
    safety_flags_flares_fusees: bool = False
    safety_flags_flares_fusees_photo: Optional[str] = None
    safety_reflective_triangles: bool = False
    safety_reflective_triangles_photo: Optional[str] = None
    safety_spare_bulbs_and_fuses: bool = False
    safety_spare_bulbs_and_fuses_photo: Optional[str] = None
    safety_spare_seal_beam: bool = False
    safety_spare_seal_beam_photo: Optional[str] = None
    starter: bool = False
    starter_photo: Optional[str] = None
    steering: bool = False
    steering_photo: Optional[str] = None
    suspension_system: bool = False
    suspension_system_photo: Optional[str] = None
    tire_chains: bool = False
    tire_chains_photo: Optional[str] = None
    tires: bool = False
    tires_photo: Optional[str] = None
    transmission: bool = False
    transmission_photo: Optional[str] = None
    trip_recorder: bool = False
    trip_recorder_photo: Optional[str] = None
    wheels_and_rims: bool = False
    wheels_and_rims_photo: Optional[str] = None
    windows: bool = False
    windows_photo: Optional[str] = None
    windshield_wipers: bool = False
    windshield_wipers_photo: Optional[str] = None
    other: bool = False
    other_photo: Optional[str] = None
    other_description: Optional[str] = None


class TrailerInspectionItems(BaseModel):
    brake_connections: bool = False
    brake_connections_photo: Optional[str] = None
    brakes: bool = False
    brakes_photo: Optional[str] = None
    coupling_devices: bool = False
    coupling_devices_photo: Optional[str] = None
    coupling_king_pin: bool = False
    coupling_king_pin_photo: Optional[str] = None
    doors: bool = False
    doors_photo: Optional[str] = None
    hitch: bool = False
    hitch_photo: Optional[str] = None
    landing_gear: bool = False
    landing_gear_photo: Optional[str] = None
    lights_all: bool = False
    lights_all_photo: Optional[str] = None
    reflectors_reflective_tape: bool = False
    reflectors_reflective_tape_photo: Optional[str] = None
    roof: bool = False
    roof_photo: Optional[str] = None
    suspension_system: bool = False
    suspension_system_photo: Optional[str] = None
    tarpaulin: bool = False
    tarpaulin_photo: Optional[str] = None
    tires: bool = False
    tires_photo: Optional[str] = None
    wheels_and_rims: bool = False
    wheels_and_rims_photo: Optional[str] = None
    other: bool = False
    other_photo: Optional[str] = None
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
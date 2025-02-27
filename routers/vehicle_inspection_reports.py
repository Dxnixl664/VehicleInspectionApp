from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Role as RoleModel, InspectionReportDB, TruckInspectionItemsDB, TrailerDB, TrailerInspectionItemsDB
from schemas import VehicleInspectionReport, TruckInspectionItems, TrailerInspectionItems, Trailer
from database import get_db
from security import get_current_user


router = APIRouter(prefix="/vehicle-inspection-reports", tags=["Vehicle Inspection Reports"])


@router.post("/", response_model=VehicleInspectionReport)
def create_vehicle_inspection_report(
        report_data: VehicleInspectionReport,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Crear un reporte de inspección de vehículo.
    """
    if current_user.role != RoleModel.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios con rol 'user' pueden crear reportes."
        )

    # 1) Crear el reporte principal
    db_report = InspectionReportDB(
        carrier=report_data.carrier,
        address=report_data.address,
        inspection_date=report_data.inspection_date,
        truck_number=report_data.truck_number,
        odometer_reading=report_data.odometer_reading,
        remarks=report_data.remarks
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # 2) Crear los items de inspección del camión
    truck_items_data = report_data.truck_inspection_items
    db_truck_items = TruckInspectionItemsDB(
        report_id=db_report.id,
        air_compressor=truck_items_data.air_compressor,
        air_lines=truck_items_data.air_lines,
        battery=truck_items_data.battery,
        belts_and_hoses=truck_items_data.belts_and_hoses,
        body=truck_items_data.body,
        brake_accessories=truck_items_data.brake_accessories,
        brake_parking=truck_items_data.brake_parking,
        brake_service=truck_items_data.brake_service,
        clutch=truck_items_data.clutch,
        coupling_devices=truck_items_data.coupling_devices,
        defroster_heater=truck_items_data.defroster_heater,
        drive_line=truck_items_data.drive_line,
        engine=truck_items_data.engine,
        exhaust=truck_items_data.exhaust,
        fifth_wheel=truck_items_data.fifth_wheel,
        fluid_levels=truck_items_data.fluid_levels,
        frame_and_assembly=truck_items_data.frame_and_assembly,
        front_axle=truck_items_data.front_axle,
        fuel_tanks=truck_items_data.fuel_tanks,
        horn=truck_items_data.horn,
        lights_head_stop=truck_items_data.lights_head_stop,
        lights_tail_dash=truck_items_data.lights_tail_dash,
        lights_turn_indicators=truck_items_data.lights_turn_indicators,
        lights_clearance_marker=truck_items_data.lights_clearance_marker,
        mirrors=truck_items_data.mirrors,
        muffler=truck_items_data.muffler,
        oil_pressure=truck_items_data.oil_pressure,
        radiator=truck_items_data.radiator,
        rear_end=truck_items_data.rear_end,
        reflectors=truck_items_data.reflectors,
        safety_fire_extinguisher=truck_items_data.safety_fire_extinguisher,
        safety_flags_flares_fusees=truck_items_data.safety_flags_flares_fusees,
        safety_reflective_triangles=truck_items_data.safety_reflective_triangles,
        safety_spare_bulbs_and_fuses=truck_items_data.safety_spare_bulbs_and_fuses,
        safety_spare_seal_beam=truck_items_data.safety_spare_seal_beam,
        starter=truck_items_data.starter,
        steering=truck_items_data.steering,
        suspension_system=truck_items_data.suspension_system,
        tire_chains=truck_items_data.tire_chains,
        tires=truck_items_data.tires,
        transmission=truck_items_data.transmission,
        trip_recorder=truck_items_data.trip_recorder,
        wheels_and_rims=truck_items_data.wheels_and_rims,
        windows=truck_items_data.windows,
        windshield_wipers=truck_items_data.windshield_wipers,
        other=truck_items_data.other,
        other_description=truck_items_data.other_description
    )
    db.add(db_truck_items)
    db.commit()
    db.refresh(db_truck_items)

    # 3) Crear los items de inspección de cada trailer
    for trailer in report_data.trailers:
        db_trailer = TrailerDB(
            report_id=trailer.report_id,
            trailer_number=trailer.trailer_number,
        )
        db.add(db_trailer)
        db.commit()
        db.refresh(db_trailer)

        trailer_items_data = trailer.inspection_items
        db_trailer_inspection = TrailerInspectionItemsDB(
            trailer_id=db_trailer.id,
            brake_connections=trailer_items_data.brake_connections,
            brakes=trailer_items_data.brakes,
            coupling_devices=trailer_items_data.coupling_devices,
            coupling_king_pin=trailer_items_data.coupling_king_pin,
            doors=trailer_items_data.doors,
            hitch=trailer_items_data.hitch,
            landing_gear=trailer_items_data.landing_gear,
            lights_all=trailer_items_data.lights_all,
            reflectors_reflective_tape=trailer_items_data.reflectors_reflective_tape,
            roof=trailer_items_data.roof,
            suspension_system=trailer_items_data.suspension_system,
            tarpaulin=trailer_items_data.tarpaulin,
            tires=trailer_items_data.tires,
            wheels_and_rims=trailer_items_data.wheels_and_rims,
            other=trailer_items_data.other,
            other_description=trailer_items_data.other_description
        )
        db.add(db_trailer_inspection)

    db.commit()

    return report_data


@router.get("/", response_model=List[VehicleInspectionReport])
def list_vehicle_inspection_reports(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Listar todos los reportes de inspección de vehículo.
    """
    if current_user.role != RoleModel.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios con rol 'admin' pueden ver los reportes."
        )

    db_reports = db.query(InspectionReportDB).all()
    results = []

    for report in db_reports:
        db_truck_items = (
            db.query(TruckInspectionItemsDB)
            .filter_by(report_id=report.id)
            .first()
        )
        truck_inspection = TruckInspectionItems()
        if db_truck_items:
            truck_inspection = TruckInspectionItems(
                air_compressor=db_truck_items.air_compressor,
                air_lines=db_truck_items.air_lines,
                battery=db_truck_items.battery,
                belts_and_hoses=db_truck_items.belts_and_hoses,
                body=db_truck_items.body,
                brake_accessories=db_truck_items.brake_accessories,
                brake_parking=db_truck_items.brake_parking,
                brake_service=db_truck_items.brake_service,
                clutch=db_truck_items.clutch,
                coupling_devices=db_truck_items.coupling_devices,
                defroster_heater=db_truck_items.defroster_heater,
                drive_line=db_truck_items.drive_line,
                engine=db_truck_items.engine,
                exhaust=db_truck_items.exhaust,
                fifth_wheel=db_truck_items.fifth_wheel,
                fluid_levels=db_truck_items.fluid_levels,
                frame_and_assembly=db_truck_items.frame_and_assembly,
                front_axle=db_truck_items.front_axle,
                fuel_tanks=db_truck_items.fuel_tanks,
                horn=db_truck_items.horn,
                lights_head_stop=db_truck_items.lights_head_stop,
                lights_tail_dash=db_truck_items.lights_tail_dash,
                lights_turn_indicators=db_truck_items.lights_turn_indicators,
                lights_clearance_marker=db_truck_items.lights_clearance_marker,
                mirrors=db_truck_items.mirrors,
                muffler=db_truck_items.muffler,
                oil_pressure=db_truck_items.oil_pressure,
                radiator=db_truck_items.radiator,
                rear_end=db_truck_items.rear_end,
                reflectors=db_truck_items.reflectors,
                safety_fire_extinguisher=db_truck_items.safety_fire_extinguisher,
                safety_flags_flares_fusees=db_truck_items.safety_flags_flares_fusees,
                safety_reflective_triangles=db_truck_items.safety_reflective_triangles,
                safety_spare_bulbs_and_fuses=db_truck_items.safety_spare_bulbs_and_fuses,
                safety_spare_seal_beam=db_truck_items.safety_spare_seal_beam,
                starter=db_truck_items.starter,
                steering=db_truck_items.steering,
                suspension_system=db_truck_items.suspension_system,
                tire_chains=db_truck_items.tire_chains,
                tires=db_truck_items.tires,
                transmission=db_truck_items.transmission,
                trip_recorder=db_truck_items.trip_recorder,
                wheels_and_rims=db_truck_items.wheels_and_rims,
                windows=db_truck_items.windows,
                windshield_wipers=db_truck_items.windshield_wipers,
                other=db_truck_items.other,
                other_description=db_truck_items.other_description
            )

        db_trailers = db.query(TrailerDB).filter_by(report_id=report.id).all()
        trailer_list = []
        for db_trailer in db_trailers:
            db_trailer_items = (
                db.query(TrailerInspectionItemsDB)
                .filter_by(trailer_id=db_trailer.id)
                .first()
            )
            trailer_items = TrailerInspectionItems()
            if db_trailer_items:
                trailer_items = TrailerInspectionItems(
                    brake_connections=db_trailer_items.brake_connections,
                    brakes=db_trailer_items.brakes,
                    coupling_devices=db_trailer_items.coupling_devices,
                    coupling_king_pin=db_trailer_items.coupling_king_pin,
                    doors=db_trailer_items.doors,
                    hitch=db_trailer_items.hitch,
                    landing_gear=db_trailer_items.landing_gear,
                    lights_all=db_trailer_items.lights_all,
                    reflectors_reflective_tape=db_trailer_items.reflectors_reflective_tape,
                    roof=db_trailer_items.roof,
                    suspension_system=db_trailer_items.suspension_system,
                    tarpaulin=db_trailer_items.tarpaulin,
                    tires=db_trailer_items.tires,
                    wheels_and_rims=db_trailer_items.wheels_and_rims,
                    other=db_trailer_items.other,
                    other_description=db_trailer_items.other_description
                )

            trailer_list.append(
                Trailer(
                    trailer_number=db_trailer.trailer_number,
                    inspection_items=trailer_items,
                )
            )

        result_schema = VehicleInspectionReport(
            carrier=report.carrier,
            address=report.address,
            inspection_date=report.inspection_date,
            truck_number=report.truck_number,
            odometer_reading=report.odometer_reading,
            truck_inspection_items=truck_inspection,
            trailers=trailer_list,
            remarks=report.remarks
        )
        results.append(result_schema)

    return results


@router.get("/{report_id}", response_model=VehicleInspectionReport)
def get_vehicle_inspection_report(
        report_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Obtener un reporte de inspección de vehículo.
    """
    if current_user.role != RoleModel.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios con rol 'admin' pueden ver el reporte."
        )

    db_report = db.query(InspectionReportDB).filter_by(id=report_id).first()
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte de inspección no encontrado."
        )

    db_truck_items = (
        db.query(TruckInspectionItemsDB)
        .filter_by(report_id=report_id)
        .first()
    )
    truck_inspection = TruckInspectionItems()
    if db_truck_items:
        truck_inspection = TruckInspectionItems(
            air_compressor=db_truck_items.air_compressor,
            air_lines=db_truck_items.air_lines,
            battery=db_truck_items.battery,
            belts_and_hoses=db_truck_items.belts_and_hoses,
            body=db_truck_items.body,
            brake_accessories=db_truck_items.brake_accessories,
            brake_parking=db_truck_items.brake_parking,
            brake_service=db_truck_items.brake_service,
            clutch=db_truck_items.clutch,
            coupling_devices=db_truck_items.coupling_devices,
            defroster_heater=db_truck_items.defroster_heater,
            drive_line=db_truck_items.drive_line,
            engine=db_truck_items.engine,
            exhaust=db_truck_items.exhaust,
            fifth_wheel=db_truck_items.fifth_wheel,
            fluid_levels=db_truck_items.fluid_levels,
            frame_and_assembly=db_truck_items.frame_and_assembly,
            front_axle=db_truck_items.front_axle,
            fuel_tanks=db_truck_items.fuel_tanks,
            horn=db_truck_items.horn,
            lights_head_stop=db_truck_items.lights_head_stop,
            lights_tail_dash=db_truck_items.lights_tail_dash,
            lights_turn_indicators=db_truck_items.lights_turn_indicators,
            lights_clearance_marker=db_truck_items.lights_clearance_marker,
            mirrors=db_truck_items.mirrors,
            muffler=db_truck_items.muffler,
            oil_pressure=db_truck_items.oil_pressure,
            radiator=db_truck_items.radiator,
            rear_end=db_truck_items.rear_end,
            reflectors=db_truck_items.reflectors,
            safety_fire_extinguisher=db_truck_items.safety_fire_extinguisher,
            safety_flags_flares_fusees=db_truck_items.safety_flags_flares_fusees,
            safety_reflective_triangles=db_truck_items.safety_reflective_triangles,
            safety_spare_bulbs_and_fuses=db_truck_items.safety_spare_bulbs_and_fuses,
            safety_spare_seal_beam=db_truck_items.safety_spare_seal_beam,
            starter=db_truck_items.starter,
            steering=db_truck_items.steering,
            suspension_system=db_truck_items.suspension_system,
            tire_chains=db_truck_items.tire_chains,
            tires=db_truck_items.tires,
            transmission=db_truck_items.transmission,
            trip_recorder=db_truck_items.trip_recorder,
            wheels_and_rims=db_truck_items.wheels_and_rims,
            windows=db_truck_items.windows,
            windshield_wipers=db_truck_items.windshield_wipers,
            other=db_truck_items.other,
            other_description=db_truck_items.other_description
        )

    db_trailers = db.query(TrailerDB).filter_by(report_id=db_report.id).all()
    trailer_list = []
    for db_trailer in db_trailers:
        db_trailer_items = (
            db.query(TrailerInspectionItemsDB)
            .filter_by(report_id=db_trailer.id)
            .first()
        )
        trailer_items = TrailerInspectionItemsDB()
        if db_trailer_items:
            trailer_items = TrailerInspectionItems(
                brake_connections=db_trailer_items.brake_connections,
                brakes=db_trailer_items.brakes,
                coupling_devices=db_trailer_items.coupling_devices,
                coupling_king_pin=db_trailer_items.coupling_king_pin,
                doors=db_trailer_items.doors,
                hitch=db_trailer_items.hitch,
                landing_gear=db_trailer_items.landing_gear,
                lights_all=db_trailer_items.lights_all,
                reflectors_reflective_tape=db_trailer_items.reflectors_reflective_tape,
                roof=db_trailer_items.roof,
                suspension_system=db_trailer_items.suspension_system,
                tarpaulin=db_trailer_items.tarpaulin,
                tires=db_trailer_items.tires,
                wheels_and_rims=db_trailer_items.wheels_and_rims,
                other=db_trailer_items.other,
                other_description=db_trailer_items.other_description,
            )

        trailer_list.append(
            Trailer(
                trailer_number=db_trailer.trailer_number,
                inspection_items=trailer_items,
            )
        )

    return VehicleInspectionReport(
        carrier=db_report.carrier,
        address=db_report.address,
        inspection_date=db_report.inspection_date,
        truck_number=db_report.truck_number,
        odometer_reading=db_report.odometer_reading,
        truck_inspection_items=truck_inspection,
        trailers=trailer_list,
        remarks=db_report.remarks
    )



@router.patch("/{report_id}", response_model=VehicleInspectionReport)
def update_vehicle_inspection_report(
        report_id: int,
        report_data: VehicleInspectionReport,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Actualizar un reporte de inspección de vehículo.
    """
    if current_user.role != RoleModel.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios con rol 'admin' pueden editar reportes."
        )

    db_report = db.query(InspectionReportDB).filter_by(id=report_id).first()
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte de inspección no encontrado."
        )

    db_report.carrier = report_data.carrier
    db_report.address = report_data.address
    db_report.inspection_date = report_data.inspection_date
    db_report.truck_number = report_data.truck_number
    db_report.odometer_reading = report_data.odometer_reading
    db_report.remarks = report_data.remarks

    db_truck_items = (
        db.query(TruckInspectionItemsDB)
        .filter_by(report_id=db_report.id)
        .first()
    )

    if db_truck_items:
        t_items = report_data.truck_inspection_items
        db_truck_items.air_compressor = t_items.air_compressor
        db_truck_items.air_lines = t_items.air_lines
        db_truck_items.battery = t_items.battery
        db_truck_items.belts_and_hoses = t_items.belts_and_hoses
        db_truck_items.body = t_items.body
        db_truck_items.brake_accessories = t_items.brake_accessories
        db_truck_items.brake_parking = t_items.brake_parking
        db_truck_items.brake_service = t_items.brake_service
        db_truck_items.clutch = t_items.clutch
        db_truck_items.coupling_devices = t_items.coupling_devices
        db_truck_items.defroster_heater = t_items.defroster_heater
        db_truck_items.drive_line = t_items.drive_line
        db_truck_items.engine = t_items.engine
        db_truck_items.exhaust = t_items.exhaust
        db_truck_items.fifth_wheel = t_items.fifth_wheel
        db_truck_items.fluid_levels = t_items.fluid_levels
        db_truck_items.frame_and_assembly = t_items.frame_and_assembly
        db_truck_items.front_axle = t_items.front_axle
        db_truck_items.fuel_tanks = t_items.fuel_tanks
        db_truck_items.horn = t_items.horn
        db_truck_items.lights_head_stop = t_items.lights_head_stop
        db_truck_items.lights_tail_dash = t_items.lights_tail_dash
        db_truck_items.lights_turn_indicators = t_items.lights_turn_indicators
        db_truck_items.lights_clearance_marker = t_items.lights_clearance_marker
        db_truck_items.mirrors = t_items.mirrors
        db_truck_items.muffler = t_items.muffler
        db_truck_items.oil_pressure = t_items.oil_pressure
        db_truck_items.radiator = t_items.radiator
        db_truck_items.rear_end = t_items.rear_end
        db_truck_items.reflectors = t_items.reflectors
        db_truck_items.safety_fire_extinguisher = t_items.safety_fire_extinguisher
        db_truck_items.safety_flags_flares_fusees = t_items.safety_flags_flares_fusees
        db_truck_items.safety_reflective_triangles = t_items.safety_reflective_triangles
        db_truck_items.safety_spare_bulbs_and_fuses = t_items.safety_spare_bulbs_and_fuses
        db_truck_items.safety_spare_seal_beam = t_items.safety_spare_seal_beam
        db_truck_items.starter = t_items.starter
        db_truck_items.steering = t_items.steering
        db_truck_items.suspension_system = t_items.suspension_system
        db_truck_items.tire_chains = t_items.tire_chains
        db_truck_items.tires = t_items.tires
        db_truck_items.transmission = t_items.transmission
        db_truck_items.trip_recorder = t_items.trip_recorder
        db_truck_items.wheels_and_rims = t_items.wheels_and_rims
        db_truck_items.windows = t_items.windows
        db_truck_items.windshield_wipers = t_items.windshield_wipers
        db_truck_items.other = t_items.other
        db_truck_items.other_description = t_items.other_description
    else:
        pass

    for new_trailer_data in report_data.trailers:
        db_trailer = (
            db.query(TrailerDB)
            .filter_by(report_id=db_report.id, trailer_number=new_trailer_data.trailer_number)
            .first()
        )

        if db_trailer:
            db_trailer_items = (
                db.query(TrailerInspectionItemsDB)
                .filter_by(trailer_id=db_trailer.id)
                .first()
            )
            if db_trailer_items:
                it = new_trailer_data.inspection_items
                db_trailer_items.brake_connections = it.brake_connections
                db_trailer_items.brakes = it.brakes
                db_trailer_items.coupling_devices = it.coupling_devices
                db_trailer_items.coupling_king_pin = it.coupling_king_pin
                db_trailer_items.doors = it.doors
                db_trailer_items.hitch = it.hitch
                db_trailer_items.landing_gear = it.landing_gear
                db_trailer_items.lights_all = it.lights_all
                db_trailer_items.reflectors_reflective_tape = it.reflectors_reflective_tape
                db_trailer_items.roof = it.roof
                db_trailer_items.suspension_system = it.suspension_system
                db_trailer_items.tarpaulin = it.tarpaulin
                db_trailer_items.tires = it.tires
                db_trailer_items.wheels_and_rims = it.wheels_and_rims
                db_trailer_items.other = it.other
                db_trailer_items.other_description = it.other_description
            else:
                pass

        else:
            pass

    db.commit()
    db.refresh(db_report)

    return report_data


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle_inspection_report(
        report_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Eliminar un reporte de inspección de vehículo.
    """
    if current_user.role != RoleModel.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios con rol 'admin' pueden eliminar reportes."
        )

    db_report = db.query(InspectionReportDB).filter_by(id=report_id).first()
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte de inspección no encontrado."
        )

    db_truck_items = db.query(TruckInspectionItemsDB).filter_by(report_id=db_report.id).first()
    if db_truck_items:
        db.delete(db_truck_items)

    db_trailers = db.query(TrailerDB).filter_by(report_id=db_report.id).all()
    for trailer in db_trailers:
        db_trailer_items = db.query(TrailerInspectionItemsDB).filter_by(trailer_id=trailer.id).first()
        if db_trailer_items:
            db.delete(db_trailer_items)
        db.delete(trailer)

    db.delete(db_report)
    db.commit()

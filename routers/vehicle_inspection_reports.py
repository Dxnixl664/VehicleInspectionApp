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
        air_compressor_photo=truck_items_data.air_compressor_photo,
        air_lines=truck_items_data.air_lines,
        air_lines_photo=truck_items_data.air_lines_photo,
        battery=truck_items_data.battery,
        battery_photo=truck_items_data.battery_photo,
        belts_and_hoses=truck_items_data.belts_and_hoses,
        belts_and_hoses_photo=truck_items_data.belts_and_hoses_photo,
        body=truck_items_data.body,
        body_photo=truck_items_data.body_photo,
        brake_accessories=truck_items_data.brake_accessories,
        brake_accessories_photo=truck_items_data.brake_accessories_photo,
        brake_parking=truck_items_data.brake_parking,
        brake_parking_photo=truck_items_data.brake_parking_photo,
        brake_service=truck_items_data.brake_service,
        brake_service_photo=truck_items_data.brake_service_photo,
        clutch=truck_items_data.clutch,
        clutch_photo=truck_items_data.clutch_photo,
        coupling_devices=truck_items_data.coupling_devices,
        coupling_devices_photo=truck_items_data.coupling_devices_photo,
        defroster_heater=truck_items_data.defroster_heater,
        defroster_heater_photo=truck_items_data.defroster_heater_photo,
        drive_line=truck_items_data.drive_line,
        drive_line_photo=truck_items_data.drive_line_photo,
        engine=truck_items_data.engine,
        engine_photo=truck_items_data.engine_photo,
        exhaust=truck_items_data.exhaust,
        exhaust_photo=truck_items_data.exhaust_photo,
        fifth_wheel=truck_items_data.fifth_wheel,
        fifth_wheel_photo=truck_items_data.fifth_wheel_photo,
        fluid_levels=truck_items_data.fluid_levels,
        fluid_levels_photo=truck_items_data.fluid_levels_photo,
        frame_and_assembly=truck_items_data.frame_and_assembly,
        frame_and_assembly_photo=truck_items_data.frame_and_assembly_photo,
        front_axle=truck_items_data.front_axle,
        front_axle_photo=truck_items_data.front_axle_photo,
        fuel_tanks=truck_items_data.fuel_tanks,
        fuel_tanks_photo=truck_items_data.fuel_tanks_photo,
        horn=truck_items_data.horn,
        horn_photo=truck_items_data.horn_photo,
        lights_head_stop=truck_items_data.lights_head_stop,
        lights_head_stop_photo=truck_items_data.lights_head_stop_photo,
        lights_tail_dash=truck_items_data.lights_tail_dash,
        lights_tail_dash_photo=truck_items_data.lights_tail_dash_photo,
        lights_turn_indicators=truck_items_data.lights_turn_indicators,
        lights_turn_indicators_photo=truck_items_data.lights_turn_indicators_photo,
        lights_clearance_marker=truck_items_data.lights_clearance_marker,
        lights_clearance_marker_photo=truck_items_data.lights_clearance_marker_photo,
        mirrors=truck_items_data.mirrors,
        mirrors_photo=truck_items_data.mirrors_photo,
        muffler=truck_items_data.muffler,
        muffler_photo=truck_items_data.muffler_photo,
        oil_pressure=truck_items_data.oil_pressure,
        oil_pressure_photo=truck_items_data.oil_pressure_photo,
        radiator=truck_items_data.radiator,
        radiator_photo=truck_items_data.radiator_photo,
        rear_end=truck_items_data.rear_end,
        rear_end_photo=truck_items_data.rear_end_photo,
        reflectors=truck_items_data.reflectors,
        reflectors_photo=truck_items_data.reflectors_photo,
        safety_fire_extinguisher=truck_items_data.safety_fire_extinguisher,
        safety_fire_extinguisher_photo=truck_items_data.safety_fire_extinguisher_photo,
        safety_flags_flares_fusees=truck_items_data.safety_flags_flares_fusees,
        safety_flags_flares_fusees_photo=truck_items_data.safety_flags_flares_fusees_photo,
        safety_reflective_triangles=truck_items_data.safety_reflective_triangles,
        safety_reflective_triangles_photo=truck_items_data.safety_reflective_triangles_photo,
        safety_spare_bulbs_and_fuses=truck_items_data.safety_spare_bulbs_and_fuses,
        safety_spare_bulbs_and_fuses_photo=truck_items_data.safety_spare_bulbs_and_fuses_photo,
        safety_spare_seal_beam=truck_items_data.safety_spare_seal_beam,
        safety_spare_seal_beam_photo=truck_items_data.safety_spare_seal_beam_photo,
        starter=truck_items_data.starter,
        starter_photo=truck_items_data.starter_photo,
        steering=truck_items_data.steering,
        steering_photo=truck_items_data.steering_photo,
        suspension_system=truck_items_data.suspension_system,
        suspension_system_photo=truck_items_data.suspension_system_photo,
        tire_chains=truck_items_data.tire_chains,
        tire_chains_photo=truck_items_data.tire_chains_photo,
        tires=truck_items_data.tires,
        tires_photo=truck_items_data.tires_photo,
        transmission=truck_items_data.transmission,
        transmission_photo=truck_items_data.transmission_photo,
        trip_recorder=truck_items_data.trip_recorder,
        trip_recorder_photo=truck_items_data.trip_recorder_photo,
        wheels_and_rims=truck_items_data.wheels_and_rims,
        wheels_and_rims_photo=truck_items_data.wheels_and_rims_photo,
        windows=truck_items_data.windows,
        windows_photo=truck_items_data.windows_photo,
        windshield_wipers=truck_items_data.windshield_wipers,
        windshield_wipers_photo=truck_items_data.windshield_wipers_photo,
        other=truck_items_data.other,
        other_description=truck_items_data.other_description,
        other_photo=truck_items_data.other_photo if hasattr(truck_items_data, "other_photo") else None
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
            brake_connections_photo=trailer_items_data.brake_connections_photo,
            brakes=trailer_items_data.brakes,
            brakes_photo=trailer_items_data.brakes_photo,
            coupling_devices=trailer_items_data.coupling_devices,
            coupling_devices_photo=trailer_items_data.coupling_devices_photo,
            coupling_king_pin=trailer_items_data.coupling_king_pin,
            coupling_king_pin_photo=trailer_items_data.coupling_king_pin_photo,
            doors=trailer_items_data.doors,
            doors_photo=trailer_items_data.doors_photo,
            hitch=trailer_items_data.hitch,
            hitch_photo=trailer_items_data.hitch_photo,
            landing_gear=trailer_items_data.landing_gear,
            landing_gear_photo=trailer_items_data.landing_gear_photo,
            lights_all=trailer_items_data.lights_all,
            lights_all_photo=trailer_items_data.lights_all_photo,
            reflectors_reflective_tape=trailer_items_data.reflectors_reflective_tape,
            reflectors_reflective_tape_photo=trailer_items_data.reflectors_reflective_tape_photo,
            roof=trailer_items_data.roof,
            roof_photo=trailer_items_data.roof_photo,
            suspension_system=trailer_items_data.suspension_system,
            suspension_system_photo=trailer_items_data.suspension_system_photo,
            tarpaulin=trailer_items_data.tarpaulin,
            tarpaulin_photo=trailer_items_data.tarpaulin_photo,
            tires=trailer_items_data.tires,
            tires_photo=trailer_items_data.tires_photo,
            wheels_and_rims=trailer_items_data.wheels_and_rims,
            wheels_and_rims_photo=trailer_items_data.wheels_and_rims_photo,
            other=trailer_items_data.other,
            other_description=trailer_items_data.other_description,
            other_photo=trailer_items_data.other_photo
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
                air_compressor_photo=db_truck_items.air_compressor_photo,
                air_lines=db_truck_items.air_lines,
                air_lines_photo=db_truck_items.air_lines_photo,
                battery=db_truck_items.battery,
                battery_photo=db_truck_items.battery_photo,
                belts_and_hoses=db_truck_items.belts_and_hoses,
                belts_and_hoses_photo=db_truck_items.belts_and_hoses_photo,
                body=db_truck_items.body,
                body_photo=db_truck_items.body_photo,
                brake_accessories=db_truck_items.brake_accessories,
                brake_accessories_photo=db_truck_items.brake_accessories_photo,
                brake_parking=db_truck_items.brake_parking,
                brake_parking_photo=db_truck_items.brake_parking_photo,
                brake_service=db_truck_items.brake_service,
                brake_service_photo=db_truck_items.brake_service_photo,
                clutch=db_truck_items.clutch,
                clutch_photo=db_truck_items.clutch_photo,
                coupling_devices=db_truck_items.coupling_devices,
                coupling_devices_photo=db_truck_items.coupling_devices_photo,
                defroster_heater=db_truck_items.defroster_heater,
                defroster_heater_photo=db_truck_items.defroster_heater_photo,
                drive_line=db_truck_items.drive_line,
                drive_line_photo=db_truck_items.drive_line_photo,
                engine=db_truck_items.engine,
                engine_photo=db_truck_items.engine_photo,
                exhaust=db_truck_items.exhaust,
                exhaust_photo=db_truck_items.exhaust_photo,
                fifth_wheel=db_truck_items.fifth_wheel,
                fifth_wheel_photo=db_truck_items.fifth_wheel_photo,
                fluid_levels=db_truck_items.fluid_levels,
                fluid_levels_photo=db_truck_items.fluid_levels_photo,
                frame_and_assembly=db_truck_items.frame_and_assembly,
                frame_and_assembly_photo=db_truck_items.frame_and_assembly_photo,
                front_axle=db_truck_items.front_axle,
                front_axle_photo=db_truck_items.front_axle_photo,
                fuel_tanks=db_truck_items.fuel_tanks,
                fuel_tanks_photo=db_truck_items.fuel_tanks_photo,
                horn=db_truck_items.horn,
                horn_photo=db_truck_items.horn_photo,
                lights_head_stop=db_truck_items.lights_head_stop,
                lights_head_stop_photo=db_truck_items.lights_head_stop_photo,
                lights_tail_dash=db_truck_items.lights_tail_dash,
                lights_tail_dash_photo=db_truck_items.lights_tail_dash_photo,
                lights_turn_indicators=db_truck_items.lights_turn_indicators,
                lights_turn_indicators_photo=db_truck_items.lights_turn_indicators_photo,
                lights_clearance_marker=db_truck_items.lights_clearance_marker,
                lights_clearance_marker_photo=db_truck_items.lights_clearance_marker_photo,
                mirrors=db_truck_items.mirrors,
                mirrors_photo=db_truck_items.mirrors_photo,
                muffler=db_truck_items.muffler,
                muffler_photo=db_truck_items.muffler_photo,
                oil_pressure=db_truck_items.oil_pressure,
                oil_pressure_photo=db_truck_items.oil_pressure_photo,
                radiator=db_truck_items.radiator,
                radiator_photo=db_truck_items.radiator_photo,
                rear_end=db_truck_items.rear_end,
                rear_end_photo=db_truck_items.rear_end_photo,
                reflectors=db_truck_items.reflectors,
                reflectors_photo=db_truck_items.reflectors_photo,
                safety_fire_extinguisher=db_truck_items.safety_fire_extinguisher,
                safety_fire_extinguisher_photo=db_truck_items.safety_fire_extinguisher_photo,
                safety_flags_flares_fusees=db_truck_items.safety_flags_flares_fusees,
                safety_flags_flares_fusees_photo=db_truck_items.safety_flags_flares_fusees_photo,
                safety_reflective_triangles=db_truck_items.safety_reflective_triangles,
                safety_reflective_triangles_photo=db_truck_items.safety_reflective_triangles_photo,
                safety_spare_bulbs_and_fuses=db_truck_items.safety_spare_bulbs_and_fuses,
                safety_spare_bulbs_and_fuses_photo=db_truck_items.safety_spare_bulbs_and_fuses_photo,
                safety_spare_seal_beam=db_truck_items.safety_spare_seal_beam,
                safety_spare_seal_beam_photo=db_truck_items.safety_spare_seal_beam_photo,
                starter=db_truck_items.starter,
                starter_photo=db_truck_items.starter_photo,
                steering=db_truck_items.steering,
                steering_photo=db_truck_items.steering_photo,
                suspension_system=db_truck_items.suspension_system,
                suspension_system_photo=db_truck_items.suspension_system_photo,
                tire_chains=db_truck_items.tire_chains,
                tire_chains_photo=db_truck_items.tire_chains_photo,
                tires=db_truck_items.tires,
                tires_photo=db_truck_items.tires_photo,
                transmission=db_truck_items.transmission,
                transmission_photo=db_truck_items.transmission_photo,
                trip_recorder=db_truck_items.trip_recorder,
                trip_recorder_photo=db_truck_items.trip_recorder_photo,
                wheels_and_rims=db_truck_items.wheels_and_rims,
                wheels_and_rims_photo=db_truck_items.wheels_and_rims_photo,
                windows=db_truck_items.windows,
                windows_photo=db_truck_items.windows_photo,
                windshield_wipers=db_truck_items.windshield_wipers,
                windshield_wipers_photo=db_truck_items.windshield_wipers_photo,
                other=db_truck_items.other,
                other_description=db_truck_items.other_description,
                other_photo=db_truck_items.other_photo
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
                    brake_connections_photo=db_trailer_items.brake_connections_photo,
                    brakes=db_trailer_items.brakes,
                    brakes_photo=db_trailer_items.brakes_photo,
                    coupling_devices=db_trailer_items.coupling_devices,
                    coupling_devices_photo=db_trailer_items.coupling_devices_photo,
                    coupling_king_pin=db_trailer_items.coupling_king_pin,
                    coupling_king_pin_photo=db_trailer_items.coupling_king_pin_photo,
                    doors=db_trailer_items.doors,
                    doors_photo=db_trailer_items.doors_photo,
                    hitch=db_trailer_items.hitch,
                    hitch_photo=db_trailer_items.hitch_photo,
                    landing_gear=db_trailer_items.landing_gear,
                    landing_gear_photo=db_trailer_items.landing_gear_photo,
                    lights_all=db_trailer_items.lights_all,
                    lights_all_photo=db_trailer_items.lights_all_photo,
                    reflectors_reflective_tape=db_trailer_items.reflectors_reflective_tape,
                    reflectors_reflective_tape_photo=db_trailer_items.reflectors_reflective_tape_photo,
                    roof=db_trailer_items.roof,
                    roof_photo=db_trailer_items.roof_photo,
                    suspension_system=db_trailer_items.suspension_system,
                    suspension_system_photo=db_trailer_items.suspension_system_photo,
                    tarpaulin=db_trailer_items.tarpaulin,
                    tarpaulin_photo=db_trailer_items.tarpaulin_photo,
                    tires=db_trailer_items.tires,
                    tires_photo=db_trailer_items.tires_photo,
                    wheels_and_rims=db_trailer_items.wheels_and_rims,
                    wheels_and_rims_photo=db_trailer_items.wheels_and_rims_photo,
                    other=db_trailer_items.other,
                    other_description=db_trailer_items.other_description,
                    other_photo=db_trailer_items.other_photo
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
            air_compressor_photo=db_truck_items.air_compressor_photo,
            air_lines=db_truck_items.air_lines,
            air_lines_photo=db_truck_items.air_lines_photo,
            battery=db_truck_items.battery,
            battery_photo=db_truck_items.battery_photo,
            belts_and_hoses=db_truck_items.belts_and_hoses,
            belts_and_hoses_photo=db_truck_items.belts_and_hoses_photo,
            body=db_truck_items.body,
            body_photo=db_truck_items.body_photo,
            brake_accessories=db_truck_items.brake_accessories,
            brake_accessories_photo=db_truck_items.brake_accessories_photo,
            brake_parking=db_truck_items.brake_parking,
            brake_parking_photo=db_truck_items.brake_parking_photo,
            brake_service=db_truck_items.brake_service,
            brake_service_photo=db_truck_items.brake_service_photo,
            clutch=db_truck_items.clutch,
            clutch_photo=db_truck_items.clutch_photo,
            coupling_devices=db_truck_items.coupling_devices,
            coupling_devices_photo=db_truck_items.coupling_devices_photo,
            defroster_heater=db_truck_items.defroster_heater,
            defroster_heater_photo=db_truck_items.defroster_heater_photo,
            drive_line=db_truck_items.drive_line,
            drive_line_photo=db_truck_items.drive_line_photo,
            engine=db_truck_items.engine,
            engine_photo=db_truck_items.engine_photo,
            exhaust=db_truck_items.exhaust,
            exhaust_photo=db_truck_items.exhaust_photo,
            fifth_wheel=db_truck_items.fifth_wheel,
            fifth_wheel_photo=db_truck_items.fifth_wheel_photo,
            fluid_levels=db_truck_items.fluid_levels,
            fluid_levels_photo=db_truck_items.fluid_levels_photo,
            frame_and_assembly=db_truck_items.frame_and_assembly,
            frame_and_assembly_photo=db_truck_items.frame_and_assembly_photo,
            front_axle=db_truck_items.front_axle,
            front_axle_photo=db_truck_items.front_axle_photo,
            fuel_tanks=db_truck_items.fuel_tanks,
            fuel_tanks_photo=db_truck_items.fuel_tanks_photo,
            horn=db_truck_items.horn,
            horn_photo=db_truck_items.horn_photo,
            lights_head_stop=db_truck_items.lights_head_stop,
            lights_head_stop_photo=db_truck_items.lights_head_stop_photo,
            lights_tail_dash=db_truck_items.lights_tail_dash,
            lights_tail_dash_photo=db_truck_items.lights_tail_dash_photo,
            lights_turn_indicators=db_truck_items.lights_turn_indicators,
            lights_turn_indicators_photo=db_truck_items.lights_turn_indicators_photo,
            lights_clearance_marker=db_truck_items.lights_clearance_marker,
            lights_clearance_marker_photo=db_truck_items.lights_clearance_marker_photo,
            mirrors=db_truck_items.mirrors,
            mirrors_photo=db_truck_items.mirrors_photo,
            muffler=db_truck_items.muffler,
            muffler_photo=db_truck_items.muffler_photo,
            oil_pressure=db_truck_items.oil_pressure,
            oil_pressure_photo=db_truck_items.oil_pressure_photo,
            radiator=db_truck_items.radiator,
            radiator_photo=db_truck_items.radiator_photo,
            rear_end=db_truck_items.rear_end,
            rear_end_photo=db_truck_items.rear_end_photo,
            reflectors=db_truck_items.reflectors,
            reflectors_photo=db_truck_items.reflectors_photo,
            safety_fire_extinguisher=db_truck_items.safety_fire_extinguisher,
            safety_fire_extinguisher_photo=db_truck_items.safety_fire_extinguisher_photo,
            safety_flags_flares_fusees=db_truck_items.safety_flags_flares_fusees,
            safety_flags_flares_fusees_photo=db_truck_items.safety_flags_flares_fusees_photo,
            safety_reflective_triangles=db_truck_items.safety_reflective_triangles,
            safety_reflective_triangles_photo=db_truck_items.safety_reflective_triangles_photo,
            safety_spare_bulbs_and_fuses=db_truck_items.safety_spare_bulbs_and_fuses,
            safety_spare_bulbs_and_fuses_photo=db_truck_items.safety_spare_bulbs_and_fuses_photo,
            safety_spare_seal_beam=db_truck_items.safety_spare_seal_beam,
            safety_spare_seal_beam_photo=db_truck_items.safety_spare_seal_beam_photo,
            starter=db_truck_items.starter,
            starter_photo=db_truck_items.starter_photo,
            steering=db_truck_items.steering,
            steering_photo=db_truck_items.steering_photo,
            suspension_system=db_truck_items.suspension_system,
            suspension_system_photo=db_truck_items.suspension_system_photo,
            tire_chains=db_truck_items.tire_chains,
            tire_chains_photo=db_truck_items.tire_chains_photo,
            tires=db_truck_items.tires,
            tires_photo=db_truck_items.tires_photo,
            transmission=db_truck_items.transmission,
            transmission_photo=db_truck_items.transmission_photo,
            trip_recorder=db_truck_items.trip_recorder,
            trip_recorder_photo=db_truck_items.trip_recorder_photo,
            wheels_and_rims=db_truck_items.wheels_and_rims,
            wheels_and_rims_photo=db_truck_items.wheels_and_rims_photo,
            windows=db_truck_items.windows,
            windows_photo=db_truck_items.windows_photo,
            windshield_wipers=db_truck_items.windshield_wipers,
            windshield_wipers_photo=db_truck_items.windshield_wipers_photo,
            other=db_truck_items.other,
            other_description=db_truck_items.other_description,
            other_photo=db_truck_items.other_photo
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
                brake_connections_photo=db_trailer_items.brake_connections_photo,
                brakes=db_trailer_items.brakes,
                brakes_photo=db_trailer_items.brakes_photo,
                coupling_devices=db_trailer_items.coupling_devices,
                coupling_devices_photo=db_trailer_items.coupling_devices_photo,
                coupling_king_pin=db_trailer_items.coupling_king_pin,
                coupling_king_pin_photo=db_trailer_items.coupling_king_pin_photo,
                doors=db_trailer_items.doors,
                doors_photo=db_trailer_items.doors_photo,
                hitch=db_trailer_items.hitch,
                hitch_photo=db_trailer_items.hitch_photo,
                landing_gear=db_trailer_items.landing_gear,
                landing_gear_photo=db_trailer_items.landing_gear_photo,
                lights_all=db_trailer_items.lights_all,
                lights_all_photo=db_trailer_items.lights_all_photo,
                reflectors_reflective_tape=db_trailer_items.reflectors_reflective_tape,
                reflectors_reflective_tape_photo=db_trailer_items.reflectors_reflective_tape_photo,
                roof=db_trailer_items.roof,
                roof_photo=db_trailer_items.roof_photo,
                suspension_system=db_trailer_items.suspension_system,
                suspension_system_photo=db_trailer_items.suspension_system_photo,
                tarpaulin=db_trailer_items.tarpaulin,
                tarpaulin_photo=db_trailer_items.tarpaulin_photo,
                tires=db_trailer_items.tires,
                tires_photo=db_trailer_items.tires_photo,
                wheels_and_rims=db_trailer_items.wheels_and_rims,
                wheels_and_rims_photo=db_trailer_items.wheels_and_rims_photo,
                other=db_trailer_items.other,
                other_description=db_trailer_items.other_description,
                other_photo=db_trailer_items.other_photo
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
        db_truck_items.air_compressor_photo = t_items.air_compressor_photo

        db_truck_items.air_lines = t_items.air_lines
        db_truck_items.air_lines_photo = t_items.air_lines_photo

        db_truck_items.battery = t_items.battery
        db_truck_items.battery_photo = t_items.battery_photo

        db_truck_items.belts_and_hoses = t_items.belts_and_hoses
        db_truck_items.belts_and_hoses_photo = t_items.belts_and_hoses_photo

        db_truck_items.body = t_items.body
        db_truck_items.body_photo = t_items.body_photo

        db_truck_items.brake_accessories = t_items.brake_accessories
        db_truck_items.brake_accessories_photo = t_items.brake_accessories_photo

        db_truck_items.brake_parking = t_items.brake_parking
        db_truck_items.brake_parking_photo = t_items.brake_parking_photo

        db_truck_items.brake_service = t_items.brake_service
        db_truck_items.brake_service_photo = t_items.brake_service_photo

        db_truck_items.clutch = t_items.clutch
        db_truck_items.clutch_photo = t_items.clutch_photo

        db_truck_items.coupling_devices = t_items.coupling_devices
        db_truck_items.coupling_devices_photo = t_items.coupling_devices_photo

        db_truck_items.defroster_heater = t_items.defroster_heater
        db_truck_items.defroster_heater_photo = t_items.defroster_heater_photo

        db_truck_items.drive_line = t_items.drive_line
        db_truck_items.drive_line_photo = t_items.drive_line_photo

        db_truck_items.engine = t_items.engine
        db_truck_items.engine_photo = t_items.engine_photo

        db_truck_items.exhaust = t_items.exhaust
        db_truck_items.exhaust_photo = t_items.exhaust_photo

        db_truck_items.fifth_wheel = t_items.fifth_wheel
        db_truck_items.fifth_wheel_photo = t_items.fifth_wheel_photo

        db_truck_items.fluid_levels = t_items.fluid_levels
        db_truck_items.fluid_levels_photo = t_items.fluid_levels_photo

        db_truck_items.frame_and_assembly = t_items.frame_and_assembly
        db_truck_items.frame_and_assembly_photo = t_items.frame_and_assembly_photo

        db_truck_items.front_axle = t_items.front_axle
        db_truck_items.front_axle_photo = t_items.front_axle_photo

        db_truck_items.fuel_tanks = t_items.fuel_tanks
        db_truck_items.fuel_tanks_photo = t_items.fuel_tanks_photo

        db_truck_items.horn = t_items.horn
        db_truck_items.horn_photo = t_items.horn_photo

        db_truck_items.lights_head_stop = t_items.lights_head_stop
        db_truck_items.lights_head_stop_photo = t_items.lights_head_stop_photo

        db_truck_items.lights_tail_dash = t_items.lights_tail_dash
        db_truck_items.lights_tail_dash_photo = t_items.lights_tail_dash_photo

        db_truck_items.lights_turn_indicators = t_items.lights_turn_indicators
        db_truck_items.lights_turn_indicators_photo = t_items.lights_turn_indicators_photo

        db_truck_items.lights_clearance_marker = t_items.lights_clearance_marker
        db_truck_items.lights_clearance_marker_photo = t_items.lights_clearance_marker_photo

        db_truck_items.mirrors = t_items.mirrors
        db_truck_items.mirrors_photo = t_items.mirrors_photo

        db_truck_items.muffler = t_items.muffler
        db_truck_items.muffler_photo = t_items.muffler_photo

        db_truck_items.oil_pressure = t_items.oil_pressure
        db_truck_items.oil_pressure_photo = t_items.oil_pressure_photo

        db_truck_items.radiator = t_items.radiator
        db_truck_items.radiator_photo = t_items.radiator_photo

        db_truck_items.rear_end = t_items.rear_end
        db_truck_items.rear_end_photo = t_items.rear_end_photo

        db_truck_items.reflectors = t_items.reflectors
        db_truck_items.reflectors_photo = t_items.reflectors_photo

        db_truck_items.safety_fire_extinguisher = t_items.safety_fire_extinguisher
        db_truck_items.safety_fire_extinguisher_photo = t_items.safety_fire_extinguisher_photo

        db_truck_items.safety_flags_flares_fusees = t_items.safety_flags_flares_fusees
        db_truck_items.safety_flags_flares_fusees_photo = t_items.safety_flags_flares_fusees_photo

        db_truck_items.safety_reflective_triangles = t_items.safety_reflective_triangles
        db_truck_items.safety_reflective_triangles_photo = t_items.safety_reflective_triangles_photo

        db_truck_items.safety_spare_bulbs_and_fuses = t_items.safety_spare_bulbs_and_fuses
        db_truck_items.safety_spare_bulbs_and_fuses_photo = t_items.safety_spare_bulbs_and_fuses_photo

        db_truck_items.safety_spare_seal_beam = t_items.safety_spare_seal_beam
        db_truck_items.safety_spare_seal_beam_photo = t_items.safety_spare_seal_beam_photo

        db_truck_items.starter = t_items.starter
        db_truck_items.starter_photo = t_items.starter_photo

        db_truck_items.steering = t_items.steering
        db_truck_items.steering_photo = t_items.steering_photo

        db_truck_items.suspension_system = t_items.suspension_system
        db_truck_items.suspension_system_photo = t_items.suspension_system_photo

        db_truck_items.tire_chains = t_items.tire_chains
        db_truck_items.tire_chains_photo = t_items.tire_chains_photo

        db_truck_items.tires = t_items.tires
        db_truck_items.tires_photo = t_items.tires_photo

        db_truck_items.transmission = t_items.transmission
        db_truck_items.transmission_photo = t_items.transmission_photo

        db_truck_items.trip_recorder = t_items.trip_recorder
        db_truck_items.trip_recorder_photo = t_items.trip_recorder_photo

        db_truck_items.wheels_and_rims = t_items.wheels_and_rims
        db_truck_items.wheels_and_rims_photo = t_items.wheels_and_rims_photo

        db_truck_items.windows = t_items.windows
        db_truck_items.windows_photo = t_items.windows_photo

        db_truck_items.windshield_wipers = t_items.windshield_wipers
        db_truck_items.windshield_wipers_photo = t_items.windshield_wipers_photo

        db_truck_items.other = t_items.other
        db_truck_items.other_description = t_items.other_description
        db_truck_items.other_photo = t_items.other_photo

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
                db_trailer_items.brake_connections_photo = it.brake_connections_photo

                db_trailer_items.brakes = it.brakes
                db_trailer_items.brakes_photo = it.brakes_photo

                db_trailer_items.coupling_devices = it.coupling_devices
                db_trailer_items.coupling_devices_photo = it.coupling_devices_photo

                db_trailer_items.coupling_king_pin = it.coupling_king_pin
                db_trailer_items.coupling_king_pin_photo = it.coupling_king_pin_photo

                db_trailer_items.doors = it.doors
                db_trailer_items.doors_photo = it.doors_photo

                db_trailer_items.hitch = it.hitch
                db_trailer_items.hitch_photo = it.hitch_photo

                db_trailer_items.landing_gear = it.landing_gear
                db_trailer_items.landing_gear_photo = it.landing_gear_photo

                db_trailer_items.lights_all = it.lights_all
                db_trailer_items.lights_all_photo = it.lights_all_photo

                db_trailer_items.reflectors_reflective_tape = it.reflectors_reflective_tape
                db_trailer_items.reflectors_reflective_tape_photo = it.reflectors_reflective_tape_photo

                db_trailer_items.roof = it.roof
                db_trailer_items.roof_photo = it.roof_photo

                db_trailer_items.suspension_system = it.suspension_system
                db_trailer_items.suspension_system_photo = it.suspension_system_photo

                db_trailer_items.tarpaulin = it.tarpaulin
                db_trailer_items.tarpaulin_photo = it.tarpaulin_photo

                db_trailer_items.tires = it.tires
                db_trailer_items.tires_photo = it.tires_photo

                db_trailer_items.wheels_and_rims = it.wheels_and_rims
                db_trailer_items.wheels_and_rims_photo = it.wheels_and_rims_photo

                db_trailer_items.other = it.other
                db_trailer_items.other_description = it.other_description
                db_trailer_items.other_photo = it.other_photo
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

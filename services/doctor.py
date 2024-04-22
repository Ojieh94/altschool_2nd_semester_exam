
from fastapi import HTTPException
from schema.doctor import DoctorsAvailabilityStatus, DoctorsEdit, doctors, Doctors, DoctorsCreate


class DoctorService:

    @staticmethod
    def parse_doctors(doctor_data):
        data = []
        for doctor in doctor_data:
            data.append(doctors[doctor])
        return data

    @staticmethod
    def get_doctor_by_id(doctor_id: int):
        doctor = doctors.get(doctor_id)
        if not doctor:
            raise HTTPException(
                detail='Doctor does not exist.', status_code=404)
        return doctor

    @staticmethod
    def create_doctor(payload: DoctorsCreate):
        id = len(doctors)
        doctor = Doctors(
            id=id,
            **payload.model_dump()
        )
        doctors[id] = doctor
        return doctor

    @staticmethod
    def edit_doctor(doctor_id: int, payload: DoctorsEdit):
        doctor = doctors.get(doctor_id)
        if not doctor:
            raise HTTPException(
                detail='Doctor does not exist.', status_code=404)

        if payload.name is not None:
            doctor.name = payload.name
        if payload.specialization is not None:
            doctor.specialization = payload.specialization
        if payload.phone is not None:
            doctor.phone = payload.phone
        return doctor

    @staticmethod
    def delete_doctor(doctor_id: int):
        doctor = doctors.get(doctor_id)
        if not doctor:
            raise HTTPException(
                detail='Doctor does not exist.', status_code=404)
        del doctors[doctor_id]

    @staticmethod
    def set_doctor_availability_status(doctor_id: int):
        doctor = doctors.get(doctor_id)
        if not doctor:
            raise HTTPException(
                detail='Doctor does not exist.', status_code=404)

        if doctor.is_available == DoctorsAvailabilityStatus.AVAILABLE:
            doctor.is_available = DoctorsAvailabilityStatus.UNAVAILABLE
        else:
            doctor.is_available = DoctorsAvailabilityStatus.AVAILABLE

        return doctor

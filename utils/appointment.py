from fastapi import HTTPException
from schema.doctor import DoctorsAvailabilityStatus, doctors
from schema.appointment import AppointmentsStatus, appointments



class AppointmentHelpers:

    @staticmethod
    def appoint_doctor_to_patient():
        for doctor_id, doctor in doctors.items():
            if doctor.is_available == DoctorsAvailabilityStatus.AVAILABLE:
                doctor.is_available = DoctorsAvailabilityStatus.UNAVAILABLE
                return doctors[doctor_id]
        raise HTTPException(
            detail='No doctor available', status_code=404)

    @staticmethod
    def get_appointment_by_id(appointment_id: int):
        appointment = appointments.get(appointment_id)
        if not appointment:
            raise HTTPException(
                detail='Appointment not found', status_code=404)
        return appointment

    @staticmethod
    def check_pending_appointments(patient):
        for key, appointment in appointments.items():
            if patient == appointment.patient and appointment.status == AppointmentsStatus.PENDING:
                raise HTTPException(
                    detail='Patient has pending appointment. Please complete pending appointment', status_code=200)

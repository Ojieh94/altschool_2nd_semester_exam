from fastapi import HTTPException


from schema.appointment import Appointments, AppointmentsCreateEdit, AppointmentsStatus, appointments
from schema.doctor import Doctors
from schema.patient import patients
from utils.appointment import AppointmentHelpers
from utils.doctor import DoctorHelpers


class AppointmentService:

    @staticmethod
    def parse_appointments(appointment_data):
        data = []
        for appointment in appointment_data:
            data.append(appointments[appointment])
        return data

    @staticmethod
    def get_appointment_by_id(appointment_id: int):
        appointment = AppointmentHelpers.get_appointment_by_id(appointment_id)
        return appointment

    @staticmethod
    def create_appointment(payload: AppointmentsCreateEdit):
        id = len(appointments)
        patient = patients.get(payload.patient_id)
        if not patient:
            raise HTTPException(detail='Patient not found', status_code=404)

        AppointmentHelpers.check_pending_appointments(patient)

        doctor: Doctors = AppointmentHelpers.appoint_doctor_to_patient()

        appointment = Appointments(
            id=id,
            patient=patient,
            doctor=doctor,
            date=payload.date
        )
        appointments[id] = appointment
        return appointment

    @staticmethod
    def edit_appointment(appointment_id: int, payload: AppointmentsCreateEdit):
        appointment = AppointmentHelpers.get_appointment_by_id(appointment_id)

     # Check if the patient_id in the payload is already associated with another appointment

        for existing_appointment in appointments.values():
            if existing_appointment.id != appointment_id and existing_appointment.patient.id == payload.patient_id:
                raise HTTPException(
                    detail=f"Patient already has an existing appointment.",
                    status_code=400
                )

        appointment.patient = patients.get(payload.patient_id)
        if appointment.patient is None:
            raise HTTPException(
                detail='Patient not found.', status_code=404
            )

        appointment.date = payload.date
        return appointment

    @staticmethod
    def delete_appointment(appointment_id: int):
        appointment = AppointmentHelpers.get_appointment_by_id(appointment_id)

        DoctorHelpers.set_doctor_availability_true(appointment)

        del appointments[appointment_id]

    @staticmethod
    def complete_appointment(appointment_id: int):
        appointment = AppointmentHelpers.get_appointment_by_id(appointment_id)
        appointment.status = AppointmentsStatus.COMPLETED

        DoctorHelpers.set_doctor_availability_true(appointment)

        return appointment

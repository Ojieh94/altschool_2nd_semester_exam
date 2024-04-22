from schema.doctor import DoctorsAvailabilityStatus, doctors


class DoctorHelpers:
   @staticmethod
   def set_doctor_availability_true(appointment):
       for doc, doctor in doctors.items():
            if doctor == appointment.doctor:
                doctor.is_available = DoctorsAvailabilityStatus.AVAILABLE
       return appointment

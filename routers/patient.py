from fastapi import APIRouter
from schema.patient import PatientsCreate, patients, PatientsEdit
from services.patient import PatientService

patient_router = APIRouter()


@patient_router.get('/', status_code=200)
def get_patient():
    data = PatientService.parse_patients(patient_data=patients)
    return {'message': 'Successful', 'data': data}


@patient_router.get('/{patient_id}', status_code=200)
def get_patient_by_id(patient_id: int):
    data = PatientService.get_patient_by_id(patient_id)
    return {'message': 'Successful', 'data': data}


@patient_router.post('/', status_code=201)
def create_patient(payload: PatientsCreate):
    data = PatientService.create_patient(payload)
    return {'message': 'Patient created successfully', 'data': data}


@patient_router.put('/{patient_id}', status_code=200)
def edit_patient(patient_id: int, payload: PatientsEdit):
    data = PatientService.edit_patient(patient_id, payload)
    return {'message': 'Patient updated successfully', 'data': data}


@patient_router.delete('/{patient_id}', status_code=200)
def delete_patient(patient_id: int):
    PatientService.delete_patient(patient_id)
    return {'message': 'Patient deleted successfully'}

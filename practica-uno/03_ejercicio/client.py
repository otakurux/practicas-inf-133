import requests
import json

base_url = 'http://localhost:8000'

def get_pacientes():
    endpoint = '/pacientes'
    response = requests.get(base_url + endpoint)
    return response.json()

def buscar_paciente_por_ci(ci):
    endpoint = f'/pacientes?ci={ci}'
    response = requests.get(base_url + endpoint)
    return response.json()

def listar_pacientes_por_diagnostico(diagnostico):
    endpoint = f'/pacientes?diagnostico={diagnostico}'
    response = requests.get(base_url + endpoint)
    return response.json()

def listar_pacientes_por_doctor(doctor):
    endpoint = f'/pacientes?doctor={doctor}'
    response = requests.get(base_url + endpoint)
    return response.json()

def crear_paciente(data):
    endpoint = '/pacientes'
    response = requests.post(base_url + endpoint, json=data)
    return response.json()

def actualizar_paciente(ci, data):
    endpoint = f'/pacientes/{ci}'
    response = requests.put(base_url + endpoint, json=data)
    return response.json()

def eliminar_paciente(ci):
    endpoint = f'/pacientes/{ci}'
    response = requests.delete(base_url + endpoint)
    return response.json()

if __name__ == '__main__':
    print("Lista de todos los pacientes:")
    print(get_pacientes())

    ci_buscar = '1234567'
    print(f"\nPaciente con CI {ci_buscar}:")
    print(buscar_paciente_por_ci(ci_buscar))

    diagnostico_listar = 'Diabetes'
    print(f"\nPacientes con diagnóstico {diagnostico_listar}:")
    print(listar_pacientes_por_diagnostico(diagnostico_listar))

    doctor_listar = 'Dr. Martínez'
    print(f"\nPacientes atendidos por el doctor {doctor_listar}:")
    print(listar_pacientes_por_doctor(doctor_listar))

    nuevo_paciente = {
        "ci": "4567890",
        "nombre": "Luis",
        "apellido": "Ramirez",
        "edad": 40,
        "genero": "Masculino",
        "diagnostico": "Asma",
        "doctor": "Dr. Gómez"
    }
    print(f"\nCreando nuevo paciente:")
    print(crear_paciente(nuevo_paciente))

    paciente_actualizar = {
        "nombre": "Luisa",
        "apellido": "Ramirez",
        "edad": 45
    }
    ci_actualizar = '4567890'
    print(f"\nActualizando información del paciente con CI {ci_actualizar}:")
    print(actualizar_paciente(ci_actualizar, paciente_actualizar))

    ci_eliminar = '3456789'
    print(f"\nEliminando paciente con CI {ci_eliminar}:")
    print(eliminar_paciente(ci_eliminar))

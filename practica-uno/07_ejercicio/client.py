import requests
import json

def crear_partida(elemento):
    url = "http://localhost:8000/partidas"
    payload = {"elemento": elemento}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        partida = response.json()
        print("Partida creada exitosamente:")
        print(partida)
    else:
        print("Error al crear la partida")

def obtener_partidas():
    url = "http://localhost:8000/partidas"

    response = requests.get(url)
    if response.status_code == 200:
        partidas = response.json()
        print("Listado de partidas:")
        print(partidas)
    else:
        print("Error al obtener las partidas")

def obtener_partidas_por_resultado(resultado):
    url = f"http://localhost:8000/partidas?resultado={resultado}"

    response = requests.get(url)
    if response.status_code == 200:
        partidas = response.json()
        print(f"Listado de partidas con resultado '{resultado}':")
        print(partidas)
    else:
        print("Error al obtener las partidas por resultado")

crear_partida("piedra")
crear_partida("tijera")
obtener_partidas()
obtener_partidas_por_resultado("ganó")

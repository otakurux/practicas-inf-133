import requests
import json

base_url = "http://localhost:8000"

def crear_mensaje(contenido):
    url = f"{base_url}/mensajes"
    data = {"contenido": contenido}
    response = requests.post(url, json=data)
    return response.json()

def obtener_mensajes():
    url = f"{base_url}/mensajes"
    response = requests.get(url)
    return response.json()

def buscar_mensaje_por_id(mensaje_id):
    url = f"{base_url}/mensajes/{mensaje_id}"
    response = requests.get(url)
    return response.json()

def actualizar_mensaje(mensaje_id, nuevo_contenido):
    url = f"{base_url}/mensajes/{mensaje_id}"
    data = {"contenido": nuevo_contenido}
    response = requests.put(url, json=data)
    return response.json()

def eliminar_mensaje(mensaje_id):
    url = f"{base_url}/mensajes/{mensaje_id}"
    response = requests.delete(url)
    return response.json()

mensaje_creado = crear_mensaje("Hola, este es un mensaje de prueba")
print("Mensaje creado:", mensaje_creado)

mensajes = obtener_mensajes()
print("Todos los mensajes:", mensajes)

mensaje_encontrado = buscar_mensaje_por_id(1)
print("Mensaje encontrado:", mensaje_encontrado)

mensaje_actualizado = actualizar_mensaje(1, "Este mensaje ha sido actualizado")
print("Mensaje actualizado:", mensaje_actualizado)

mensaje_eliminado = eliminar_mensaje(1)
print("Mensaje eliminado:", mensaje_eliminado)

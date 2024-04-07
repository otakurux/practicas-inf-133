import requests

url = "http://localhost:8000/"

# Listar todos los animales
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print("Listar todos los animales:")
print(get_response.text)

# Crear un animal
ruta_post = url + "animales"
nuevo_animal = {
    "nombre": "Elefante",
    "especie": "Loxodonta africana",
    "genero": "Macho",
    "edad": 15,
    "peso": 5000,
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print("\nCrear un animal:")
print(post_response.text)

# Buscar animales por especie
ruta_get_especie = url + "animales?especie=Panthera leo"
get_response_especie = requests.request(method="GET", url=ruta_get_especie)
print("\nBuscar animales por especie:")
print(get_response_especie.text)

# Buscar animales por genero
ruta_get_genero = url + "animales?genero=Macho"
get_response_genero = requests.request(method="GET", url=ruta_get_genero)
print("\nBuscar animales por género:")
print(get_response_genero.text)

# Actualizar la información de un animal
datos_actualizados = {
    "especie": "Panthera leo",
    "edad": 6,
}
id_animal_actualizar = 1
ruta_put = f"{url}/animales/{id_animal_actualizar}"
put_response = requests.request(method="PUT", url=ruta_put, json=datos_actualizados)
print("\nActualizar la información de un animal:")
print(put_response.text)

# Eliminar un animal
id_animal_eliminar = 2
ruta_delete = f"{url}/animales/{id_animal_eliminar}"
delete_response = requests.request(method="DELETE", url=ruta_delete)
print("\nEliminar un animal:")
print(delete_response.text)
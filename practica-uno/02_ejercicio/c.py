import requests

URL = 'http://localhost:8000/graphql'

query_todas_las_plantas = """
{
  plantas {
    id
    nombre
    especie
    cantidad
  }
}
"""

def query_planta_por_id(id):
    return f"""
    {{
        plantaPorId(id: {id}) {{
            nombre
        }}
    }}
    """

def mutation_crear_planta(nombre, especie, cantidad):
    return f"""
    mutation {{
        crearPlanta(nombre: "{nombre}", especie: "{especie}", cantidad: {cantidad}) {{
            planta {{
                id
                nombre
                especie
                cantidad
            }}
        }}
    }}
    """

def mutation_eliminar_planta(id):
    return f"""
    mutation {{
        deletePlanta(id: {id}) {{
            planta {{
                id
                nombre
                especie
                cantidad
            }}
        }}
    }}
    """

def send_request(query):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL, headers=headers, json={'query': query})
    return response.json()

response_plantas = send_request(query_todas_las_plantas)
print("Todas las plantas:")
print(response_plantas)

response_planta_id_2 = send_request(query_planta_por_id(2))
print("\nPlanta por ID (ID=2):")
print(response_planta_id_2)

response_crear_planta = send_request(mutation_crear_planta("Angel", "Gomez", 5))
print("\nNueva planta creada:")
print(response_crear_planta)

response_eliminar_planta = send_request(mutation_eliminar_planta(3))
print("\nPlanta eliminada:")
print(response_eliminar_planta)

response_plantas_despues = send_request(query_todas_las_plantas)
print("\nTodas las plantas después de las operaciones:")
print(response_plantas_despues)

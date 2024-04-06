import requests
import json

# URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

# Consulta GraphQL para obtener todas las plantas
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

mutation_crear_planta = """
mutation {
  crearPlanta(nombre: "Orquidea", especie: "Phalaenopsis", cantidad: 5) {
    planta {
      id
      nombre
      especie
      cantidad
    }
  }
}
"""

mutation_actualizar_planta = """
mutation {
  actualizarPlanta(id: 2, cantidad: 20) {
    planta {
      id
      nombre
      especie
      cantidad
    }
  }
}
"""

def send_request(query):
  response = requests.post(url, json={'query':query})
  return response.text
    # headers = {'Content-Type': 'application/json'}
    # response = requests.post(url, headers=headers, data=json.dumps({'query': query}))
    # return response.json()

response_plantas = send_request(query_todas_las_plantas)
print("Todas las plantas:")
print(response_plantas)
# print(json.dumps(response_plantas, indent=2))

response_crear_planta = send_request(mutation_crear_planta)
print("\nNueva planta creada:")
print(response_crear_planta)
# print(json.dumps(response_crear_planta, indent=2))

response_actualizar_planta = send_request(mutation_actualizar_planta)
print("\nPlanta actualizada:")
print(response_actualizar_planta)
# print(json.dumps(response_actualizar_planta, indent=2))

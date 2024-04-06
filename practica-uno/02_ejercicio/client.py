import requests
import json

url = 'http://localhost:8000/graphql'

def send_request(query):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json={'query': query})
    return response.json()

def query_plantas_por_especie(especie):
    return f"""
    {{
      plantasPorEspecie(especie: "{especie}") {{
        id
        nombreComun
        especie
        edad
        altura
        frutos
      }}
    }}
    """

def mutation_actualizar_planta(id, nombre_comun, especie, edad, altura, frutos):
    return f"""
    mutation {{
      actualizarPlanta(
        id: {id},
        nombreComun: "{nombre_comun}",
        especie: "{especie}",
        edad: {edad},
        altura: {altura},
        frutos: {frutos}
      ) {{
        planta {{
          id
          nombreComun
          especie
          edad
          altura
          frutos
        }}
      }}
    }}
    """

query_todas_las_plantas = """
{
  todasLasPlantas {
    id
    nombreComun
    especie
    edad
    altura
    frutos
  }
}
"""

query_planta_por_id = """
{
  plantaPorId(id: 2) {
    nombreComun
    especie
    edad
    altura
    frutos
  }
}
"""

mutation_crear_planta = """
mutation {
  crearPlanta(
    nombreComun: "Orquídea",
    especie: "Orchidaceae",
    edad: 24,
    altura: 30,
    frutos: false
  ) {
    planta {
      id
      nombreComun
      especie
      edad
      altura
      frutos
    }
  }
}
"""

mutation_eliminar_planta = """
mutation {
  eliminarPlanta(id: 3) {
    planta {
      id
      nombreComun
      especie
      edad
      altura
      frutos
    }
  }
}
"""

query_plantas_con_frutos = """
{
  plantasConFrutos {
    id
    nombreComun
    especie
    edad
    altura
    frutos
  }
}
"""

response_crear_planta = send_request(mutation_crear_planta)
print("\nNueva planta creada:")
print(response_crear_planta)

response_plantas = send_request(query_todas_las_plantas)
print("\nTodas las plantas:")
print(response_plantas)

response_plantas_rosa = send_request(query_plantas_por_especie("Rosa"))
print("\nTodas las plantas de la especie 'Rosa':")
print(response_plantas_rosa)

response_plantas_con_frutos = send_request(query_plantas_con_frutos)
print("\nPlantas que tienen frutos:")
print(response_plantas_con_frutos)

response_actualizar_planta = send_request(mutation_actualizar_planta(1, "Rosa Roja", "Rosa gallica", 15, 55, True))
print("\nPlanta actualizada:")
print(response_actualizar_planta)

response_eliminar_planta = send_request(mutation_eliminar_planta)
print("\nPlanta eliminada:")
print(response_eliminar_planta)

response_plantas_despues = send_request(query_todas_las_plantas)
print("\nTodas las plantas despues de las operaciones:")
print(response_plantas_despues)

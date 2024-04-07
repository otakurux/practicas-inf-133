from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci": "1234567",
        "nombre": "Ana",
        "apellido": "Gonzalez",
        "edad": 35,
        "genero": "Femenino",
        "diagnostico": "Hipertension",
        "doctor": "Dr. Martínez",
    },
    {
        "ci": "2345678",
        "nombre": "Juan",
        "apellido": "Perez",
        "edad": 45,
        "genero": "Masculino",
        "diagnostico": "Diabetes",
        "doctor": "Dra. Rodríguez",
    },
    {
        "ci": "3456789",
        "nombre": "Maria",
        "apellido": "Lopez",
        "edad": 28,
        "genero": "Femenino",
        "diagnostico": "Asma",
        "doctor": "Dr. Gomez",
    },
]


class PacientesService:
    @staticmethod
    def actualizar_paciente(ci, data):
        paciente = PacientesService.find_paciente(ci)
        if paciente:
            paciente.update(data)
            return paciente
        else:
            return None

    @staticmethod
    def eliminar_paciente(ci):
        paciente = PacientesService.find_paciente(ci)
        if paciente:
            pacientes.remove(paciente)
            return paciente
        else:
            return None

    @staticmethod
    def find_paciente(ci):
        return next((paciente for paciente in pacientes if paciente["ci"] == ci), None)

    @staticmethod
    def validar_ci_unica(ci):
        return not any(paciente["ci"] == ci for paciente in pacientes)

    @staticmethod
    def crear_paciente(data):
        if data != None:
            if PacientesService.validar_ci_unica(data["ci"]):
                pacientes.append(data)
                return data
            else:
                return None
        else:
            return None


    @staticmethod
    def listar_pacientes():
        return pacientes

    @staticmethod
    def buscar_paciente_por_ci(ci):
        paciente = next((paciente for paciente in pacientes if paciente["ci"] == ci), None)
        return [paciente] if paciente else []

    @staticmethod
    def listar_pacientes_por_diagnostico(diagnostico):
        return [paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico]

    @staticmethod
    def listar_pacientes_por_doctor(doctor):
        return [paciente for paciente in pacientes if paciente["doctor"] == doctor]



class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            if "ci" in query_params:
                ci = query_params["ci"][0]
                pacientes_encontrados = PacientesService.buscar_paciente_por_ci(ci)
                HTTPResponseHandler.handle_response(self, 200, pacientes_encontrados)
            elif "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_diagnostico = PacientesService.listar_pacientes_por_diagnostico(diagnostico)
                HTTPResponseHandler.handle_response(self, 200, pacientes_diagnostico)
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_doctor = PacientesService.listar_pacientes_por_doctor(doctor)
                HTTPResponseHandler.handle_response(self, 200, pacientes_doctor)
            else:
                pacientes_todos = PacientesService.listar_pacientes()
                HTTPResponseHandler.handle_response(self, 200, pacientes_todos)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            nuevo_paciente = PacientesService.crear_paciente(data)
            if nuevo_paciente:
                HTTPResponseHandler.handle_response(self, 201, nuevo_paciente)
            else:
                HTTPResponseHandler.handle_response(
                    self, 400, {"error": "El CI del paciente ya existe"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"error": "Ruta no existente"}
            )

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/pacientes/"):
            ci = parsed_path.path.split("/")[-1]
            data = self.read_data()
            pacientes_actualizados = PacientesService.actualizar_paciente(ci, data)
            if pacientes_actualizados:
                HTTPResponseHandler.handle_response(self, 200, pacientes_actualizados)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"error": "Ruta no existente"}
            )

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/pacientes/"):
            ci = parsed_path.path.split("/")[-1]
            pacientes_eliminados = PacientesService.eliminar_paciente(ci)
            if pacientes_eliminados:
                HTTPResponseHandler.handle_response(self, 200, pacientes_eliminados)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"error": "Ruta no existente"}
            )
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()

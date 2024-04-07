from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Paciente:
    def __init__(self, ci, nombre, apellido, edad, genero, diagnostico, doctor):
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.genero = genero
        self.diagnostico = diagnostico
        self.doctor = doctor

class PacienteBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.paciente = {}

    def set_ci(self, ci):
        self.paciente['ci'] = ci
        return self

    def set_nombre(self, nombre):
        self.paciente['nombre'] = nombre
        return self

    def set_apellido(self, apellido):
        self.paciente['apellido'] = apellido
        return self

    def set_edad(self, edad):
        self.paciente['edad'] = edad
        return self

    def set_genero(self, genero):
        self.paciente['genero'] = genero
        return self

    def set_diagnostico(self, diagnostico):
        self.paciente['diagnostico'] = diagnostico
        return self

    def set_doctor(self, doctor):
        self.paciente['doctor'] = doctor
        return self

    def build(self):
        paciente = self.paciente
        self.reset()
        return paciente

pacientes = [
    Paciente("1234567", "Ana", "Gonzalez", 35, "Femenino", "Hipertension", "Dr. Martínez"),
    Paciente("2345678", "Juan", "Perez", 45, "Masculino", "Diabetes", "Dra. Rodríguez"),
    Paciente("3456789", "Maria", "Lopez", 28, "Femenino", "Asma", "Dr. Gomez"),
]

def json_a_paciente(data_json):
    paciente = Paciente(
        ci=data_json["ci"],
        nombre=data_json["nombre"],
        apellido=data_json["apellido"],
        edad=data_json["edad"],
        genero=data_json["genero"],
        diagnostico=data_json["diagnostico"],
        doctor=data_json["doctor"]
    )
    return paciente


class PacientesService:
    @staticmethod
    def find_paciente(ci):
        return next((paciente for paciente in pacientes if paciente.ci == ci), None)

    @staticmethod
    def filter_pacientes_by_diagnostico(diagnostico):
        return [paciente.__dict__ for paciente in pacientes if paciente.diagnostico == diagnostico]

    @staticmethod
    def pacientes_list():
        return [paciente.__dict__ for paciente in pacientes]

    @staticmethod
    def update_paciente(ci, data):
        paciente = PacientesService.find_paciente(ci)
        if paciente:
            for key, value in data.items():
                if hasattr(paciente, key):
                    setattr(paciente, key, value)
            return paciente
        else:
            return None



    @staticmethod
    def delete_paciente(ci):
        paciente = PacientesService.find_paciente(ci)
        if paciente:
            pacientes.remove(paciente)
            return paciente
        else:
            return None

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
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_diagnostico(diagnostico)
                if pacientes_filtrados:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, PacientesService.pacientes_list())
        elif parsed_path.path.startswith("/pacientes/"):
            ci = parsed_path.path.split("/")[-1]
            paciente = PacientesService.find_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente.__dict__])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            data = self.read_data()
            paciente = PacientesService.update_paciente(ci, data)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente.__dict__)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            paciente = PacientesService.delete_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente.__dict__)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            data_objet = json_a_paciente(data)
            pacientes.append(data_objet) 
            HTTPResponseHandler.handle_response(self, 200, data_objet.__dict__)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

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
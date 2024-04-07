from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Mensaje:
    def __init__(self, id, contenido, contenido_encriptado):
        self.id = id
        self.contenido = contenido
        self.contenido_encriptado = contenido_encriptado

class MensajeBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.mensaje = {}

    def set_id(self, id):
        self.mensaje['id'] = id
        return self

    def set_contenido(self, contenido):
        self.mensaje['contenido'] = contenido
        return self

    def set_contenido_encriptado(self, contenido_encriptado):
        self.mensaje['contenido_encriptado'] = contenido_encriptado
        return self

    def build(self):
        mensaje = self.mensaje
        self.reset()
        return mensaje

mensajes = []
id_counter = 1

def encriptar_mensaje(contenido):
    contenido_encriptado = ""
    for char in contenido:
        if char.isalpha():
            offset = 3
            ascii_code = ord(char)
            encrypted_code = ascii_code + offset if ascii_code <= ord('z') - offset else ascii_code - 26 + offset
            contenido_encriptado += chr(encrypted_code)
        else:
            contenido_encriptado += char
    return contenido_encriptado

class MensajesService:
    @staticmethod
    def create_mensaje(contenido):
        global id_counter
        contenido_encriptado = encriptar_mensaje(contenido)
        mensaje = Mensaje(id_counter, contenido, contenido_encriptado)
        id_counter += 1
        mensajes.append(mensaje)
        return mensaje

    @staticmethod
    def get_mensajes():
        return [mensaje.__dict__ for mensaje in mensajes]

    @staticmethod
    def get_mensaje_by_id(id):
        mensaje = next((mensaje for mensaje in mensajes if mensaje.id == id), None)
        return mensaje.__dict__ if mensaje else None

    @staticmethod
    def update_mensaje(id, contenido):
        mensaje = MensajesService.get_mensaje_by_id(id)
        if mensaje:
            mensaje['contenido'] = contenido
            mensaje['contenido_encriptado'] = encriptar_mensaje(contenido)
            return mensaje
        else:
            return None

    @staticmethod
    def delete_mensaje(id):
        global mensajes
        mensajes = [mensaje for mensaje in mensajes if mensaje.id != id]
        return mensajes

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
        path_parts = parsed_path.path.split("/")

        if parsed_path.path == "/mensajes":
            HTTPResponseHandler.handle_response(self, 200, MensajesService.get_mensajes())
        elif path_parts[1] == "mensajes" and len(path_parts) == 3:
            mensaje_id = int(path_parts[2])
            mensaje = MensajesService.get_mensaje_by_id(mensaje_id)
            if mensaje:
                HTTPResponseHandler.handle_response(self, 200, mensaje)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/mensajes":
            data = self.read_data()
            contenido = data["contenido"]
            print(type(contenido))
            mensaje = MensajesService.create_mensaje(contenido)
            HTTPResponseHandler.handle_response(self, 200, mensaje.__dict__)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split("/")

        if path_parts[1] == "mensajes" and len(path_parts) == 3:
            mensaje_id = int(path_parts[2])
            data = self.read_data()
            contenido = data["contenido"]
            mensaje = MensajesService.update_mensaje(mensaje_id, contenido)
            if mensaje:
                HTTPResponseHandler.handle_response(self, 200, mensaje)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split("/")

        if path_parts[1] == "mensajes" and len(path_parts) == 3:
            mensaje_id = int(path_parts[2])
            mensajes = MensajesService.delete_mensaje(mensaje_id)
            HTTPResponseHandler.handle_response(self, 200, mensajes)
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

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from urllib.parse import urlparse, parse_qs

class JuegoPiedraPapelTijera:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.partidas = []
        return cls.__instance

    def jugar(self, elemento_jugador):
        elementos = ["piedra", "papel", "tijera"]
        elemento_servidor = random.choice(elementos)
        resultado = self.calcular_resultado(elemento_jugador, elemento_servidor)
        partida = {
            "id": len(self.partidas) + 1,
            "elemento": elemento_jugador,
            "elemento_servidor": elemento_servidor,
            "resultado": resultado
        }
        self.partidas.append(partida)
        return partida

    def calcular_resultado(self, elemento_jugador, elemento_servidor):
        if elemento_jugador == elemento_servidor:
            return "empate"
        elif (elemento_jugador == "piedra" and elemento_servidor == "tijera") or \
             (elemento_jugador == "tijera" and elemento_servidor == "papel") or \
             (elemento_jugador == "papel" and elemento_servidor == "piedra"):
            return "ganó"
        else:
            return "perdió"

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/partidas":
            data = self.read_data()
            juego = JuegoPiedraPapelTijera()
            partida = juego.jugar(data["elemento"])
            self.handle_response(200, partida)
        else:
            self.handle_response(404, {"Error": "Ruta no existente"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/partidas":
            if "resultado" in query_params:
                resultado = query_params["resultado"][0]
                partidas_filtradas = self.filter_partidas(resultado)
                self.handle_response(200, partidas_filtradas)
            else:
                juego = JuegoPiedraPapelTijera()
                partidas = juego.partidas
                self.handle_response(200, partidas)
        else:
            self.handle_response(404, {"Error": "Ruta no existente"})

    def filter_partidas(self, resultado):
        juego = JuegoPiedraPapelTijera()
        return [partida for partida in juego.partidas if partida["resultado"] == resultado]

    def handle_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

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

from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def suma(num1, num2):
    return num1 + num2

def resta(num1, num2):
    return num1 - num2

def multiplicacion(num1, num2):
    return num1 * num2

def division(num1, num2):
    if num2 != 0:
        return num1 / num2
    else:
        return "Error: Division por cero"

operaciones = {
    'suma': {
        'func': suma, 
        'returns': {'resultado': int},
        'args': {'num1': int, 'num2': int}
        },
    'resta': {
        'func': resta,
        'returns': {'resultado': int},
        'args': {'num1': int, 'num2': int}
        },
    'multiplicacion': {
        'func': multiplicacion, 
        'returns': {'resultado': int},
        'args': {'num1': int, 'num2': int}
        },
    'division': {
        'func': division,
        'returns': {'resultado': float}, 
        'args': {'num1': int, 'num2': int}
        },
}

dispatcher = SoapDispatcher(
    'operaciones-soap-server',
    location='http://localhost:8000/',
    action='http://localhost:8000/',
    namespace='http://localhost:8000/',
    trace=True,
    ns=True,
)

for name, date_function in operaciones.items():
    dispatcher.register_function(name, date_function['func'], returns=date_function['returns'], args=date_function['args'])

server = HTTPServer(('0.0.0.0', 8000), SOAPHandler)
server.dispatcher = dispatcher

print('Servidor SOAP iniciado en http://localhost:8000/')
server.serve_forever()

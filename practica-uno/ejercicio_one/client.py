from zeep import Client

url = 'http://localhost:8000/'

client = Client(url)

num1 = 10
num2 = 5

resultado_suma = client.service.suma(num1, num2)
print(f'Suma de {num1} y {num2}: {resultado_suma}')

resultado_resta = client.service.resta(num1, num2)
print(f'Resta de {num1} y {num2}: {resultado_resta}')

resultado_multiplicacion = client.service.multiplicacion(num1, num2)
print(f'Multiplicacion de {num1} y {num2}: {resultado_multiplicacion}')

resultado_division = client.service.division(num1, num2)
resultado_division_format = "{:.2f}".format(resultado_division)
print(f'División de {num1} y {num2}: {resultado_division_format}')


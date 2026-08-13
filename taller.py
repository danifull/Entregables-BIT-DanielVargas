calificacion = ""
acumulacion = 0.0
promedio = 0.0
busqueda = ""
encontrado = False


estudiantes = [
    ("Pedro", 10, 3.2),
    ("Angel", 12, 3.4),
    ("Ana", 11, 2.2),
    ("Juan", 13, 5.0),
    ("Carlos", 16, 1.8),
    ("Roberto", 17, 3.6),
    ("Lina", 9, 3.3),
    ("Andres", 8, 3.7),
    ("Carmen", 11, 1.2),
    ("Miguel", 13, 4.2),
]

for nombre, edad, nota in estudiantes:
    print(f"{nombre} tiene {edad} años y obtuvo una nota de {nota}")

    if nota >= 4.5:
        calificacion = "EXCELENTE"
        print(f"{nombre} saco una nota de {nota}, su promedio es {calificacion}")
    elif nota >= 4.0 and nota <= 4.49:
        calificacion = "BUENO"
        print(f"{nombre} saco una nota de {nota}, su promedio es {calificacion}")
    elif nota >= 3.0 and nota <= 3.99:
        calificacion = "ACEPTABLE"
        print(f"{nombre} saco una nota de {nota}, su promedio es {calificacion}")
    elif nota < 3.0:
        calificacion = "REPROBÓ"
        print(f"{nombre} saco una nota de {nota}, su promedio es {calificacion}")

    acumulacion += nota

promedio = acumulacion / len(estudiantes)

print(f"El Promedio de Nota es {promedio}")

busqueda = input("Ingrese el nombre del estudiante: ")

for nombres, edad, nota in estudiantes:
    if busqueda == nombres:
        encontrado = True
        break

if encontrado:
    print(f"El Estudiante {busqueda} ha sido encontrado en nuestra base.")
else:
    print(f"El Estudiante {busqueda} NO se encuentra.")


estudiantes = {
    "Andres": "Cartagena",
    "Carlos": "Cali",
    "Pedro": "Bogota",
    "Juan": "Medellin",
    "Luis": "Cali",
    "Miguel": "Bogota",
    "Daniel": "Medellin",
    "Santiago": "Cartagena",
    "Felipe": "Cali",
    "Sebastian": "Bogota",
    "Mateo": "Medellin",
    "Nicolas": "Cartagena",
    "Alejandro": "Cali",
    "David": "Bogota",
    "Jorge": "Medellin",
    "Camilo": "Cartagena",
    "Andres Felipe": "Cali",
    "Juan Pablo": "Bogota",
    "Diego": "Medellin",
    "Cristian": "Cartagena",
}

for nombre, ciudad in estudiantes.items():
    print(f"{nombre} vive en {ciudad}")


conteo_ciudad = {}

for nombre, ciudad in estudiantes.items():
    if ciudad in conteo_ciudad:
        conteo_ciudad[ciudad] += 1
    else:
        conteo_ciudad[ciudad] = 1

print(conteo_ciudad)

suma_total = 0
conteo = 0

while True:
    numero_ingresado = int(input("Ingrese un numero (para detener oprima 0): "))
    if numero_ingresado == 0:
        break
    conteo = conteo + 1
    suma_total = suma_total + numero_ingresado

if conteo > 0:
    promedio = suma_total / conteo
    print(
        f"La cantidad es: {conteo}, la suma es: {suma_total}, el promedio es: {promedio}"
    )
else:
    print("No ingresaste ningún número.")


for i in range(1, 31):
    if i == 25:
        break
    elif i % 3 == 0:
        continue
    print(f"Numeros procesados en el ciclo: {i}")

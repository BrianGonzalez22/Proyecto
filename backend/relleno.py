import sqlite3
from faker import Faker
import random
from datetime import datetime

# Conectar a la base de datos SQLite
conn = sqlite3.connect("db.sqlite3")  # Asegúrate de usar el nombre correcto de tu BD
cursor = conn.cursor()

# Inicializar Faker para generar datos falsos
fake = Faker()

# Cantidad de registros a insertar
NUM_USUARIOS = 15
NUM_VEHICULOS = NUM_USUARIOS
NUM_REGISTROS = 20

# 1️⃣ Insertar usuarios en la tabla datos_usuarios
usuarios = []
for _ in range(NUM_USUARIOS):
    nombre = fake.name()
    correo = fake.email()
    telefono = fake.phone_number()
    
    cursor.execute("""
        INSERT INTO datos_usuarios (nombre, correo, telefono) 
        VALUES (?, ?, ?)
    """, (nombre, correo, telefono))
    
    usuarios.append(cursor.lastrowid)  # Guardar el ID del usuario recién insertado


# Insertar vehículos (1 vehículo por usuario)
vehiculos = []
for usuario_id in usuarios:  # Asignar un vehículo a cada usuario de la lista
    placa = fake.unique.license_plate()
    modelo = fake.word().capitalize()
    color = fake.color_name()
    tipo = random.choice(["Sedán", "SUV", "Camioneta", "Deportivo", "Hatchback"])
    estado = random.choice([0, 1])
    
    cursor.execute("""
        INSERT INTO datos_vehiculos (usuario_id, placa, modelo, color, tipo, estado) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (usuario_id, placa, modelo, color, tipo, estado))
    
    vehiculos.append(cursor.lastrowid)  # Guardar el ID del vehículo recién insertado


# 3️⃣ Insertar registros en la tabla datos_registros
tipos_movimiento = ["entrada", "salida"]
for _ in range(NUM_REGISTROS):
    usuario_id = random.choice(usuarios)
    vehiculo_id = random.choice(vehiculos)
    movimiento = random.choice(tipos_movimiento)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato SQLite
    cursor.execute("""
        INSERT INTO datos_registros (usuario_id, vehiculo_id, movimiento, fecha) 
        VALUES (?, ?, ?, ?)
    """, (usuario_id, vehiculo_id, movimiento, fecha))

# Guardar los cambios en la base de datos y cerrar la conexión
conn.commit()
conn.close()

print("✅ Registros insertados correctamente en la base de datos.")

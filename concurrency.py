import psycopg2
import threading
import time
from datetime import datetime
from statistics import mean
import random

# Config DB
db_config = {
    "dbname": "Proyect2_Isolation",
    "user": "postgres",
    "password": "diegodb",
    "host": "localhost",
    "port": 5432
}

# Nivel de aislamiento
niveles = {
    "READ COMMITTED": psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
    "REPEATABLE READ": psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
    "SERIALIZABLE": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
}

# Resultados compartidos
resultados = {
    "exitosas": 0,
    "fallidas": 0,
    "tiempos": []
}
lock = threading.Lock()


def log(usuario_id, mensaje):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [Usuario {usuario_id}] {mensaje}")


def reservar_localidad(usuario_id, localidad_id, nivel_psycopg2):
    inicio = time.time()
    try:
        with psycopg2.connect(**db_config) as conn:
            conn.set_session(isolation_level=nivel_psycopg2)
            with conn.cursor() as cursor:
                cursor.execute("BEGIN;")

                cursor.execute(
                    "SELECT disponible FROM localidades WHERE id = %s ;", (localidad_id,))
                result = cursor.fetchone()
                # time.sleep(random.uniform(0.1, 0.3))

                if result and result[0]:
                    cursor.execute(
                        "UPDATE localidades SET disponible = false WHERE id = %s;", (localidad_id,))
                    cursor.execute(
                        "INSERT INTO reservas (id_usuario, id_localidad) VALUES (%s, %s);", (usuario_id, localidad_id))
                    conn.commit()
                    log(usuario_id, "Reserva exitosa.")
                    with lock:
                        resultados["exitosas"] += 1
                else:
                    conn.rollback()
                    log(usuario_id, "Reserva fallida.")
                    with lock:
                        resultados["fallidas"] += 1
    except Exception as e:
        log(usuario_id, f"Error: {e}")
        with lock:
            resultados["fallidas"] += 1
    finally:
        duracion = (time.time() - inicio) * 1000  # milisegundos
        with lock:
            resultados["tiempos"].append(duracion)

# Función para ejecutar la prueba con N usuarios


def ejecutar_simulacion(num_usuarios, nivel_nombre):
    global resultados
    resultados = {"exitosas": 0, "fallidas": 0, "tiempos": []}

    localidad_id = crear_localidad_para_prueba()

    hilos = []
    for i in range(num_usuarios):
        # delay = random.uniform(0.1,0.5)
        t = threading.Thread(target=reservar_localidad, args=(
            i + 1, localidad_id, niveles[nivel_nombre]))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    print("\n--- RESULTADOS ---")
    print(f"Usuarios: {num_usuarios}")
    print(f"Nivel: {nivel_nombre}")
    print(f"Exitosas: {resultados['exitosas']}")
    print(f"Fallidas: {resultados['fallidas']}")
    print(f"Tiempo promedio: {mean(resultados['tiempos']):.2f} ms")
    print("------------------\n")


# Crear una nueva localidad libre para probar (cada vez)
def crear_localidad_para_prueba():
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO localidades (id_evento, seccion, fila, numero, disponible)
                VALUES (1, 'VIP', 'A', floor(random()*1000)::int, true)
                RETURNING id;
            """)
            return cursor.fetchone()[0]


if __name__ == "__main__":
    ejecutar_simulacion(5, "READ COMMITTED")
    ejecutar_simulacion(5, "REPEATABLE READ")
    ejecutar_simulacion(5, "SERIALIZABLE")


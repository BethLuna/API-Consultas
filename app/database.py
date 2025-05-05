# database.py
import os
import pandas as pd
from sqlalchemy import create_engine






# Cargar variables de entorno
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
MYSQL_USER = os.getenv('MYSQL_USER', 'user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
MYSQL_DB = os.getenv('MYSQL_DB', 'video_games')

# Crear engine
engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')

# Tablas y carpeta destino
tablas = ['genre', 'game', 'game_platform', 'game_publisher', 'platform', 'publisher', 'region', 'region_sales']
carpeta_destino = '/app/data'

def extraer_tablas(tablas, carpeta_destino):
    os.makedirs(carpeta_destino, exist_ok=True)
    for tabla in tablas:
        df = pd.read_sql(f"SELECT * FROM {tabla}", con=engine)
        archivo_salida = os.path.join(carpeta_destino, f"{tabla}.csv")
        df.to_csv(archivo_salida, index=False)
        print(f"Tabla {tabla} exportada a {archivo_salida}")

def verificar_archivos(tablas, carpeta_destino):
    for archivo in tablas:
        ruta_archivo = os.path.join(carpeta_destino, f"{archivo}.csv")
        if os.path.exists(ruta_archivo):
            print(f"El archivo {archivo} se ha descargado correctamente.")
        else:
            print(f"El archivo {archivo} no se encuentra en la ruta {ruta_archivo}.")

def obtener_datos():
    # Establecer la conexión a la base de datos
    engine = create_engine("mysql+pymysql://usuario:contraseña@localhost/base_de_datos")
    with engine.connect() as connection:
        # Realizar la consulta
        result = connection.execute("SELECT * FROM tabla")
        # Retornar los resultados
        return result.fetchall()
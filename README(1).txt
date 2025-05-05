Iniciar el proyecto con Docker:

Abre una terminal, navega a la carpeta principal del proyecto y ejecuta el siguiente comando:

docker compose up -d --build

Acceso a las interfaces:

    Documentación de la API (FastAPI - Swagger UI):
    http://localhost:8000/docs#/

    phpMyAdmin (gestor de base de datos):
    http://localhost:8082/

Archivos CSV:

Los archivos .csv se generan automáticamente al iniciar los contenedores de Docker.

Visualización de datos en Swagger:

Para ver el contenido de las tablas en la interfaz de Swagger:

    Ingresa a la documentación en http://localhost:8000/docs#/

    Haz clic en el endpoint correspondiente (por ejemplo, /get_all_data/)

    Presiona el botón "Try it out" y luego "Execute"

    Revisa la URL generada en el campo Request URL

    Da clic en esa URL o ábrela directamente en el navegador para ver los datos de forma legible.
    De lo contrario, solo verás una vista en crudo en el campo Response body.
    
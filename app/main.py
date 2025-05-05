from fastapi import APIRouter, FastAPI
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import StreamingResponse
from database import obtener_datos
from visualizations import router as vis_router
from fastapi import FastAPI
from routes import router as routes_router
from crud import router as crud_router
from tables import router as tables_router



router = APIRouter()
app = FastAPI()

  # este ya estaba
app.include_router(router)  
app.include_router(vis_router, prefix="/Graficas_panda")
app.include_router(routes_router)
app.include_router(crud_router)    # este es el que faltaba
app.include_router(tables_router, prefix="/Tablas")


@router.get("/grafica")
async def obtener_grafica():
    datos = obtener_datos()
    df = pd.DataFrame(datos)

    plt.figure(figsize=(10, 6))
    df['columna'].value_counts().plot(kind='bar')
    plt.title('Ejemplo de Gráfica')

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

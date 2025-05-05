from fastapi import APIRouter, Response, HTTPException
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from sqlalchemy import create_engine
from database import engine

router = APIRouter()

# Conexión a la base de datos
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
MYSQL_USER = os.getenv('MYSQL_USER', 'user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
MYSQL_DB = os.getenv('MYSQL_DB', 'video_games')

engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')



@router.get("/ventas_por_genero", response_class=Response, tags=["Graficas"])
async def get_sales_per_genre_plot():
    query = """
    SELECT g.genre_name, SUM(rs.num_sales) AS num_sales
    FROM genre g
    JOIN game g2 ON g.id = g2.genre_id
    JOIN game_publisher gp ON gp.game_id = g2.id
    JOIN game_platform gpl ON gpl.game_publisher_id = gp.id
    JOIN region_sales rs ON rs.game_platform_id = gpl.id
    GROUP BY g.genre_name
    ORDER BY num_sales DESC;
    """
    try:
        df = pd.read_sql(query, con=engine)

        plt.figure(figsize=(10, 6))
        df.set_index("genre_name")["num_sales"].plot(kind='bar', title='Ventas por Género', color='coral')
        plt.ylabel("Unidades Vendidas")
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        return Response(content=buf.getvalue(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ventas_por_plataforma", response_class=Response, tags=["Graficas"])
async def get_sales_per_platform_plot():
    query = """
    SELECT p.platform_name, SUM(rs.num_sales) AS num_sales
    FROM platform p
    JOIN game_platform gp ON p.id = gp.platform_id
    JOIN region_sales rs ON rs.game_platform_id = gp.id
    GROUP BY p.platform_name
    ORDER BY num_sales DESC;
    """
    try:
        df = pd.read_sql(query, con=engine)

        plt.figure(figsize=(10, 6))
        plt.bar(df['platform_name'], df['num_sales'], color='mediumseagreen')
        plt.title('Ventas Totales por Plataforma')
        plt.xlabel('Plataforma')
        plt.ylabel('Ventas')
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        return Response(content=buf.getvalue(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ventas_por_año", response_class=Response, tags=["Graficas"])
async def get_sales_per_year_plot():
    query = """
    SELECT gp.release_year, SUM(rs.num_sales) AS num_sales
    FROM game_platform gp
    JOIN region_sales rs ON rs.game_platform_id = gp.id
    GROUP BY gp.release_year
    ORDER BY gp.release_year;
    """
    try:
        df = pd.read_sql(query, con=engine)

        plt.figure(figsize=(10, 6))
        plt.plot(df['release_year'], df['num_sales'], marker='o', linestyle='-', color='steelblue')
        plt.title('Ventas Totales por Año de Lanzamiento')
        plt.xlabel('Año de Lanzamiento')
        plt.ylabel('Ventas')
        plt.grid(True)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        return Response(content=buf.getvalue(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






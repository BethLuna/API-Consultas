from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse  # Cambiado a JSONResponse
import pandas as pd
from database import engine

router = APIRouter()

@router.get("/games/genre", tags=["Consultas"])
async def get_games_by_genre(genre: str):
    query = """
    SELECT game.game_name AS nombre_juego, 
           platform.platform_name AS plataforma,
           release_year AS año_lanzamiento
    FROM game
    JOIN genre ON genre.id = game.genre_id
    JOIN game_publisher ON game_publisher.game_id = game.id
    JOIN game_platform ON game_platform.game_publisher_id = game_publisher.id
    JOIN platform ON platform.id = game_platform.platform_id
    WHERE genre.genre_name LIKE %s
    LIMIT 50;
    """
    try:
        genre_param = f"%{genre}%"
        df = pd.read_sql(query, con=engine, params=(genre_param,))
        return JSONResponse(content=df.to_dict(orient='records'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/year", tags=["Consultas"])
async def get_games_by_year_and_platform(year: int, platform: str):
    query = """
    SELECT 
        g.game_name, 
        p.platform_name, 
        gpl.release_year
    FROM game g
    INNER JOIN game_publisher gp ON g.id = gp.game_id
    INNER JOIN game_platform gpl ON gp.id = gpl.game_publisher_id
    INNER JOIN platform p ON gpl.platform_id = p.id
    WHERE gpl.release_year = %s
    AND p.platform_name LIKE %s
    LIMIT 50;
    """
    try:
        df = pd.read_sql(query, con=engine, params=(year, f"%{platform}%"))
        return JSONResponse(content=df.to_dict(orient='records'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/publisher-sales", tags=["Consultas"])
async def get_sales_by_publisher():
    query = """
    SELECT pub.publisher_name, SUM(rs.num_sales) AS total_sales
    FROM publisher pub
    JOIN game_publisher gp ON pub.id = gp.publisher_id
    JOIN game_platform gpl ON gp.id = gpl.game_publisher_id
    JOIN region_sales rs ON gpl.id = rs.game_platform_id
    GROUP BY pub.publisher_name
    ORDER BY total_sales DESC
    """
    try:
        df = pd.read_sql(query, con=engine)
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/platform-count", tags=["Consultas"])  # Corregido el nombre
async def get_game_count_per_platform():
    query = """
    SELECT p.platform_name, COUNT(*) AS total_games
    FROM platform p
    JOIN game_platform gpl ON p.id = gpl.platform_id
    GROUP BY p.platform_name
    ORDER BY total_games DESC
    """
    try:
        df = pd.read_sql(query, con=engine)
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/top-release-year", tags=["Consultas"])  # Corregido el nombre
async def get_year_with_most_releases():
    query = """
    SELECT gp.release_year, COUNT(*) AS total_games
    FROM game g
    JOIN game_publisher gpub ON g.id = gpub.game_id
    JOIN game_platform gp ON gpub.id = gp.game_publisher_id
    WHERE gp.release_year IS NOT NULL
    GROUP BY gp.release_year
    ORDER BY total_games DESC
    LIMIT 20;
    """
    try:
        df = pd.read_sql(query, con=engine)
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
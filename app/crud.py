import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text



# Conexión a base de datos
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
MYSQL_USER = os.getenv('MYSQL_USER', 'user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
MYSQL_DB = os.getenv('MYSQL_DB', 'video_games')

engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')

# Crear un router para el CRUD
router = APIRouter()

# Modelos de datos (Pydantic) para entrada de datos
class GameCreate(BaseModel):
    game_name: str
    genre_id: int
    publisher_id: int
    release_year: int

class GameUpdate(BaseModel):
    game_name: str | None = None
    genre_id: int | None = None
    publisher_id: int | None = None
    release_year: int | None = None

# Crear juego
@router.post("/games", tags=["?"])
async def create_game(game: GameCreate):
    query = """
    INSERT INTO game (game_name, genre_id, publisher_id, release_year)
    VALUES (:game_name, :genre_id, :publisher_id, :release_year)
    """
    try:
        with engine.begin() as conn:
            conn.execute(text(query), {
                "game_name": game.game_name,
                "genre_id": game.genre_id,
                "publisher_id": game.publisher_id,
                "release_year": game.release_year
            })
            return {"message": "Game created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating game: {e}")



# Obtener todos los juegos
@router.get("/games", tags=["Consultas"])
async def get_all_games():
    query = "SELECT * FROM game"
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            games = [dict(row._mapping) for row in result]
            return {"games": games}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching games: {e}")









# Obtener juego por ID
@router.get("/games/{game_id}", tags=["?"])
async def get_game_by_id(game_id: int):
    query = "SELECT * FROM game WHERE id = :game_id"
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), {"game_id": game_id}).fetchone()
            if result:
                return dict(result)
            else:
                raise HTTPException(status_code=404, detail="Game not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching game: {e}")

# Actuali?ar juego
@router.put("/games/{game_id}", tags=["?"])
async def update_game(game_id: int, game: GameUpdate):
    query = """
    UPDATE game
    SET game_name = COALESCE(:game_name, game_name),
        genre_id = COALESCE(:genre_id, genre_id),
        publisher_id = COALESCE(:publisher_id, publisher_id),
        release_year = COALESCE(:release_year, release_year)
    WHERE id = :game_id
    """
    try:
        with engine.begin() as conn:
            result = conn.execute(text(query), {
                "game_id": game_id,
                "game_name": game.game_name,
                "genre_id": game.genre_id,
                "publisher_id": game.publisher_id,
                "release_year": game.release_year
            })
            return {"message": "Game updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating game: {e}")

# Eliminar juego
@router.delete("/games/{game_id}", tags=["?"])
async def delete_game(game_id: int):
    query = "DELETE FROM game WHERE id = :game_id"
    try:
        with engine.begin() as conn:
            conn.execute(text(query), {"game_id": game_id})
            return {"message": "Game deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting game: {e}")

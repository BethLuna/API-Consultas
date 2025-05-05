from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import pandas as pd
from pathlib import Path

router = APIRouter()

# Configuración de rutas
DATA_DIR = Path("data")

# Cargar todos los datos al iniciar (para mejor performance)
def load_all_data():
    return {
        'game': pd.read_csv(DATA_DIR / "game.csv"),
        'genre': pd.read_csv(DATA_DIR / "genre.csv").rename(columns={'genre_name': 'genero'}),
        'publisher': pd.read_csv(DATA_DIR / "publisher.csv"),
        'game_publisher': pd.read_csv(DATA_DIR / "game_publisher.csv"),
        'platform': pd.read_csv(DATA_DIR / "platform.csv"),
        'game_platform': pd.read_csv(DATA_DIR / "game_platform.csv"),
        'region': pd.read_csv(DATA_DIR / "region.csv").rename(columns={'region_name': 'name'}),
        'region_sales': pd.read_csv(DATA_DIR / "region_sales.csv")
    }

# Cargamos todos los datos una vez
data = load_all_data()

# Función para generar HTML
def generate_html_response(df: pd.DataFrame, title: str) -> HTMLResponse:
    html = df.to_html(index=False, classes='table', border=0)
    
    style = """
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4; }
        .table {
            border-collapse: collapse;
            width: 80%;
            margin: auto;
            background-color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .table th, .table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .table th {
            background-color: #4CAF50;
            color: white;
        }
        .table tr:nth-child(even){background-color: #f2f2f2;}
        .table tr:hover {background-color: #ddd;}
    </style>
    """
    
    content = f"""
    <html>
        <head>
            <title>{title}</title>
            {style}
        </head>
        <body>
            <h2 style="text-align:center;">{title}</h2>
            {html}
        </body>
    </html>
    """
    
    return HTMLResponse(content=content)

@router.get("/tabla/publishers", response_class=HTMLResponse, tags=["Tablas"])
async def tabla_publishers():
    try:
        merged = pd.merge(data['publisher'], data['game_publisher'], 
                         left_on='id', right_on='publisher_id')
        merged = pd.merge(merged, data['game_platform'], 
                         left_on='id_y', right_on='game_publisher_id')
        merged = pd.merge(merged, data['region_sales'], 
                         left_on='id', right_on='game_platform_id')
        
        result = merged.groupby('publisher_name')['num_sales'].sum().reset_index()
        result.columns = ['publisher_name', 'total_sales']
        result = result.sort_values('total_sales', ascending=False).head(20)
        
        return generate_html_response(result, "Top 20 Publishers por Ventas")
    
    except Exception as e:
        error_msg = f"<h1>Error</h1><p>{str(e)}</p>"
        return HTMLResponse(content=error_msg)




@router.get("/tabla/platforms", response_class=HTMLResponse, tags=["Tablas"])
async def tabla_platforms():
    try:
        merged = pd.merge(data['platform'], data['game_platform'], 
                         left_on='id', right_on='platform_id')
        merged = pd.merge(merged, data['region_sales'], 
                         left_on='id_y', right_on='game_platform_id')
        
        result = merged.groupby('platform_name')['num_sales'].sum().reset_index()
        result.columns = ['platform_name', 'total_sales']
        result = result.sort_values('total_sales', ascending=False).head(20)
        
        return generate_html_response(result, "Top 20 Plataformas por Ventas")
    
    except Exception as e:
        error_msg = f"<h1>Error</h1><p>{str(e)}</p>"
        return HTMLResponse(content=error_msg)


@router.get("/tabla/genres", response_class=HTMLResponse, tags=["Tablas"])
async def tabla_genres():
    try:
        # 1. Primer merge: genre + game
        step1 = pd.merge(
            data['genre'],
            data['game'],
            left_on='id',
            right_on='genre_id',
            suffixes=('_genre', '_game')
        )
        
        # 2. Segundo merge: + game_publisher
        step2 = pd.merge(
            step1,
            data['game_publisher'],
            left_on='id_game',
            right_on='game_id',
            suffixes=('_prev', '_gp')
        )
        
        # 3. Tercer merge (CORREGIDO): + game_platform
        step3 = pd.merge(
            step2,
            data['game_platform'],
            left_on='id',  # Usamos 'id' de game_publisher en lugar de 'id_gp'
            right_on='game_publisher_id',
            suffixes=('_prev', '_gpl')
        )
        
        # 4. Cuarto merge: + region_sales
        final = pd.merge(
            step3,
            data['region_sales'],
            left_on='id_gpl',  # 'id' de game_platform
            right_on='game_platform_id'
        )
        
        # 5. Procesamiento final
        result = final.groupby('genero')['num_sales'].sum().reset_index()
        result.columns = ['genero', 'ventas_totales']
        result = result.sort_values('ventas_totales', ascending=False).head(20)
        
        return generate_html_response(result, "Top 20 Géneros por Ventas")
        
    except Exception as e:
        error_msg = f"""
        <h1>Error</h1>
        <p>{str(e)}</p>
        <h3>Recuerda:</h3>
        <ul>
            <li>genre → game: left_on='id', right_on='genre_id'</li>
            <li>+ game_publisher: left_on='id_game', right_on='game_id'</li>
            <li>+ game_platform: left_on='id', right_on='game_publisher_id'</li>
            <li>+ region_sales: left_on='id_gpl', right_on='game_platform_id'</li>
        </ul>
        """
        return HTMLResponse(content=error_msg)





@router.get("/tabla/regions", response_class=HTMLResponse, tags=["Tablas"])
async def tabla_regions():
    try:
        merged = pd.merge(data['region_sales'], data['region'], 
                         left_on='region_id', right_on='id')
        
        result = merged.groupby('name')['num_sales'].sum().reset_index()
        result.columns = ['region', 'ventas_totales']
        result = result.sort_values('ventas_totales', ascending=False)
        
        return generate_html_response(result, "Ventas por Región")
    
    except Exception as e:
        error_msg = f"<h1>Error</h1><p>{str(e)}</p>"
        return HTMLResponse(content=error_msg)
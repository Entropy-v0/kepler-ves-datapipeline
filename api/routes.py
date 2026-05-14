from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import os
import pandas as pd
import config.settings as settings

router = APIRouter()

# Motor global con Pool de conexiones
url_object = URL.create(
    "postgresql",
    username=os.getenv('DB_USER', settings.DB_USER),
    password=os.getenv('DB_PASS', settings.DB_PASS),
    host=os.getenv('DB_HOST', settings.DB_HOST),
    port=os.getenv('DB_PORT', settings.DB_PORT),
    database=os.getenv('DB_NAME', settings.DB_NAME),
)
engine = create_engine(url_object)

@router.get("/")
async def root():
    return {"message": "Kepler P2P API is ONLINE", "status": "active"}

@router.get("/ads")
async def get_latest_ads(limit: int = 50):
    try:
        with engine.connect() as connection:
            query = text("SELECT * FROM p2p_ads ORDER BY timestamp DESC LIMIT :limit")
            df = pd.read_sql(query, connection, params={"limit": limit})
            return df.to_dict(orient="records") 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.get("/stats")
async def get_market_stats():
    """Retorna promedios y picos de precio y stock."""
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT 
                    AVG(price) as avg_p, MAX(price) as max_p, MIN(price) as min_p,
                    AVG(surplus_amount) as avg_s, MAX(surplus_amount) as max_s, MIN(surplus_amount) as min_s,
                    COUNT(*) as total
                FROM p2p_ads
            """)
            res = connection.execute(query).fetchone()
            
            return {
                "precio": {
                    "promedio": round(res.avg_p, 2) if res.avg_p else 0,
                    "pico_alto": res.max_p or 0,
                    "pico_bajo": res.min_p or 0
                },
                "stock": {
                    "promedio": round(res.avg_s, 2) if res.avg_s else 0,
                    "pico_maximo": res.max_s or 0,
                    "pico_minimo": res.min_s or 0
                },
                "muestras": res.total
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/volume")
async def get_total_volume():
    """Calcula el volumen total de USDT y su equivalente estimado en VES."""
    try:
        with engine.connect() as connection:
            # Calculamos volumen en USDT y el total nominal en VES (price * available)
            query = text("""
                SELECT 
                    SUM(available) as vol_usdt,
                    SUM(available * price) as vol_ves 
                FROM p2p_ads
            """)    
            result = connection.execute(query).fetchone()
            
            return {
                "total_usdt": round(result.vol_usdt, 2) if result.vol_usdt else 0,
                "total_ves_estimado": round(result.vol_ves, 2) if result.vol_ves else 0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
import os, json, hmac, secrets, uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from fastapi import FastAPI, HTTPException, Header, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

DATABASE_URL = os.getenv("DATABASE_URL", "")
ADMIN_ACCESS_CODE = os.getenv("ADMIN_ACCESS_CODE", "")
ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN", "")
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/var/data/uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CATEGORIES = [
 {"id":"cat_ali","name":"Alimentos","subcats":["Granos y Pastas","Enlatados","Cárnicos","Lácteos"]},
 {"id":"cat_ase","name":"Aseo e Higiene","subcats":["Personal","Hogar y Limpieza","Cuidado Infantil"]},
 {"id":"cat_med","name":"Medicinas y Salud","subcats":["Analgésicos","Primeros Auxilios","Vitaminas"]},
 {"id":"cat_ele","name":"Electrodomésticos","subcats":["Climatización","Cocina","TV y Audio"]},
 {"id":"cat_rop","name":"Ropa y Calzado","subcats":["Hombre","Mujer","Niños"]},
 {"id":"cat_fer","name":"Ferretería","subcats":["Herramientas","Pintura","Solar/Baterías"]},
 {"id":"cat_tec","name":"Tecnología","subcats":["Teléfonos","Accesorios","Computación"]},
 {"id":"cat_rep","name":"Repuestos Auto/Moto","subcats":["Llantas","Baterías","Piezas"]},
 {"id":"cat_com","name":"Combos Especiales","subcats":["Combos Comida","Combos Aseo","Mix"]},
 {"id":"cat_mis","name":"Misceláneos","subcats":["Varios","Regalos"]}
]
DEFAULT_STATES = [
 {"name":"Florida (FL)","fee":0},{"name":"Texas (TX)","fee":10},{"name":"New York (NY)","fee":15},
 {"name":"California (CA)","fee":20},{"name":"New Jersey (NJ)","fee":12},{"name":"Georgia (GA)","fee":10},
 {"name":"Illinois (IL)","fee":15},{"name":"Otros Estados EE.UU. (50)","fee":25},
 {"name":"Envío Internacional (Fuera de USA)","fee":35}
]
DEFAULT_PRODUCTS = [
 {"id":1,"name":"Combo Cárnico Familiar","price":85.00,"catId":"cat_ali","subcat":"Cárnicos","stock":"in_stock","desc":"Incluye lomo de cerdo, pollo, picado y embutidos.","img":"https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=400&q=80"},
 {"id":2,"name":"Split Aire Acondicionado 12000 BTU","price":320.00,"catId":"cat_ele","subcat":"Climatización","stock":"in_stock","desc":"Marca reconocida, alta eficiencia energética.","img":"https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=400&q=80"},
 {"id":3,"name":"Kit Aseo Personal Completo","price":45.00,"catId":"cat_ase","subcat":"Personal","stock":"in_stock","desc":"Jabón, champú, crema dental y desodorantes.","img":"https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=400&q=80"}
]

app = FastAPI(title="Agencia Cuba Directo API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "*").split(","), allow_credentials=False, allow_methods=["GET","POST","PUT","DELETE","OPTIONS"], allow_headers=["Authorization","Content-Type"])
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


def db_url():
    if not DATABASE_URL:
        raise RuntimeError("Falta configurar DATABASE_URL en el entorno")
    return DATABASE_URL.replace("postgres://", "postgresql://", 1)


def connect():
    return psycopg.connect(db_url(), row_factory=dict_row, connect_timeout=10)


def init_db():
    with connect() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS app_config (id INTEGER PRIMARY KEY CHECK (id=1), data JSONB NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY, data JSONB NOT NULL, updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())")
        conn.execute("CREATE TABLE IF NOT EXISTS trackings (code TEXT PRIMARY KEY, data JSONB NOT NULL, updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())")
        conn.execute("CREATE TABLE IF NOT EXISTS orders (id UUID PRIMARY KEY, data JSONB NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())")
        cur = conn.execute("SELECT data FROM app_config WHERE id=1")
        row = cur.fetchone()
        if not row:
            config = {"categories":DEFAULT_CATEGORIES,"states":DEFAULT_STATES,"rates":{"air":4.50,"sea":2.00}}
            conn.execute("INSERT INTO app_config(id,data) VALUES(1,%s)", (Jsonb(config),))
            for p in DEFAULT_PRODUCTS:
                conn.execute("INSERT INTO products(id,data) VALUES(%s,%s) ON CONFLICT(id) DO NOTHING", (str(p["id"]), Jsonb(p)))
            conn.execute("INSERT INTO trackings(code,data) VALUES(%s,%s) ON CONFLICT(code) DO NOTHING", ("CUBA-1001", Jsonb({"step":3,"lastUpdate":"Hoy 10:30 AM"})))


@app.on_event("startup")
def startup():
    init_db()


def require_admin(authorization: Optional[str]):
    if not ADMIN_API_TOKEN:
        raise HTTPException(503, "El administrador del servidor debe configurar ADMIN_API_TOKEN")
    token = (authorization or "").removeprefix("Bearer ").strip()
    if not token or not hmac.compare_digest(token, ADMIN_API_TOKEN):
        raise HTTPException(401, "Sesión administrativa no válida")


class LoginBody(BaseModel):
    pin: str

class SettingsBody(BaseModel):
    rates: dict = Field(default_factory=dict)
    states: list = Field(default_factory=list)

class TrackingBody(BaseModel):

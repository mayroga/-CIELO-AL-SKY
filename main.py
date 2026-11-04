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
code: str
    step: int

class OrderBody(BaseModel):
    customer: dict = Field(default_factory=dict)
    items: list
    subtotal: float
    freight_fee: float
    freight_origin: str
    freight_type: str
    weight: float
    total: float
    currency: str = "USD"


@app.get("/")
def home():
    return FileResponse(Path(__file__).with_name("index.html"))

@app.get("/api/health")
def health():
    with connect() as conn:
        conn.execute("SELECT 1")
    return {"ok":True,"database":"connected"}

@app.get("/api/public")
def public_data():
    with connect() as conn:
        cfg = conn.execute("SELECT data FROM app_config WHERE id=1").fetchone()["data"]
        rows = conn.execute("SELECT data FROM products ORDER BY updated_at DESC").fetchall()
    products = [r["data"] for r in rows]
    return {**cfg, "products":products}

@app.post("/api/admin/login")
def admin_login(body: LoginBody):
    if not ADMIN_ACCESS_CODE or not ADMIN_API_TOKEN:
        raise HTTPException(503, "Faltan ADMIN_ACCESS_CODE o ADMIN_API_TOKEN en Render")
    if not hmac.compare_digest(body.pin, ADMIN_ACCESS_CODE):
        raise HTTPException(401, "PIN incorrecto")
    return {"token":ADMIN_API_TOKEN}

@app.get("/api/admin/settings")
def admin_settings(authorization: Optional[str] = Header(default=None)):
    require_admin(authorization)
    with connect() as conn:
        return conn.execute("SELECT data FROM app_config WHERE id=1").fetchone()["data"]

@app.put("/api/admin/settings")
def update_settings(body: SettingsBody, authorization: Optional[str] = Header(default=None)):
    require_admin(authorization)
    if len(body.states) == 0 or any(not isinstance(s, dict) or not s.get("name") or float(s.get("fee", -1)) < 0 for s in body.states):
        raise HTTPException(400, "La lista de orígenes o sus tarifas no es válida")
    rates = {"air":float(body.rates.get("air",0)), "sea":float(body.rates.get("sea",0))}
    if rates["air"] < 0 or rates["sea"] < 0:
        raise HTTPException(400, "Las tarifas por libra no pueden ser negativas")
    with connect() as conn:
        cfg = conn.execute("SELECT data FROM app_config WHERE id=1").fetchone()["data"]
        cfg["rates"] = rates
        cfg["states"] = body.states
        conn.execute("UPDATE app_config SET data=%s WHERE id=1", (Jsonb(cfg),))
    return {"ok":True,"rates":rates,"states":body.states}

@app.post("/api/admin/products")
async def save_product(data: str = Form(...), image: Optional[UploadFile] = File(default=None), authorization: Optional[str] = Header(default=None)):
    require_admin(authorization)
    try:
        product = json.loads(data)
    except Exception:
        raise HTTPException(400, "Datos del producto inválidos")
    product_id = str(product.get("id") or uuid.uuid4())
    product["id"] = product_id
    if image and image.filename:
        content_type = image.content_type or ""
        if not content_type.startswith("image/"):
            raise HTTPException(400, "El archivo debe ser una imagen")
        raw = await_read = image.file.read()
        if len(raw) > 8 * 1024 * 1024:
            raise HTTPException(413, "La imagen supera el límite de 8 MB")
        ext = Path(image.filename).suffix.lower()
        if ext not in {".jpg",".jpeg",".png",".webp",".gif"}:
            ext = ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"
        (UPLOAD_DIR / filename).write_bytes(raw)
        base = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
        product["img"] = f"{base}/uploads/{filename}" if base else f"/uploads/{filename}"
    if not product.get("name") or float(product.get("price", -1)) < 0:
        raise HTTPException(400, "Nombre o precio de producto inválido")
    with connect() as conn:
        conn.execute("INSERT INTO products(id,data,updated_at) VALUES(%s,%s,NOW()) ON CONFLICT(id) DO UPDATE SET data=EXCLUDED.data,updated_at=NOW()", (product_id,Jsonb(product)))
    return {"ok":True,"product":product}

@app.delete("/api/admin/products/{product_id}")
def delete_product(product_id: str, authorization: Optional[str] = Header(default=None)):
    require_admin(authorization)
    with connect() as conn:
        conn.execute("DELETE FROM products WHERE id=%s", (product_id,))
    return {"ok":True}

@app.get("/api/trackings/{code}")
def get_tracking(code: str):
    with connect() as conn:
        row = conn.execute("SELECT data FROM trackings WHERE code=%s", (code.upper(),)).fetchone()
    if not row:
        raise HTTPException(404, "Código de guía no encontrado")
    return {"code":code.upper(), **row["data"]}

@app.put("/api/admin/tracking")
def update_tracking(body: TrackingBody, authorization: Optional[str] = Header(default=None)):
    require_admin(authorization)
    if not body.code.strip() or body.step not in range(1,6):
        raise HTTPException(400, "Código o etapa de rastreo inválidos")
    data = {"step":body.step,"lastUpdate":datetime.now(timezone.utc).astimezone().strftime("%d/%m/%Y %I:%M %p")}
    with connect() as conn:
        conn.execute("INSERT INTO trackings(code,data,updated_at) VALUES(%s,%s,NOW()) ON CONFLICT(code) DO UPDATE SET data=EXCLUDED.data,updated_at=NOW()", (body.code.strip().upper(),Jsonb(data)))
    return {"ok":True,"code":body.code.strip().upper(),**data}

@app.post("/api/orders")
def create_order(body: OrderBody):
    if not body.items or body.total < 0 or body.freight_fee < 0:
        raise HTTPException(400, "El pedido no contiene datos válidos")
    order_id = uuid.uuid4()
    snapshot = body.model_dump()
    snapshot["created_at"] = datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        conn.execute("INSERT INTO orders(id,data) VALUES(%s,%s)", (order_id,Jsonb(snapshot)))
    return {"ok":True,"order_id":str(order_id),"created_at":snapshot["created_at"]} 

import os,json,hmac,uuid,math
from pathlib import Path
from datetime import datetime,timezone
from typing import Optional
import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from fastapi import FastAPI,HTTPException,Header,UploadFile,File,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel,Field

APP_DIR=Path(__file__).resolve().parent
DATABASE_URL=os.getenv("DATABASE_URL","")
ADMIN_ACCESS_CODE=os.getenv("ADMIN_ACCESS_CODE","")
ADMIN_API_TOKEN=os.getenv("ADMIN_API_TOKEN","")

# Corrección de ruta para evitar PermissionError en Render
UPLOAD_DIR=Path(os.getenv("UPLOAD_DIR",APP_DIR/"uploads"))

PUBLIC_BASE_URL=os.getenv("PUBLIC_BASE_URL","").rstrip("/")
MAX_IMAGE_SIZE=8*1024*1024
UPLOAD_DIR.mkdir(parents=True,exist_ok=True)

app=FastAPI(title="Agencia Cuba Directo API",version="1.0.0")
origins=[x.strip() for x in os.getenv("CORS_ORIGINS","*").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins or ["*"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
app.mount("/uploads",StaticFiles(directory=str(UPLOAD_DIR)),name="uploads")

DEFAULT_CONFIG={
    "categories":[
        {"id":"cat_ali","name":"Alimentos"},
        {"id":"cat_ase","name":"Aseo e Higiene"},
        {"id":"cat_med","name":"Medicinas y Salud"},
        {"id":"cat_ele","name":"Electrodomésticos"},
        {"id":"cat_rop","name":"Ropa y Calzado"},
        {"id":"cat_fer","name":"Ferretería"},
        {"id":"cat_tec","name":"Tecnología"},
        {"id":"cat_rep","name":"Repuestos Auto/Moto"},
        {"id":"cat_com","name":"Combos Especiales"},
        {"id":"cat_mis","name":"Misceláneos"}
    ],
    "states":[
        {"name":"Florida","fee":0},
        {"name":"Texas","fee":10},
        {"name":"New York","fee":15},
        {"name":"California","fee":20},
        {"name":"New Jersey","fee":12},
        {"name":"Georgia","fee":10},
        {"name":"Illinois","fee":15},
        {"name":"Other US States","fee":25},
        {"name":"International","fee":35}
    ],
    "rates":{"air":4.50,"sea":2.00}
}

INITIAL_PRODUCTS=[
    {"id":"p001","name":"Combo de Alimentos","price":45,"category":"cat_com","stock":10,"description":"Combo básico de alimentos","image":""},
    {"id":"p002","name":"Kit de Higiene","price":25,"category":"cat_ase","stock":10,"description":"Productos básicos de higiene","image":""},
    {"id":"p003","name":"Ropa Variada","price":35,"category":"cat_rop","stock":10,"description":"Selección de ropa","image":""}
]

def db_url():
    if not DATABASE_URL:
        raise HTTPException(503,"DATABASE_URL no está configurada.")
    return DATABASE_URL.replace("postgres://","postgresql://",1)

def connect():
    return psycopg.connect(db_url(),row_factory=dict_row,connect_timeout=10)

def init_db():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS app_config(
            id INTEGER PRIMARY KEY CHECK(id=1),data JSONB NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS products(
            id TEXT PRIMARY KEY,data JSONB NOT NULL,
            updated_at TIMESTAMPTZ DEFAULT now())""")
        conn.execute("""CREATE TABLE IF NOT EXISTS trackings(
            code TEXT PRIMARY KEY,data JSONB NOT NULL,
            updated_at TIMESTAMPTZ DEFAULT now())""")
        conn.execute("""CREATE TABLE IF NOT EXISTS orders(
            id UUID PRIMARY KEY,data JSONB NOT NULL,
            created_at TIMESTAMPTZ DEFAULT now())""")
        exists=conn.execute("SELECT id FROM app_config WHERE id=1").fetchone()
        if not exists:
            conn.execute("INSERT INTO app_config(id,data) VALUES(1,%s)",(Jsonb(DEFAULT_CONFIG),))
            for p in INITIAL_PRODUCTS:
                conn.execute("INSERT INTO products(id,data) VALUES(%s,%s)",(p["id"],Jsonb(p)))
            conn.execute("INSERT INTO trackings(code,data) VALUES(%s,%s)",(
                "CUBA-1001",Jsonb({"step":3,"lastUpdate":"Hoy 10:30 AM"})))
        conn.commit()

@app.on_event("startup")
def startup():
    init_db()

def get_config():
    with connect() as conn:
        row=conn.execute("SELECT data FROM app_config WHERE id=1").fetchone()
    return row["data"] if row else DEFAULT_CONFIG

def require_admin(authorization:Optional[str]):
    if not ADMIN_API_TOKEN:
        raise HTTPException(503,"ADMIN_API_TOKEN no está configurado.")
    expected="Bearer "+ADMIN_API_TOKEN
    if not authorization or not hmac.compare_digest(authorization,expected):
        raise HTTPException(401,"Acceso administrativo no autorizado.")

def valid_number(value):
    try:
        number=float(value)
        return math.isfinite(number) and number>=0
    except (TypeError,ValueError):
        return False

def product_price(product):
    price=product.get("price",0)
    if not valid_number(price):
        raise HTTPException(400,"El precio del producto no es válido.")
    return float(price)

class LoginBody(BaseModel):
    pin:str

class SettingsBody(BaseModel):
    rates:dict=Field(default_factory=dict)
    states:list=Field(default_factory=list)

class TrackingBody(BaseModel):
    code:str
    step:int=Field(ge=1,le=5)

class OrderBody(BaseModel):
    customer:dict=Field(default_factory=dict)
    items:list
    subtotal:float
    freight_fee:float
    freight_origin:str
    freight_type:str
    weight:float
    total:float
    currency:str="USD"

@app.get("/")
def home():
    index=APP_DIR/"index.html"
    if not index.exists():
        raise HTTPException(404,"No se encontró index.html.")
    return FileResponse(index)

@app.get("/health")
@app.get("/api/health")
def health():
    try:
        with connect() as conn:
            conn.execute("SELECT 1")
        return {"ok":True,"database":"connected"}
    except Exception as e:
        raise HTTPException(503,f"Database unavailable: {str(e)}")

@app.get("/api/public")
def public_data():
    config=get_config()
    with connect() as conn:
        rows=conn.execute("SELECT data FROM products ORDER BY updated_at DESC").fetchall()
    products=[r["data"] for r in rows]
    return {**config,"products":products}

@app.post("/api/admin/login")
def admin_login(body:LoginBody):
    if not ADMIN_ACCESS_CODE or not ADMIN_API_TOKEN:
        raise HTTPException(503,"Faltan las variables de acceso administrativo.")
    if not hmac.compare_digest(body.pin,ADMIN_ACCESS_CODE):
        raise HTTPException(401,"Contraseña incorrecta.")
    return {"token":ADMIN_API_TOKEN}

@app.get("/api/admin/settings")
def admin_settings(authorization:Optional[str]=Header(None)):
    require_admin(authorization)
    return get_config()

@app.put("/api/admin/settings")
def update_settings(body:SettingsBody,authorization:Optional[str]=Header(None)):
    require_admin(authorization)
    if not body.states:
        raise HTTPException(400,"Debe existir al menos un estado u origen.")
    for state in body.states:
        if not isinstance(state,dict) or not state.get("name") or not valid_number(state.get("fee")):
            raise HTTPException(400,"Revisa los nombres y tarifas de los estados.")
    for key in ("air","sea"):
        if key not in body.rates or not valid_number(body.rates[key]):
            raise HTTPException(400,f"La tarifa {key} no es válida.")
    config=get_config()
    config["rates"]={**config.get("rates",{}),**body.rates}
    config["states"]=body.states
    with connect() as conn:
        conn.execute("UPDATE app_config SET data=%s WHERE id=1",(Jsonb(config),))
        conn.commit()
    return {"ok":True,"settings":config}

@app.post("/api/admin/products")
async def save_product(
    data:str=Form(...),
    image:Optional[UploadFile]=File(None),
    authorization:Optional[str]=Header(None)
):
    require_admin(authorization)
    try:
        product=json.loads(data)
    except json.JSONDecodeError:
        raise HTTPException(400,"Los datos del producto no son JSON válido.")
    product_id=str(product.get("id") or uuid.uuid4())
    product["id"]=product_id
    name=str(product.get("name","")).strip()
    if not name:
        raise HTTPException(400,"El producto necesita un nombre.")
    product["name"]=name
    product["price"]=product_price(product)
    if image and image.filename:
        allowed={"jpg","jpeg","png","webp","gif"}
        ext=Path(image.filename).suffix.lower().lstrip(".")
        if image.content_type not in ("image/jpeg","image/png","image/webp","image/gif") or ext not in allowed:
            raise HTTPException(400,"Formato de imagen no permitido.")
        content=await image.read(MAX_IMAGE_SIZE+1)
        if len(content)>MAX_IMAGE_SIZE:
            raise HTTPException(413,"La imagen supera el límite de 8 MB.")
        filename=f"{uuid.uuid4().hex}.{ext}"
        (UPLOAD_DIR/filename).write_bytes(content)
        product["image"]=f"{PUBLIC_BASE_URL}/uploads/{filename}" if PUBLIC_BASE_URL else f"/uploads/{filename}"
    with connect() as conn:
        conn.execute("""INSERT INTO products(id,data) VALUES(%s,%s)
            ON CONFLICT(id) DO UPDATE SET data=EXCLUDED.data,updated_at=now()""",
            (product_id,Jsonb(product)))
        conn.commit()
    return {"ok":True,"product":product}

@app.delete("/api/admin/products/{product_id}")
def delete_product(product_id:str,authorization:Optional[str]=Header(None)):
    require_admin(authorization)
    with connect() as conn:
        result=conn.execute("DELETE FROM products WHERE id=%s",(product_id,))
        conn.commit()
    if result.rowcount==0:
        raise HTTPException(404,"Producto no encontrado.")
    return {"ok":True,"deleted":product_id}

@app.get("/api/trackings/{code}")
def get_tracking(code:str):
    with connect() as conn:
        row=conn.execute("SELECT data FROM trackings WHERE code=%s",(code.upper(),)).fetchone()
    if not row:
        raise HTTPException(404,"No se encontró el envío.")
    return {"code":code.upper(),**row["data"]}

@app.put("/api/admin/tracking")
def update_tracking(body:TrackingBody,authorization:Optional[str]=Header(None)):
    require_admin(authorization)
    code=body.code.strip().upper()
    if not code:
        raise HTTPException(400,"El código de seguimiento es obligatorio.")
    data={"step":body.step,"lastUpdate":datetime.now(timezone.utc).strftime("%d/%m/%Y %I:%M %p")}
    with connect() as conn:
        conn.execute("""INSERT INTO trackings(code,data) VALUES(%s,%s)
            ON CONFLICT(code) DO UPDATE SET data=EXCLUDED.data,updated_at=now()""",
            (code,Jsonb(data)))
        conn.commit()
    return {"ok":True,"code":code,**data}

@app.post("/api/orders")
def create_order(body:OrderBody):
    if not body.items:
        raise HTTPException(400,"El pedido no contiene productos.")
    amounts=[body.subtotal,body.freight_fee,body.weight,body.total]
    if not all(valid_number(x) for x in amounts):
        raise HTTPException(400,"Los importes del pedido no son válidos.")
    if not all(isinstance(item,dict) for item in body.items):
        raise HTTPException(400,"La lista de productos no es válida.")
    order_id=str(uuid.uuid4())
    created_at=datetime.now(timezone.utc).isoformat()
    data=body.dict()
    data.update({
        "order_id":order_id,
        "created_at":created_at,
        "payment_method":"Pago directo a la agencia",
        "status":"Solicitud recibida"
    })
    with connect() as conn:
        conn.execute("INSERT INTO orders(id,data) VALUES(%s,%s)",(order_id,Jsonb(data)))
        conn.commit()
    return {"ok":True,"order_id":order_id,"created_at":created_at,"status":"Solicitud recibida"}

@app.get("/api/admin/orders")
def admin_orders(authorization:Optional[str]=Header(None)):
    require_admin(authorization)
    with connect() as conn:
        rows=conn.execute("SELECT data FROM orders ORDER BY created_at DESC").fetchall()
    return {"orders":[r["data"] for r in rows]}

@app.get("/api")
def api_status():
    return {"app":"Agencia Cuba Directo","version":"1.0.0","status":"online"}

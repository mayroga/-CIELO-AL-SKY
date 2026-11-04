
import os
import json
import hmac
import uuid
import math
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from fastapi import (
    FastAPI,
    HTTPException,
    Header,
    UploadFile,
    File,
    Form,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field


# =========================================================
# CONFIGURACIÓN
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = os.getenv("DATABASE_URL", "")
ADMIN_ACCESS_CODE = os.getenv("ADMIN_ACCESS_CODE", "")
ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN", "")

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/var/data/uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

INDEX_FILE = BASE_DIR / "index.html"

MAX_IMAGE_SIZE = 8 * 1024 * 1024

ALLOWED_IMAGES = {
    "image/jpeg": {".jpg", ".jpeg"},
    "image/png": {".png"},
    "image/webp": {".webp"},
    "image/gif": {".gif"},
}


# =========================================================
# DATOS INICIALES
# =========================================================

DEFAULT_CATEGORIES = [
    {"id": "cat_ali", "name": "Alimentos",
     "subcats": ["Granos y Pastas", "Enlatados", "Cárnicos", "Lácteos"]},
    {"id": "cat_ase", "name": "Aseo e Higiene",
     "subcats": ["Personal", "Hogar y Limpieza", "Cuidado Infantil"]},
    {"id": "cat_med", "name": "Medicinas y Salud",
     "subcats": ["Analgésicos", "Primeros Auxilios", "Vitaminas"]},
    {"id": "cat_ele", "name": "Electrodomésticos",
     "subcats": ["Climatización", "Cocina", "TV y Audio"]},
    {"id": "cat_rop", "name": "Ropa y Calzado",
     "subcats": ["Hombre", "Mujer", "Niños"]},
    {"id": "cat_fer", "name": "Ferretería",
     "subcats": ["Herramientas", "Pintura", "Solar/Baterías"]},
    {"id": "cat_tec", "name": "Tecnología",
     "subcats": ["Teléfonos", "Accesorios", "Computación"]},
    {"id": "cat_rep", "name": "Repuestos Auto/Moto",
     "subcats": ["Llantas", "Baterías", "Piezas"]},
    {"id": "cat_com", "name": "Combos Especiales",
     "subcats": ["Combos Comida", "Combos Aseo", "Mix"]},
    {"id": "cat_mis", "name": "Misceláneos",
     "subcats": ["Varios", "Regalos"]},
]

DEFAULT_STATES = [
    {"name": "Florida (FL)", "fee": 0},
    {"name": "Texas (TX)", "fee": 10},
    {"name": "New York (NY)", "fee": 15},
    {"name": "California (CA)", "fee": 20},
    {"name": "New Jersey (NJ)", "fee": 12},
    {"name": "Georgia (GA)", "fee": 10},
    {"name": "Illinois (IL)", "fee": 15},
    {"name": "Otros Estados EE.UU. (50)", "fee": 25},
    {"name": "Envío Internacional (Fuera de USA)", "fee": 35},
]

DEFAULT_PRODUCTS = [
    {
        "id": 1,
        "name": "Combo Cárnico Familiar",
        "price": 85.00,
        "catId": "cat_ali",
        "subcat": "Cárnicos",
        "stock": "in_stock",
        "desc": "Incluye lomo de cerdo, pollo, picado y embutidos.",
        "img": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=400&q=80",
    },
    {
        "id": 2,
        "name": "Split Aire Acondicionado 12000 BTU",
        "price": 320.00,
        "catId": "cat_ele",
        "subcat": "Climatización",
        "stock": "in_stock",
        "desc": "Marca reconocida, alta eficiencia energética.",
        "img": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=400&q=80",
    },
    {
        "id": 3,
        "name": "Kit Aseo Personal Completo",
        "price": 45.00,
        "catId": "cat_ase",
        "subcat": "Personal",
        "stock": "in_stock",
        "desc": "Jabón, champú, crema dental y desodorantes.",
        "img": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=400&q=80",
    },
]


# =========================================================
# MODELOS DE DATOS
# =========================================================

class LoginBody(BaseModel):
    pin: str


class SettingsBody(BaseModel):
    rates: dict = Field(default_factory=dict)
    states: list = Field(default_factory=list)


class TrackingBody(BaseModel):
    code: str
    step: int = Field(ge=1, le=5)


class OrderBody(BaseModel):
    customer: dict = Field(default_factory=dict)
    items: list
    subtotal: float = Field(ge=0)
    freight_fee: float = Field(ge=0)
    freight_origin: str
    freight_type: str
    weight: float = Field(ge=0)
    total: float = Field(ge=0)
    currency: str = "USD"


# =========================================================
# APLICACIÓN FASTAPI
# =========================================================

app = FastAPI(
    title="Agencia Cuba Directo API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads",
)


# =========================================================
# CONEXIÓN POSTGRESQL
# =========================================================

def db_url():
    if not DATABASE_URL:
        raise RuntimeError(
            "Falta configurar DATABASE_URL en las variables de Render."
        )

    url = DATABASE_URL.strip()

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    return url


def connect():
    return psycopg.connect(
        db_url(),
        row_factory=dict_row,
        connect_timeout=10,
    )


def init_db():
    with connect() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS app_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                data JSONB NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                data JSONB NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS trackings (
                code TEXT PRIMARY KEY,
                data JSONB NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id UUID PRIMARY KEY,
                data JSONB NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)

        row = conn.execute(
            "SELECT data FROM app_config WHERE id = 1"
        ).fetchone()

        if not row:
            config = {
                "categories": DEFAULT_CATEGORIES,
                "states": DEFAULT_STATES,
                "rates": {
                    "air": 4.50,
                    "sea": 2.00,
                },
            }

            conn.execute(
                """
                INSERT INTO app_config (id, data)
                VALUES (1, %s)
                """,
                (Jsonb(config),),
            )

            for product in DEFAULT_PRODUCTS:
                conn.execute(
                    """
                    INSERT INTO products (id, data)
                    VALUES (%s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (str(product["id"]), Jsonb(product)),
                )

            conn.execute(
                """
                INSERT INTO trackings (code, data)
                VALUES (%s, %s)
                ON CONFLICT (code) DO NOTHING
                """,
                (
                    "CUBA-1001",
                    Jsonb({
                        "step": 3,
                        "lastUpdate": "Hoy 10:30 AM",
                    }),
                ),
            )


@app.on_event("startup")
def startup():
    init_db()


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def require_admin(authorization: Optional[str]):
    if not ADMIN_API_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="El administrador debe configurar ADMIN_API_TOKEN en Render.",
        )

    token = (authorization or "").removeprefix("Bearer ").strip()

    if not token or not hmac.compare_digest(token, ADMIN_API_TOKEN):
        raise HTTPException(
            status_code=401,
            detail="Sesión administrativa no válida.",
        )


def get_config():
    with connect() as conn:
        row = conn.execute(
            "SELECT data FROM app_config WHERE id = 1"
        ).fetchone()

    if not row:
        raise HTTPException(
            status_code=500,
            detail="No se encontró la configuración de la aplicación.",
        )

    return row["data"]


def save_config(config):
    with connect() as conn:
        conn.execute(
            """
            UPDATE app_config
            SET data = %s
            WHERE id = 1
            """,
            (Jsonb(config),),
        )


def valid_number(value):
    try:
        number = float(value)
        return math.isfinite(number) and number >= 0
    except (TypeError, ValueError):
        return False


def product_price(product):
    if not valid_number(product.get("price")):
        raise HTTPException(
            status_code=400,
            detail="El precio del producto no es válido.",
        )


# =========================================================
# PÁGINA PRINCIPAL Y SALUD DEL SERVIDOR
# =========================================================

@app.get("/")
def home():
    if not INDEX_FILE.is_file():
        raise HTTPException(
            status_code=404,
            detail="No se encontró index.html en la carpeta principal.",
        )

    return FileResponse(INDEX_FILE)


@app.get("/health")
@app.get("/api/health")
def health():
    try:
        with connect() as conn:
            conn.execute("SELECT 1")

        return {
            "ok": True,
            "database": "connected",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con PostgreSQL.",
        )


# =========================================================
# DATOS PÚBLICOS
# =========================================================

@app.get("/api/public")
def public_data():
    config = get_config()

    with connect() as conn:
        rows = conn.execute(
            """
            SELECT data
            FROM products
            ORDER BY updated_at DESC
            """
        ).fetchall()

    products = [row["data"] for row in rows]

    return {
        **config,
        "products": products,
    }


# =========================================================
# ADMINISTRACIÓN: INICIO DE SESIÓN
# =========================================================

@app.post("/api/admin/login")
def admin_login(body: LoginBody):
    if not ADMIN_ACCESS_CODE or not ADMIN_API_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="Faltan ADMIN_ACCESS_CODE o ADMIN_API_TOKEN en Render.",
        )

    if not hmac.compare_digest(
        body.pin.encode("utf-8"),
        ADMIN_ACCESS_CODE.encode("utf-8"),
    ):
        raise HTTPException(
            status_code=401,
            detail="PIN incorrecto.",
        )

    return {
        "token": ADMIN_API_TOKEN,
    }


# =========================================================
# ADMINISTRACIÓN: CONFIGURACIÓN Y TARIFAS
# =========================================================

@app.get("/api/admin/settings")
def admin_settings(
    authorization: Optional[str] = Header(default=None),
):
    require_admin(authorization)
    return get_config()


@app.put("/api/admin/settings")
def update_settings(
    body: SettingsBody,
    authorization: Optional[str] = Header(default=None),
):
    require_admin(authorization)

    if not body.states:
        raise HTTPException(
            status_code=400,
            detail="Debes incluir al menos un origen.",
        )

    for state in body.states:
        if (
            not isinstance(state, dict)
            or not state.get("name")
            or not valid_number(state.get("fee"))
        ):
            raise HTTPException(
                status_code=400,
                detail="La lista de orígenes o sus tarifas no es válida.",
            )

    rates = {
        "air": body.rates.get("air", 0),
        "sea": body.rates.get("sea", 0),
    }

    if not valid_number(rates["air"]) or not valid_number(rates["sea"]):
        raise HTTPException(
            status_code=400,
            detail="Las tarifas por libra no pueden ser negativas o inválidas.",
        )

    rates = {
        "air": float(rates["air"]),
        "sea": float(rates["sea"]),
    }

    config = get_config()
    config["rates"] = rates
    config["states"] = body.states

    save_config(config)

    return {
        "ok": True,
        "rates": rates,
        "states": body.states,
    }


# =========================================================
# ADMINISTRACIÓN: PRODUCTOS
# =========================================================

@app.post("/api/admin/products")
async def save_product(
    data: str = Form(...),
    image: Optional[UploadFile] = File(default=None),
    authorization: Optional[str] = Header(default=None),
):
    require_admin(authorization)

    try:
        product = json.loads(data)
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(
            status_code=400,
            detail="Datos del producto inválidos.",
        )

    if not isinstance(product, dict):
        raise HTTPException(
            status_code=400,
            detail="El producto debe contener un objeto válido.",
        )

    product_id = str(product.get("id") or uuid.uuid4())
    product["id"] = product_id

    if not product.get("name"):
        raise HTTPException(
            status_code=400,
            detail="El nombre del producto es obligatorio.",
        )

    product_price(product)

    if image and image.filename:
        content_type = (image.content_type or "").lower()

        if content_type not in ALLOWED_IMAGES:
            raise HTTPException(
                status_code=400,
                detail="Formato no permitido. Usa JPG, PNG, WEBP o GIF.",
            )

        raw = await image.read(MAX_IMAGE_SIZE + 1)

        if not raw:
            raise HTTPException(
                status_code=400,
                detail="La fotografía está vacía.",
            )

        if len(raw) > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="La imagen supera el límite de 8 MB.",
            )

        ext = Path(image.filename).suffix.lower()

        if ext not in ALLOWED_IMAGES[content_type]:
            ext = next(iter(ALLOWED_IMAGES[content_type]))

        filename = f"{uuid.uuid4().hex}{ext}"
        destination = UPLOAD_DIR / filename
        destination.write_bytes(raw)

        base_url = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

        if base_url:
            product["img"] = f"{base_url}/uploads/{filename}"
        else:
            product["img"] = f"/uploads/{filename}"

    with connect() as conn:
        conn.execute(
            """
            INSERT INTO products (id, data, updated_at)
            VALUES (%s, %s, NOW())
            ON CONFLICT (id)
            DO UPDATE SET
                data = EXCLUDED.data,
                updated_at = NOW()
            """,
            (product_id, Jsonb(product)),
        )

    return {
        "ok": True,
        "product": product,
    }


@app.delete("/api/admin/products/{product_id}")
def delete_product(
    product_id: str,
    authorization: Optional[str] = Header(default=None),
):
    require_admin(authorization)

    with connect() as conn:
        result = conn.execute(
            "DELETE FROM products WHERE id = %s",
            (product_id,),
        )

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado.",
        )

    return {
        "ok": True,
        "deleted": product_id,
    }


# =========================================================
# SEGUIMIENTO PÚBLICO
# =========================================================

@app.get("/api/trackings/{code}")
def get_tracking(code: str):
    normalized_code = code.strip().upper()

    with connect() as conn:
        row = conn.execute(
            """
            SELECT data
            FROM trackings
            WHERE code = %s
            """,
            (normalized_code,),
        ).fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Código de guía no encontrado.",
        )

    return {
        "code": normalized_code,
        **row["data"],
    }


# =========================================================
# ADMINISTRACIÓN: ACTUALIZAR SEGUIMIENTO
# =========================================================

@app.put("/api/admin/tracking")
def update_tracking(
    body: TrackingBody,
    authorization: Optional[str] = Header(default=None),
):
    require_admin(authorization)

    code = body.code.strip().upper()

    if not code:
        raise HTTPException(
            status_code=400,
            detail="El código de seguimiento es obligatorio.",
        )

    data = {
        "step": body.step,
        "lastUpdate": datetime.now(timezone.utc).astimezone().strftime(
            "%d/%m/%Y %I:%M %p"
        ),
    }

    with connect() as conn:
        conn.execute(
            """
            INSERT INTO trackings (code, data, updated_at)
            VALUES (%s, %s, NOW())
            ON CONFLICT (code)
            DO UPDATE SET
                data = EXCLUDED.data,
                updated_at = NOW()
            """,
            (code, Jsonb(data)),
        )

    return {
        "ok": True,
        "code": code,
        **data,
    }


# =========================================================
# PEDIDOS: REGISTRO DE SOLICITUDES
# =========================================================

@app.post("/api/orders")
def create_order(body: OrderBody):
    if not body.items:
        raise HTTPException(
            status_code=400,
            detail="El pedido no contiene productos.",
        )

    for item in body.items:
        if not isinstance(item, dict):
            raise HTTPException(
                status_code=400,
                detail="Hay un producto con datos inválidos.",
            )

    numeric_values = [
        body.subtotal,
        body.freight_fee,
        body.weight,
        body.total,
    ]

    if not all(math.isfinite(value) for value in numeric_values):
        raise HTTPException(
            status_code=400,
            detail="El pedido contiene importes inválidos.",
        )

    order_id = uuid.uuid4()

    snapshot = body.dict()

    snapshot["created_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    snapshot["order_id"] = str(order_id)

    snapshot["payment_method"] = "Pago directo a la agencia"

    snapshot["status"] = "Solicitud recibida"

    with connect() as conn:
        conn.execute(
            """
            INSERT INTO orders (id, data)
            VALUES (%s, %s)
            """,
            (order_id, Jsonb(snapshot)),
        )

    return {
        "ok": True,
        "order_id": str(order_id),
        "created_at": snapshot["created_at"],
        "message": "Solicitud registrada correctamente.",
    }


# =========================================================
# ADMINISTRACIÓN: CONSULTAR PEDIDOS
# =========================================================

@app.get("/api/admin/orders")
def admin_orders(
    authorization: Optional[str] = Header(default=None),
):
    require_admin(authorization)

    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, data, created_at
            FROM orders
            ORDER BY created_at DESC
            """
        ).fetchall()

    return {
        "orders": [
            {
                "id": str(row["id"]),
                "data": row["data"],
                "created_at": row["created_at"].isoformat(),
            }
            for row in rows
        ]
    }


# =========================================================
# INFORMACIÓN DE LA API
# =========================================================

@app.get("/api")
def api_status():
    return {
        "name": "Agencia Cuba Directo API",
        "version": "1.0.0",
        "status": "running",
    }

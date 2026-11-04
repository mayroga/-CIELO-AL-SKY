AGENCIA DE ENVIOS CUBA DIRECTO
Backend FastAPI + PostgreSQL + Render

==================================================
1. CONTENIDO DEL PROYECTO
==================================================

index.html
    Interfaz de clientes y Puesto de Mando.

main.py
    Backend de la aplicación.
    Gestiona productos, tarifas, pedidos y rastreo.

requirements.txt
    Dependencias de Python.

render.yaml
    Configuración de despliegue en Render.

README.txt
    Instrucciones del proyecto.

==================================================
2. TECNOLOGIA
==================================================

Frontend:
HTML, CSS, JavaScript y Tailwind CSS.

Backend:
Python y FastAPI.

Base de datos:
PostgreSQL.

Hosting:
Render.

Fotografías:
Almacenamiento persistente de Render.

==================================================
3. CONFIGURACION DE RENDER
==================================================

1. Crear un repositorio privado en GitHub.

2. Subir todos los archivos del proyecto
   conservando sus nombres.

3. Entrar en Render.

4. Seleccionar New + Blueprint.

5. Conectar el repositorio de GitHub.

6. Render debe reconocer render.yaml.

7. Revisar los servicios y sus costos.

8. Confirmar la creación de los recursos.

==================================================
4. VARIABLES DE ENTORNO
==================================================

DATABASE_URL
Conexión a PostgreSQL.
Se obtiene automáticamente de la base de datos.

ADMIN_ACCESS_CODE
Clave de acceso administrativo.

ADMIN_API_TOKEN
Token privado para operaciones administrativas.

IMAGE_STORAGE_PATH
Ruta de almacenamiento de fotografías:
/var/data

No publicar claves ni tokens en GitHub.

==================================================
5. ADMINISTRACION
==================================================

El Puesto de Mando debe administrar:

- Productos y mercancías.
- Precios de productos.
- Fotografías.
- Categorías y subcategorías.
- Disponibilidad de inventario.
- Tarifas aéreas.
- Tarifas marítimas.
- Recargos por estado y país.
- Rastreo de paquetes.
- Pedidos confirmados.

Los cambios publicados deben quedar guardados
en el servidor y estar disponibles para todos
los usuarios de la aplicación.

==================================================
6. FOTOGRAFIAS
==================================================

Capacidad inicial prevista:

Ropa: 150 productos.
Calzado: 150 productos.
Alimentos: 100 productos.
Aseo: 100 productos.
Otras categorías: mínimo 20 productos cada una.

El almacenamiento debe permitir ampliaciones.

Las imágenes deben guardarse en almacenamiento
persistente y no únicamente en localStorage.

==================================================
7. PEDIDOS Y TARIFAS
==================================================

Cada pedido confirmado debe conservar:

- Productos solicitados.
- Cantidades.
- Precios aplicados.
- Tipo de envío.
- Peso declarado.
- Estado o país de origen.
- Recargo aplicado.
- Total calculado.
- Fecha de confirmación.

Los cambios posteriores de tarifas no deben
modificar pedidos confirmados anteriormente.

==================================================
8. SEGURIDAD
==================================================

No utilizar un PIN administrativo fijo dentro
del código HTML.

Validar la autenticación en el backend.

Las operaciones de administración deben
requerir autorización del servidor.

No almacenar contraseñas ni tokens privados
en archivos públicos.

==================================================
9. COMPROBACION
==================================================

Después del despliegue:

Comprobar:
- /health
- Conexión con PostgreSQL.
- Acceso administrativo.
- Creación y edición de productos.
- Carga y visualización de fotografías.
- Actualización de tarifas.
- Cálculo del flete.
- Registro de pedidos.
- Consulta de rastreo.

Realizar pruebas desde dos navegadores
diferentes para comprobar que los cambios
publicados son visibles para ambos.

==================================================
FIN DEL DOCUMENTO
==================================================

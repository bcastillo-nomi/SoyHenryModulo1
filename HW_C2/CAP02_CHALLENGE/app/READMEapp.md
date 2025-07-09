# Task Manager API

Esta es una API RESTful construida con FastAPI para la gestión de tareas (Task Manager). Permite crear, listar, actualizar, eliminar tareas individuales y eliminar todas las tareas. La base de datos es una simulación en memoria, ideal para pruebas y desarrollo.

## Características

- Crear tareas
- Listar tareas (con paginación)
- Obtener detalles de una tarea por ID
- Actualizar tareas
- Eliminar tareas individuales
- Eliminar todas las tareas (con confirmación)
- Documentación automática con Swagger UI

## Estructura del Proyecto

```
app/
│
├── main.py                # Punto de entrada de la aplicación FastAPI
├── db.py                  # Simulación de base de datos en memoria (FakeDB)
├── models.py              # Modelos de datos (Pydantic)
└── routers/
    └── tasks_router.py    # Rutas relacionadas con tareas
```

## Instalación

1. **Clona el repositorio**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <CARPETA_DEL_PROYECTO>
   ```

2. **Crea un entorno virtual y actívalo**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install fastapi uvicorn
   ```

## Ejecución

Desde la carpeta `app`, ejecuta:

```bash
uvicorn main:app --reload
```

La API estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000)

La documentación interactiva estará en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints Principales

| Método | Ruta                | Descripción                                 |
|--------|---------------------|---------------------------------------------|
| GET    | `/`                 | Mensaje de bienvenida                       |
| POST   | `/tasks/`           | Crear una nueva tarea                       |
| GET    | `/tasks/`           | Listar tareas (paginado)                    |
| GET    | `/tasks/{task_id}`  | Obtener tarea por ID                        |
| PUT    | `/tasks/{task_id}`  | Actualizar tarea por ID                     |
| DELETE | `/tasks/{task_id}`  | Eliminar tarea por ID                       |
| DELETE | `/tasks/?confirm=true` | Eliminar todas las tareas (requiere confirmación) |

## Ejemplo de Modelo de Tarea

```json
{
  "id": 1,
  "title": "Comprar leche",
  "description": "Ir al supermercado y comprar leche",
  "completed": false
}
```

## Notas

- **Persistencia:** La base de datos es solo en memoria. Al reiniciar la app, se pierden los datos.
- **Eliminación masiva:** Para eliminar todas las tareas, debes pasar el parámetro `confirm=true` en la query del endpoint DELETE `/tasks/`.

## Licencia

MIT

---

Desarrollado
El siguiente challenge está diseñado para que aprendas a enfrentarte a un repositorio relativamente grande por primera vez, con la ayuda de un asistente como Cody.

## Explora
1. Crea un nuevo Chat con Cody. 
	No pude instalar Cody, pero utilice Copilot

2. Haciendo referencia al main.py dentro de /app, preguntale de qué trata el aplicativo.
* ejemplo : 
`@CAP02_CHALLENGE/path/to/file ¿Que hace esta app?`
	Esta app es una API construida con FastAPI que sirve como un "Task Manager" (gestor de tareas). Expone un endpoint raíz ("/") que devuelve un mensaje de bienvenida y utiliza un router llamado tasks_router para manejar rutas relacionadas con tareas bajo el prefijo /tasks. Esto sugiere que la app permite gestionar tareas (crear, listar, actualizar, eliminar, etc.) a través de endpoints definidos en tasks_router.

	
### Haciendo uso de Cody, encuentra las respuestas a:
- 3.1 ¿Qué hace el archivo tasks_router.py?
El archivo tasks_router.py probablemente define un router de FastAPI llamado tasks_router que agrupa y organiza las rutas relacionadas con la gestión de tareas. Este archivo suele contener endpoints para operaciones como crear, obtener, actualizar y eliminar tareas (CRUD). Luego, este router se importa y se incluye en la app principal (main.py) bajo el prefijo /tasks, lo que significa que todas las rutas definidas en tasks_router.py estarán disponibles bajo /tasks.

En resumen, tasks_router.py centraliza la lógica y las rutas para manejar tareas dentro de la API.


- 3.2 ¿Cuál es son los diferentes endpoints y que hacen?
Según el contenido de main.py, hay dos tipos de endpoints definidos:

GET /

Descripción: Endpoint raíz de la API.
Función: Devuelve un mensaje de bienvenida:
/tasks/

Descripción: Todos los endpoints relacionados con tareas están agrupados bajo el prefijo /tasks.
Función: Las rutas específicas (como crear, listar, actualizar o eliminar tareas) se definen en el archivo tasks_router.py y se acceden bajo /tasks.
Ejemplo:
/tasks/ (listar tareas)
/tasks/{id} (obtener, actualizar o eliminar una tarea específica)
/tasks/create (crear una nueva tarea)
Nota: Los endpoints exactos y sus funciones dependen de la implementación en tasks_router.py.
Resumen:

/ → Mensaje de bienvenida
/tasks/... → Endpoints para gestionar tareas (definidos en tasks_router.py)


- 3.3 ¿Cómo esta construida la base de datos?
La "base de datos" de esta app está construida como una clase llamada FakeDB, que simula una base de datos en memoria usando una lista de Python (self.tasks). No utiliza un sistema gestor de bases de datos real.

Características principales:

Almacenamiento: Las tareas se guardan en una lista (self.tasks).
Operaciones:
add_task: Agrega una tarea y le asigna un ID incremental.
get_task: Busca una tarea por su ID.
get_tasks: Devuelve todas las tareas.
update_task: Actualiza los campos de una tarea existente.
delete_task: Elimina una tarea por su ID.
Persistencia: Los datos se pierden cuando se reinicia la aplicación, ya que todo está en memoria.
Esta estructura es útil para pruebas o desarrollo, pero no para producción.



- 3.4 ¿Cómo se inicializa el aplicativo?
El aplicativo se inicializa creando una instancia de FastAPI en el archivo main.py con la línea:

```python
app = FastAPI()
```

Luego, se incluye el router de tareas (`tasks_router`) bajo el prefijo `/tasks`:

```python
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
```

Finalmente, se define un endpoint raíz (`/`) que devuelve un mensaje de bienvenida.

Para ejecutar la aplicación, normalmente se usa el siguiente comando en la terminal (desde la carpeta donde está main.py):

```powershell
uvicorn main:app --reload
```

Esto inicia el servidor y expone los endpoints definidos.


## Extiende
1. Añade un nuevo endpoint al aplicativo que permita eliminar TODOS los registros de db.
   Se agrego el nuevo endponint que elimina todas las tareas.

2. Documenta el modulo `app/routers/tasks_router.py`
	Se documento los endpoint

## Corrige
1. Encuentra 5 mejoras potenciales haciendo uso del comando "Code Smells" sobre `app/routers/tasks_router.py`
	Se analizaron las mejoras
2. Implementa alguna de las mejoras propuestas por Cody AI.
	Se implementaron las mejoras.




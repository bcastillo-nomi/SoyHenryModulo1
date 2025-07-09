# InternetWhisper

InternetWhisper es una aplicación de búsqueda y respuesta asistida por IA que utiliza modelos de lenguaje, recuperación de contexto desde la web y almacenamiento en caché vectorial para proporcionar respuestas informativas y contextuales a preguntas de los usuarios. El sistema está compuesto por varios microservicios orquestados mediante Docker y utiliza tecnologías modernas como FastAPI, Streamlit, Redis y OpenAI.

## Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Variables de Entorno](#variables-de-entorno)
- [Desarrollo y Pruebas](#desarrollo-y-pruebas)
- [Licencia](#licencia)

---

## Arquitectura

El sistema está compuesto por los siguientes servicios principales:

- **Orchestrator**: Servicio principal backend (FastAPI) que coordina la búsqueda, recuperación, procesamiento y generación de respuestas.
- **Frontend**: Interfaz de usuario basada en Streamlit para interacción tipo chat.
- **Scraper**: Servicio para obtener y renderizar páginas web, incluso aquellas que requieren JavaScript.
- **Cache**: Redis Stack, utilizado para almacenamiento y búsqueda vectorial de documentos procesados.

La comunicación entre servicios se realiza mediante HTTP y eventos Server-Sent Events (SSE).

## Características

- Búsqueda web usando la API de Google Custom Search.
- Scraping avanzado de páginas web (incluyendo soporte para JavaScript con Playwright).
- División y procesamiento inteligente de textos recuperados.
- Embeddings vectoriales usando OpenAI o un servicio remoto.
- Almacenamiento y búsqueda de contexto relevante en Redis con búsqueda vectorial.
- Interfaz de chat en tiempo real con streaming de tokens de respuesta.
- Modularidad y extensibilidad para nuevas fuentes, splitters o embeddings.

## Requisitos

- Docker y Docker Compose
- Python 3.11 (para desarrollo local)
- Claves de API para Google Custom Search y OpenAI

## Instalación

1. **Clona el repositorio**:

   ```sh
   git clone <URL_DEL_REPOSITORIO>
   cd project
   ```

2. **Configura las variables de entorno**:

   Copia el archivo `.env.example` a `.env` y completa los valores necesarios:

   ```sh
   cp .env.example .env
   ```

3. **Construye y levanta los servicios**:

   ```sh
   docker-compose up --build
   ```

   Esto levantará los servicios en los siguientes puertos por defecto:
   - Frontend: [http://localhost:8501](http://localhost:8501)
   - Orchestrator (API): [http://localhost:8000](http://localhost:8000)
   - Redis: [localhost:6379](redis://localhost:6379)

## Configuración

Asegúrate de tener las siguientes variables en tu archivo `.env`:

- `GOOGLE_API_KEY`: Tu clave de API de Google Custom Search.
- `GOOGLE_CX`: ID del motor de búsqueda personalizado.
- `OPENAI_API_KEY`: Tu clave de API de OpenAI.
- Otros valores como `GOOGLE_API_HOST`, `GOOGLE_FIELDS`, `HEADER_ACCEPT_ENCODING`, `HEADER_USER_AGENT` pueden dejarse como en el ejemplo o personalizarse.

## Uso

1. Accede a la interfaz web en [http://localhost:8501](http://localhost:8501).
2. Escribe una pregunta en el chat.
3. El sistema buscará información relevante, la procesará y generará una respuesta usando IA.
4. Los resultados de búsqueda se mostrarán como botones y la respuesta se irá generando en tiempo real.

## Estructura del Proyecto

```
project/
│
├── docker-compose.yml
├── .env.example
├── src/
│   ├── orchestrator/      # Backend principal (FastAPI, lógica de recuperación, embeddings, cache)
│   ├── frontend/          # Interfaz de usuario (Streamlit)
│   ├── scraper/           # Servicio de scraping (FastAPI + Playwright)
│
├── redis_data/            # Persistencia de datos de Redis
├── tests/                 # Pruebas unitarias
└── ...
```

### Principales componentes de código

- [`src/orchestrator/main.py`](src/orchestrator/main.py): Punto de entrada del backend, define los endpoints y la lógica de orquestación.
- [`src/frontend/main.py`](src/frontend/main.py): Lógica de la interfaz de usuario en Streamlit.
- [`src/orchestrator/retrieval/`](src/orchestrator/retrieval/): Módulos para búsqueda, embeddings, cache, scraping y splitters.
- [`src/orchestrator/models/`](src/orchestrator/models/): Modelos de datos (Pydantic).
- [`src/orchestrator/prompt/prompt.py`](src/orchestrator/prompt/prompt.py): Plantilla de prompt para el modelo de lenguaje.

## Variables de Entorno

Consulta y edita el archivo [.env.example](.env.example) para ver todas las variables necesarias. Ejemplo:

```env
HEADER_ACCEPT_ENCODING="gzip"
HEADER_USER_AGENT="Mozilla/5.0 ..."
GOOGLE_API_HOST="https://www.googleapis.com/customsearch/v1?"
GOOGLE_FIELDS="items(title, displayLink, link, snippet,pagemap/cse_thumbnail)"
GOOGLE_API_KEY=tu_api_key
GOOGLE_CX=tu_cx
OPENAI_API_KEY=tu_openai_key
```

## Desarrollo y Pruebas

- Puedes correr los servicios individualmente usando los Dockerfiles en cada subcarpeta.
- Para desarrollo local, instala las dependencias de cada servicio con `pip install -r requirements.txt`.
- Las pruebas unitarias pueden ubicarse en la carpeta [`tests/`](tests/).

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

¿Preguntas o sugerencias? Abre un issue o contacta al autor.
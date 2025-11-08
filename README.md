# Tutorial: API de Tareas con FastAPI y GraphQL

¡Bienvenido! Este repositorio contiene el código para una API de Tareas (To-Do) simple. El propósito de este tutorial es guiarte a través del código, explicar cómo funciona y cómo puedes ponerlo en marcha en tu propia máquina.

## 📜 Índice

1.  [Tecnologías Utilizadas](#-tecnologías-utilizadas)
2.  [Prerrequisitos](#-prerrequisitos)
3.  [Puesta en Marcha](#-puesta-en-marcha)
    *   [Clonar el Repositorio](#1-clonar-el-repositorio)
    *   [Crear un Entorno Virtual](#2-crear-un-entorno-virtual)
    *   [Instalar Dependencias](#3-instalar-dependencias)
4.  [Ejecutar la Aplicación](#-ejecutar-la-aplicación)
5.  [Explorando el Código](#-explorando-el-código)
    *   [`models.py`](#models-el-modelo-de-datos)
    *   [`database.py`](#database-la-conexión-a-la-base-de-datos)
    *   [`schema.py`](#schema-el-corazón-de-graphql)
    *   [`main.py`](#main-el-punto-de-entrada)
6.  [Interactuando con la API](#-interactuando-con-la-api)
    *   [Obtener todas las tareas](#obtener-todas-las-tareas)
    *   [Crear una nueva tarea](#crear-una-nueva-tarea)
    *   [Actualizar una tarea](#actualizar-una-tarea)
    *   [Eliminar una tarea](#eliminar-una-tarea)

## ✨ Tecnologías Utilizadas

*   **Python:** El lenguaje de programación principal.
*   **FastAPI:** Un framework web de alto rendimiento para construir APIs.
*   **Strawberry:** Una biblioteca para crear APIs de GraphQL de forma sencilla.
*   **SQLAlchemy:** Un ORM (Mapeador Objeto-Relacional) para interactuar con la base de datos desde Python.
*   **SQLite:** Una base de datos ligera basada en un archivo.

## ✔️ Prerrequisitos

Asegúrate de tener instalado lo siguiente en tu sistema:

*   [Python 3.7+](https://www.python.org/downloads/)
*   `pip` (el gestor de paquetes de Python)

## 🚀 Puesta en Marcha

Sigue estos pasos para configurar el proyecto en tu entorno local.

### 1. Clonar el Repositorio

```bash
git clone https://github.com/hreine/todo-api.git
cd todo-api
```

### 2. Crear un Entorno Virtual

Es una buena práctica usar un entorno virtual para aislar las dependencias del proyecto.

```bash
# Crear el entorno virtual
python -m venv .venv

# Activar el entorno (en Windows)
.venv\Scripts\activate

# Activar el entorno (en macOS/Linux)
# source .venv/bin/activate
```

### 3. Instalar Dependencias

Instala todos los paquetes necesarios que se encuentran en `requered.txt`.

```bash
pip install -r requered.txt
```

## ▶️ Ejecutar la Aplicación

Una vez instaladas las dependencias, puedes iniciar el servidor de desarrollo.

```bash
uvicorn main:app --reload
```

El comando `uvicorn` iniciará el servidor. La opción `--reload` hace que el servidor se reinicie automáticamente cada vez que detecta un cambio en el código.

¡Y listo! La API estará funcionando en `http://127.0.0.1:8000`.

## 🧠 Explorando el Código

La estructura del proyecto es simple y está diseñada para separar responsabilidades.

### `models.py`: El Modelo de Datos

Este archivo define la estructura de nuestra tabla en la base de datos.

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
```

Usamos SQLAlchemy para crear una clase `Todo` que se mapea a una tabla `todos`. Cada instancia de esta clase representará una fila en esa tabla.

### `database.py`: La Conexión a la Base de Datos

Aquí configuramos la conexión a nuestra base de datos SQLite.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URI = "sqlite:///./todos.db"

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(bind=engine) # Crea la tabla si no existe
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

`get_db` es una función de dependencia que nos proporciona una sesión de base de datos y se asegura de que se cierre correctamente después de cada solicitud.

### `schema.py`: El Corazón de GraphQL

Este es el archivo más importante para nuestra lógica de GraphQL. Define qué datos se pueden consultar y cómo se pueden modificar.

*   **`Todo` Type:** Define cómo se ve un objeto `Todo` en el esquema de GraphQL.
*   **`Query`:** Define las operaciones de lectura. En nuestro caso, `todos`, que devuelve una lista de tareas.
*   **`Mutations` (`CreateTodo`, `UpdateTodo`, `DeleteTodo`):** Definen las operaciones de escritura (crear, actualizar, eliminar). Cada mutación especifica los argumentos que recibe y lo que devuelve.

### `main.py`: El Punto de Entrada

Este archivo une todo.

```python
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from .schema import Query, CreateTodo, UpdateTodo, DeleteTodo

app = FastAPI()

# ... (configuración de CORS) ...

schema = strawberry.Schema(query=Query, mutation=Mutation) # Se combinan Query y Mutations
graphql_app = GraphQL(schema)

app.add_route("/graphql", graphql_app)
```

Aquí creamos una instancia de `FastAPI`, definimos nuestro `schema` de Strawberry combinando las consultas y mutaciones, y luego montamos la aplicación GraphQL en la ruta `/graphql`.

## 🕹️ Interactuando con la API

Para probar la API, abre tu navegador y ve a `http://127.0.0.1:8000/graphql`. Encontrarás una interfaz interactiva (GraphiQL) donde puedes ejecutar consultas y mutaciones.

### Obtener todas las tareas

```graphql
query {
  todos {
    id
    title
    description
  }
}
```

### Crear una nueva tarea

```graphql
mutation {
  createTodo(title: "Mi primera tarea", description: "Aprender GraphQL") {
    todo {
      id
      title
    }
  }
}
```

### Actualizar una tarea

(Reemplaza `"1"` con el ID de la tarea que deseas actualizar).

```graphql
mutation {
  updateTodo(id: "1", title: "Tarea actualizada") {
    todo {
      id
      title
      description
    }
  }
}
```

### Eliminar una tarea

(Reemplaza `"1"` con el ID de la tarea que deseas eliminar).

```graphql
mutation {
  deleteTodo(id: "1") {
    success
  }
}
```

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
"""
main.py
Este módulo implementa una API RESTful utilizando FastAPI que proporciona autenticación JWT y una serie de operaciones sobre listas de números enteros. Las funcionalidades principales incluyen:
- Registro y autenticación de usuarios con almacenamiento simulado en memoria.
- Generación y verificación de tokens JWT para proteger rutas.
- Algoritmos y operaciones sobre listas de números:
    - Ordenamiento (Bubble Sort)
    - Búsqueda binaria (Binary Search)
    - Filtrado de números pares
    - Suma de elementos
    - Obtención del valor máximo y mínimo
    - Cálculo de promedio y mediana
Clases:
    - Payload: Modelo para operaciones que requieren solo una lista de enteros.
    - BinarySearchPayload: Modelo para búsqueda binaria (lista de enteros y objetivo).
    - User: Modelo para registro y autenticación de usuarios.
    - Token, TokenData: Modelos para manejo de tokens JWT.
Rutas principales:
    - /register: Registro de usuario.
    - /login: Autenticación y obtención de token JWT.
    - /protected: Ruta protegida de ejemplo.
    - /bubble_sort: Ordena una lista de números usando Bubble Sort.
    - /binary_search: Realiza búsqueda binaria sobre una lista.
    - /filter_even: Filtra los números pares de una lista.
    - /sum_elements: Suma los elementos de una lista.
    - /max_value: Obtiene el valor máximo de una lista.
    - /min_value: Obtiene el valor mínimo de una lista.
    - /average: Calcula el promedio de una lista.
    - /median: Calcula la mediana de una lista.
Todas las rutas de operaciones sobre listas requieren autenticación JWT.
Incluye validaciones exhaustivas sobre los datos de entrada para asegurar la integridad y seguridad de las operaciones.
Dependencias principales:
    - fastapi
    - pydantic
    - passlib
    - jose
"""

class Payload(BaseModel):
    numbers: List[int]


class BinarySearchPayload(BaseModel):
    numbers: List[int]
    target: int

# ----- CONFIG -----

SECRET_KEY = "tu_clave_secreta_muy_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simulación de base de datos
fake_db = {"users": {}}

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ----- MODELOS -----

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# ----- UTILIDADES -----

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(username: str):
    if username in fake_db:
        return {"username": username, "hashed_password": fake_db[username]}
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

# ----- RUTAS -----

@app.post("/register")
def register(user: User):
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    fake_db[user.username] = hash_password(user.password)
    return {"msg": "Usuario registrado"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta protegida
@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return {"msg": f"Hola, {username}. Esta es una ruta protegida 🎉"}


# Bubble Sort
@app.post("/bubble_sort")
def bubble_sort(payload: Payload, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    # Validación del payload
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload inválido")
    payload = Payload(**payload)  # Convertir el dict a Payload
    
    if not payload or not isinstance(payload, Payload):
        raise HTTPException(status_code=400, detail="Payload inválido")
    if not payload.numbers or not all(isinstance(num, int) for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Lista de números inválida")
    if len(payload.numbers) == 0:
        raise HTTPException(status_code=400, detail="La lista de números no puede estar vacía")
    if len(payload.numbers) > 1000:
        raise HTTPException(status_code=400, detail="La lista de números no puede tener más de 1000 elementos")
    if not all(-1000 <= num <= 1000 for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Los números deben estar entre -1000 y 1000")
    if len(set(payload.numbers)) != len(payload.numbers):
        raise HTTPException(status_code=400, detail="La lista de números no puede contener duplicados")
    if len(payload.numbers) < 2:
        raise HTTPException(status_code=400, detail="La lista de números debe tener al menos dos elementos para ordenar")
    # Implementación del algoritmo Bubble Sort
    numbers = payload.numbers
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return {"sorted_numbers": numbers}

# Binary Search
@app.post("/binary_search")
def binary_search(payload: BinarySearchPayload, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Validación del payload
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload inválido")
    payload = BinarySearchPayload(**payload)
    if not payload or not isinstance(payload, BinarySearchPayload):
        raise HTTPException(status_code=400, detail="Payload inválido")
    if not payload.numbers or not isinstance(payload.numbers, list):
        raise HTTPException(status_code=400, detail="Lista de números inválida")
    if not all(isinstance(num, int) for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Todos los elementos de la lista deben ser enteros")
    if len(payload.numbers) == 0:
        raise HTTPException(status_code=400, detail="La lista de números no puede estar vacía")
    if len(payload.numbers) > 1000:
        raise HTTPException(status_code=400, detail="La lista de números no puede tener más de 1000 elementos")
    if not all(-1000 <= num <= 1000 for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Los números deben estar entre -1000 y 1000")
    if len(set(payload.numbers)) != len(payload.numbers):
        raise HTTPException(status_code=400, detail="La lista de números no puede contener duplicados")
    if len(payload.numbers) < 2:
        raise HTTPException(status_code=400, detail="La lista de números debe tener al menos dos elementos para buscar")
    if not isinstance(payload.target, int):
        raise HTTPException(status_code=400, detail="El objetivo debe ser un número entero")
    # Implementación del algoritmo Binary Search
    numbers = sorted(payload.numbers)  # Aseguramos que la lista esté ordenada
    target = payload.target
    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if numbers[mid] == target:
            return {"found": True, "index": mid}
        elif numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return {"found": False, "index": -1}
 
# Filtro de pares
@app.post("/filter_even")
def filter_even(payload: Payload, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Validación del payload
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload inválido")
    payload = Payload(**payload)
    
    if not payload or not isinstance(payload, Payload):
        raise HTTPException(status_code=400, detail="Payload inválido")
    if not payload.numbers or not isinstance(payload.numbers, list):
        raise HTTPException(status_code=400, detail="Lista de números inválida")
    if not all(isinstance(num, int) for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Todos los elementos de la lista deben ser enteros")
    
    even_numbers = [num for num in payload.numbers if num % 2 == 0]
    return {"even_numbers": even_numbers}



# Suma de Elementos
@app.post("/sum_elements")
def sum_elements(payload: Payload, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Validación del payload
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload inválido")
    payload = Payload(**payload)
    
    if not payload or not isinstance(payload, Payload):
        raise HTTPException(status_code=400, detail="Payload inválido")
    if not payload.numbers or not isinstance(payload.numbers, list):
        raise HTTPException(status_code=400, detail="Lista de números inválida")
    if not all(isinstance(num, int) for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Todos los elementos de la lista deben ser enteros")
    
    total_sum = sum(payload.numbers)
    return {"sum": total_sum}


# Máximo Valor
@app.post("/max_value")
def max_value(payload: Payload, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Validación del payload
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload inválido")
    payload = Payload(**payload)
    
    if not payload or not isinstance(payload, Payload):
        raise HTTPException(status_code=400, detail="Payload inválido")
    if not payload.numbers or not isinstance(payload.numbers, list):
        raise HTTPException(status_code=400, detail="Lista de números inválida")
    if not all(isinstance(num, int) for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Todos los elementos de la lista deben ser enteros")
    
    max_value = max(payload.numbers)
    return {"max_value": max_value}


# Mínimo Valor
@app.post("/min_value")
def min_value(payload: Payload, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Validación del payload
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload inválido")
    payload = Payload(**payload)
    
    if not payload or not isinstance(payload, Payload):
        raise HTTPException(status_code=400, detail="Payload inválido")
    if not payload.numbers or not isinstance(payload.numbers, list):
        raise HTTPException(status_code=400, detail="Lista de números inválida")
    if not all(isinstance(num, int) for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Todos los elementos de la lista deben ser enteros")
    
    min_value = min(payload.numbers)
    return {"min_value": min_value}

# Promedio de Elementos
@app.post("/average")
def average(payload: Payload, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Validación del payload
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload inválido")
    payload = Payload(**payload)
    
    if not payload or not isinstance(payload, Payload):
        raise HTTPException(status_code=400, detail="Payload inválido")
    if not payload.numbers or not isinstance(payload.numbers, list):
        raise HTTPException(status_code=400, detail="Lista de números inválida")
    if not all(isinstance(num, int) for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Todos los elementos de la lista deben ser enteros")
    
    average_value = sum(payload.numbers) / len(payload.numbers)
    return {"average": average_value}

# Mediana de Elementos
@app.post("/median")
def median(payload: Payload, token: str = Depends(oauth2_scheme)):  
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Validación del payload
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload inválido")
    payload = Payload(**payload)
    
    if not payload or not isinstance(payload, Payload):
        raise HTTPException(status_code=400, detail="Payload inválido")
    if not payload.numbers or not isinstance(payload.numbers, list):
        raise HTTPException(status_code=400, detail="Lista de números inválida")
    if not all(isinstance(num, int) for num in payload.numbers):
        raise HTTPException(status_code=400, detail="Todos los elementos de la lista deben ser enteros")
    
    sorted_numbers = sorted(payload.numbers)
    n = len(sorted_numbers)
    mid = n // 2
    
    if n % 2 == 0:
        median_value = (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
        median_value = sorted_numbers[mid]
    
    return {"median": median_value}


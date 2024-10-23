from fastapi import FastAPI, HTTPException, Query
from API_front_exercici.API import database  
from pydantic import BaseModel  
from typing import List, Optional  
from API_front_exercici.API import db_alumnes  # Importa funciones de la base de datos de alumnos
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # Crea una instancia de la aplicación FastAPI

class Alumno(BaseModel):  # Define un moselo de datos para un alumno usando Pydantic
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    IdAula: int

class TablaAlumne(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    DescAula: str

@app.get("/")
def read_root():
    # Ruta raíz que simplemente devuelve un mensaje de bienvenida
    return ("Bienvenido a la base de datos de alumnos")

@app.get("/alumne/list", response_model=List[TablaAlumne])
def read_alumnos(orderby: Optional[str] = Query(None, enum=["asc", "desc"]),
                 contain: Optional[str] = None, 
                 skip: int = 0, 
                 limit: Optional[int] = None):
    # Ruta GET que devuelve una lista de todos los alumnos
    alumnos = db_alumnes.list_alumnos(orderby=orderby, contain=contain, skip=skip, limit=limit)
    return alumnos

@app.get("/alumne/show/{id}")
def read_alumno(id: int):
    # Ruta GET para obtener un alunmo por su ID
    alumno = db_alumnes.get_alumno_by_id(id)
    if alumno is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")  # Maneja el caso de alumno no encontrado
    return alumno

@app.post("/alumne/add")
def add_alumno(alumno: Alumno):
    # Ruta POST para añadir un nuevo alumno, validando que el aula exisita
    if not db_alumnes.aula_exists(alumno.IdAula):
        raise HTTPException(status_code=404, detail="Aula no existe")
    result = db_alumnes.add_alumno(alumno.NomAlumne, alumno.Cicle, alumno.Curs, alumno.Grup, alumno.IdAula)
    return result

@app.put("/alumne/update/{id}")
def update_alumno(id: int, alumno: Alumno):
    # Ruta PUT para actualizar un alumno, asegurando que el aula asignada exista
    if not db_alumnes.aula_exists(alumno.IdAula):
        raise HTTPException(status_code=404, detail="Aula no existe")
    result = db_alumnes.update_alumno(id, alumno.NomAlumne, alumno.Cicle, alumno.Curs, alumno.Grup, alumno.IdAula)
    if result.get("status", 0) == -1:
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/alumne/delete/{id}")
def delete_alumno(id: int):
    # Ruta DELETE para eliminar un alumno por su ID
    resultado = db_alumnes.delete_alumno(id)
    return resultado


#Aquesta part es per evitar errors per exucutar el fetch des d'un altre origen.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Esto permite todas las origenes, ajusta según necesidades
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],
)
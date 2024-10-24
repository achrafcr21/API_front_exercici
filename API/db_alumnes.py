from API_front_exercici.API.database import db_client

def list_alumnos(orderby=None, contain=None, skip=0, limit=None):
    conn = db_client()
    query = """
    SELECT alumne.NomAlumne, alumne.Cicle, alumne.Curs, alumne.Grup, aula.DescAula 
    FROM alumne 
    JOIN aula ON alumne.IdAula = aula.IdAula
    """
    params = []

    if contain:
        query += " WHERE alumne.NomAlumne LIKE %s"
        params.append(f"%{contain}%")

    if orderby:
        query += " ORDER BY alumne.NomAlumne " + ("ASC" if orderby == "asc" else "DESC")

    if limit is not None:
        query += " LIMIT %s"
        params.append(limit)

    if skip:
        query += " OFFSET %s"
        params.append(skip)

    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)
        alumnos = cur.fetchall()
        return [{"NomAlumne": alumne["NomAlumne"],
                 "Cicle": alumne["Cicle"],
                 "Curs": alumne["Curs"],
                 "Grup": alumne["Grup"],
                 "DescAula": alumne["DescAula"]} for alumne in alumnos]
    finally:
        conn.close()
        
def get_alumno_by_id(id):
    conn = db_client()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Alumne WHERE IdAlumne = %s", (id,))  # Busca un alumno específico por ID
        alumno = cur.fetchone()  # Obtiene el primer resultado
    finally:
        conn.close()
    return alumno

def aula_exists(IdAula):
    conn = db_client()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM Aula WHERE IdAula = %s", (IdAula,))  # Verifica si una aula existe
        exists = cur.fetchone()  # Devuelve el resultado de la verificación
        return exists is not None  # Retorna True si el aula existe, False si no
    finally:
        conn.close()

def add_alumno(NomAlumne, Cicle, Curs, Grup, IdAula):
    if not aula_exists(IdAula):  # Primero verifica si el aula existe antes de añadir el alumno
        return {"status": -1, "message": "Aula no existe"}
    conn = db_client()
    try:
        cur = conn.cursor()
        # Inserta un nuevo registro de alumno en la base de datos
        cur.execute("INSERT INTO Alumne (NomAlumne, Cicle, Curs, Grup, IdAula) VALUES (%s, %s, %s, %s, %s)", 
                    (NomAlumne, Cicle, Curs, Grup, IdAula))
        conn.commit()  # Hace efectivos los cambios en la base de datos
        return {"message": "Alumno añadido correctamente", "id": cur.lastrowid}
    finally:
        conn.close()

def update_alumno(IdAlumne, NomAlumne, Cicle, Curs, Grup, IdAula):
    if not aula_exists(IdAula):
        return {"status": -1, "message": "Aula no existe"}
    conn = db_client()
    try:
        cur = conn.cursor()
        # Asegúrate de que la consulta SQL esté correctamente formateada y los parámetros sean correctos
        cur.execute(
            "UPDATE Alumne SET NomAlumne=%s, Cicle=%s, Curs=%s, Grup=%s, IdAula=%s WHERE IdAlumne=%s",
            (NomAlumne, Cicle, Curs, Grup, IdAula, IdAlumne)
        )
        conn.commit()
        if cur.rowcount == 0:
            return {"status": -1, "message": "No se encontró el alumno para actualizar"}
        return {"message": "Alumno actualizado correctamente"}
    except Exception as e:
        conn.rollback()
        return {"status": -1, "message": str(e)}
    finally:
        conn.close()

def delete_alumno(id):
    conn = db_client()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Alumne WHERE IdAlumne = %s", (id,))  # Elimina un alumno por su ID
        conn.commit()
        return {"message": "Alumno eliminado correctamente"}
    finally:
        conn.close()
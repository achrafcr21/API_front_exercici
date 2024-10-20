import mysql.connector
#configuració de la connexió a la base de dades
def db_client():
    
    try:
        dbname = "alumnat"
        user = "root"
        password = "sistem"
        host = "localhost"
        port = "3307"
        collation = "utf8mb4_general_ci"
        
        return mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = dbname,
            collation = collation
        ) 
            
    except Exception as e:
            return {"status": -1, "message": f"Error de connexió:{e}" }
    

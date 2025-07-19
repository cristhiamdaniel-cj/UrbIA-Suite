from databases import Database
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

# Obtener la contraseña desde la variable de entorno
password = os.getenv("POSTGRES_PASSWORD")

# Construir la URL de conexión
DATABASE_URL = f"postgresql://postgres:{password}@localhost/urbia"

# Instancia de conexión
database = Database(DATABASE_URL)


from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv
import os
import inspect 

# Dapatkan path dari file database.py saat ini
current_file_path = inspect.getfile(inspect.currentframe())
current_dir = os.path.dirname(os.path.abspath(current_file_path))
print(f"DEBUG: Current directory of database.py: {current_dir}")

# Coba muat .env dari direktori saat ini
dotenv_path = os.path.join(current_dir, '.env')
print(f"DEBUG: Attempting to load .env from: {dotenv_path}")
load_success = load_dotenv(dotenv_path=dotenv_path, verbose=True)
print(f"DEBUG: .env loaded successfully: {load_success}")


# Ambil DATABASE_URL dari environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DEBUG: DATABASE_URL after load_dotenv: {DATABASE_URL}") 
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():

    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created.")

def get_session():

    with Session(engine) as session:
        yield session
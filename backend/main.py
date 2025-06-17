from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, Field, SQLModel, select
from typing import Optional, List
import os
from dotenv import load_dotenv
from datetime import datetime # <--- PASTIKAN INI HANYA DI SINI, DI BAGIAN PALING ATAS FILE

# Impor fungsi dan objek dari database.py
from .database import engine, create_db_and_tables, get_session
# Impor fungsi dari gemini_ai.py
from .gemini_ai import generate_content_with_gemini

# Muat variabel lingkungan dari file .env
load_dotenv()

app = FastAPI()

# --- Bagian CORS ---
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    # Tambahkan domain frontend kamu jika sudah di-deploy
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Akhir Bagian CORS ---

# ====================================================================
# Definisi Model Data
# ====================================================================

class ContentBase(SQLModel):
    title: str
    keywords: str
    content_type: str # e.g., "article", "product_description", "social_media_post", "email_promotion"
    tone: str # e.g., "formal", "casual", "persuasive", "informative"
    audience: str # e.g., "professional", "teenager", "general"
    length: str # e.g., "short", "medium", "long"
    generated_text: str = Field(default="") # Set default ke string kosong
    
    # created_at: Optional[datetime] = Field(default_factory=datetime.now, index=True)
    # ^^^ Baris ini benar. PASTIKAN TIDAK ADA LAGI "from datetime import datetime" DI SINI.
    created_at: Optional[datetime] = Field(default_factory=datetime.now, index=True)


class Content(ContentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ContentCreate(SQLModel): # Ini model untuk input dari frontend, tidak ada generated_text
    title: str
    keywords: str
    content_type: str
    tone: str
    audience: str
    length: str

class ContentRead(ContentBase): # Ini model untuk respons GET/POST agar ID juga muncul
    id: int
    # created_at: datetime # Jika ingin menampilkan datetime object langsung, ini bisa. Defaultnya sudah OK


# ====================================================================
# Event Handler Saat Aplikasi Startup
# ====================================================================

@app.on_event("startup")
def on_startup():
    """
    Fungsi yang akan dijalankan saat aplikasi FastAPI pertama kali dimulai.
    Digunakan untuk membuat tabel database jika belum ada.
    """
    create_db_and_tables()

# ====================================================================
# Endpoint API Anda
# ====================================================================

@app.get("/")
async def read_root():
    return {"message": "Selamat datang di Backend Content Generation AI dengan FastAPI!"}

@app.get("/api/hello")
async def hello_world():
    return {"message": "Hello from FastAPI!"}

# --- Endpoint untuk membuat dan menyimpan konten ---
@app.post("/api/contents/", response_model=ContentRead)
async def create_content(
    *,
    session: Session = Depends(get_session),
    content_input: ContentCreate # Menggunakan model ContentCreate untuk validasi input
):
    """
    Endpoint untuk menghasilkan konten dengan AI dan menyimpannya ke database.
    """
    try:
        # Panggil fungsi generate_content_with_gemini dari gemini_ai.py
        generated_text = await generate_content_with_gemini(
            title=content_input.title,
            keywords=content_input.keywords,
            content_type=content_input.content_type,
            tone=content_input.tone,
            audience=content_input.audience,
            length=content_input.length
        )

        # Buat objek Content lengkap dengan teks yang dihasilkan oleh AI
        content_to_save = Content(
            title=content_input.title,
            keywords=content_input.keywords,
            content_type=content_input.content_type,
            tone=content_input.tone,
            audience=content_input.audience,
            length=content_input.length,
            generated_text=generated_text # Teks yang dihasilkan AI dimasukkan di sini
        )

        session.add(content_to_save) # Tambahkan ke sesi database
        session.commit() # Simpan perubahan ke database
        session.refresh(content_to_save) # Refresh objek untuk mendapatkan ID dan data terbaru dari database
        return content_to_save
    except ValueError as e:
        # Mengembalikan error HTTP 400 jika ada masalah dengan input atau konfigurasi API
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Menangkap error umum dan mengembalikan error HTTP 500
        # Sangat disarankan untuk melakukan logging error ini di lingkungan produksi
        print(f"Error during content generation or saving: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate or save content due to an internal server error.")


# --- Endpoint untuk mendapatkan semua konten yang disimpan ---
@app.get("/api/contents/", response_model=List[ContentRead])
async def read_contents(session: Session = Depends(get_session)):
    """
    Endpoint untuk mendapatkan semua riwayat konten yang disimpan.
    """
    contents = session.exec(select(Content)).all() # Mengambil semua objek Content dari database
    return contents


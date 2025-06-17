Content AI Generator
Aplikasi web full-stack untuk menghasilkan konten teks otomatis menggunakan Google Gemini API. Dibuat untuk demonstrasi keahlian pengembangan software engineering dan integrasi AI.

    ✨ Fitur
    - Generasi Konten AI: Buat artikel, deskripsi produk, postingan media sosial, dll.

    - Kustomisasi Output: Atur tone, audiens, panjang, judul, dan kata kunci.

    - Riwayat & Editor: Simpan riwayat konten dan edit hasilnya langsung.

    - UI Modern: Antarmuka yang bersih dan responsif.

    - Landing Page: Halaman pengantar aplikasi yang interaktif.

    🚀 Teknologi
    - Frontend: Vue.js, SCSS, Axios, date-fns, Font Awesome

    - Backend: Python, FastAPI, SQLModel, Uvicorn, python-dotenv

    - Database: PostgreSQL

    - AI: Google Gemini API (model gemini-1.5-flash atau gemini-1.5-pro)

    ⚙️ Cara Menjalankan
    - Prasyarat
    - Python 3.8+
    - Node.js & npm
    - PostgreSQL
    - Git

Langkah-langkah
Klon Repositori:

git clone https://github.com/mangriza/content-ai-generator.git
cd content-ai-generator


    Setup Backend:

    - Buat dan aktifkan venv: python -m venv venv lalu .\venv\Scripts\activate (Windows) / source venv/bin/activate (macOS/Linux).

    - Instal dependensi: pip install fastapi uvicorn "psycopg2-binary<2.10" python-dotenv sqlalchemy sqlmodel google-generativeai

    - Buat content_ai_db di PostgreSQL.

    - Buat file backend/.env dengan isi:

    - DATABASE_URL="postgresql://postgres:your_postgres_password@localhost/content_ai_db"
    GEMINI_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"

Jalankan server (dari root proyek): uvicorn backend.main:app --reload --port 8000

Setup Frontend:

Masuk folder: cd frontend

Instal dependensi: npm install

Jalankan server: npm run serve

Aplikasi akan berjalan di http://localhost:8080 dan backend di http://localhost:8000 (http://localhost:8000/docs untuk dokumentasi API).

![alt text](image.png)


![alt text](image-1.png)




import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_model():
    available_models = []
    try:
        print("\n--- Listing Available Gemini Models ---")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and "vision" not in m.name:
                print(f"Model Name: {m.name}, Methods: {m.supported_generation_methods}")
                available_models.append(m.name)
        print("-------------------------------------\n")
    except Exception as e:
        print(f"Error listing models: {e}")
        raise Exception(f"Failed to list Gemini models. Check your API Key and network. Error: {e}")


    preferred_models_order = ['gemini-1.5-flash', 'gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-pro'] 

    selected_model_name = None
    for p_model_name in preferred_models_order:
        if f"models/{p_model_name}" in available_models:
            selected_model_name = p_model_name
            break

    if selected_model_name:
        print(f"Using preferred model: {selected_model_name}")
        return genai.GenerativeModel(selected_model_name)

    if available_models:
        first_available_text_model = available_models[0].replace("models/", "")
        print(f"Using first available text model: {first_available_text_model}")
        return genai.GenerativeModel(first_available_text_model)

    raise ValueError("No suitable Gemini model found for text generation. Please check your API Key and Google AI Studio settings.")


# Bagian async def generate_content_with_gemini tetap sama
async def generate_content_with_gemini(
    title: str,
    keywords: str,
    content_type: str,
    tone: str,
    audience: str,
    length: str
) -> str:
    # ... (kode ini tetap sama)
    model = get_gemini_model() 
    prompt = f"""
    Buatkan {content_type} yang menarik dan relevan.

    Detail Konten:
    - Judul: {title}
    - Kata Kunci Utama: {keywords}
    - Target Audiens: {audience}
    - Tone (Nada): {tone}
    - Panjang: {length}

    Instruksi Tambahan:
    - Pastikan kontennya koheren, informatif, dan mudah dibaca.
    - Sesuaikan gaya bahasa dengan target audiens dan tone yang diminta.
    - Jika {content_type} adalah 'artikel', buatlah dalam bentuk paragraf-paragraf yang mengalir.
    - Jika {content_type} adalah 'deskripsi produk', fokus pada fitur dan manfaat.
    - Jika {content_type} adalah 'postingan media sosial', buatlah singkat, padat, dan menarik perhatian.
    - Jika {content_type} adalah 'email promosi', buatlah persuasif dan panggil tindakan (call to action).
    - Jangan sertakan salam pembuka atau penutup yang berlebihan, langsung ke intinya kecuali diminta.
    - Hasilnya hanya berupa teks konten.
    """

    try:
        # Menggunakan generate_content untuk mendapatkan respons dari Gemini
        response = await model.generate_content_async(prompt)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise Exception(f"Failed to generate content: {str(e)}")
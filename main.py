from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import json
import requests
from typing import Optional
import pdfplumber
from docx import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Recruitment Agent", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Default job posting
DEFAULT_JOB = {
    "title": "Desarrollador Full Stack Senior",
    "description": """
    Buscamos un Desarrollador Full Stack Senior con experiencia en:
    
    Requisitos:
    - 5+ años de experiencia en desarrollo web
    - Dominio de JavaScript/TypeScript, React, Node.js
    - Experiencia con bases de datos SQL y NoSQL
    - Conocimientos de AWS o servicios cloud
    - Experiencia con metodologías ágiles
    - Capacidad de liderar equipos técnicos
    
    Responsabilidades:
    - Desarrollar aplicaciones web escalables
    - Diseñar arquitecturas de software
    - Mentorizar desarrolladores junior
    - Participar en code reviews
    - Colaborar con equipos de producto
    
    Tecnologías:
    - Frontend: React, TypeScript, HTML5, CSS3
    - Backend: Node.js, Python, Express/FastAPI
    - Base de datos: PostgreSQL, MongoDB
    - Cloud: AWS, Docker, Kubernetes
    """
}

# Store jobs in memory (in production, use a database)
jobs = [DEFAULT_JOB]

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading DOCX: {str(e)}")

def analyze_cv_with_gemini(cv_text: str, job_description: str, api_key_override: Optional[str] = None) -> dict:
    """Analyze CV using Gemini API"""
    api_key = api_key_override or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Error: la API key es inválida o está mal configurada. Verifica tu clave de acceso.")
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
    Analiza la compatibilidad entre el siguiente CV y la descripción de la vacante.
    
    CV DEL CANDIDATO:
    {cv_text}
    
    DESCRIPCIÓN DE LA VACANTE:
    {job_description}
    
    Por favor, evalúa y responde en el siguiente formato JSON:
    {{
        "calificacion": "Muy compatible" | "Compatible" | "No compatible",
        "recomendacion": "Agendar entrevista" | "Revisar por reclutador" | "Descartar",
        "justificacion": "Explicación breve de la decisión basada en habilidades, experiencia y requisitos",
        "mensaje_candidato": "Mensaje personalizado para el candidato, con retroalimentación positiva o sugerencias de mejora, en tono cordial y constructivo. Si es para agendar entrevista, motívalo y felicítalo. Si es para retroalimentación, sugiere en qué puede mejorar para futuras oportunidades."
    }}
    
    Considera:
    - Experiencia relevante
    - Habilidades técnicas requeridas
    - Años de experiencia
    - Compatibilidad con la cultura y responsabilidades
    - Sé cordial y constructivo en el mensaje al candidato
    """
    
    try:
        print(f"DEBUG: Calling Gemini API with key: {api_key[:10]}...")
        response = requests.post(url, json={
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        })
        print(f"DEBUG: Response status: {response.status_code}")
        
        if response.status_code == 401 or response.status_code == 403:
            raise HTTPException(status_code=500, detail="Error: la API key es inválida o está mal configurada. Verifica tu clave de acceso.")
        if response.status_code == 429:
            return {
                "calificacion": "No disponible",
                "recomendacion": "Intenta más tarde",
                "justificacion": "Límite de uso de la API alcanzado. Por favor, intenta nuevamente más tarde."
            }
        if response.status_code == 400:
            try:
                error_json = response.json()
                if "error" in error_json and (
                    "API key not valid" in error_json["error"].get("message", "") or
                    error_json["error"].get("reason", "") == "API_KEY_INVALID"
                ):
                    print("[GEMINI API ERROR]", json.dumps(error_json["error"], indent=2, ensure_ascii=False))
                    raise HTTPException(status_code=500, detail="Error: la API key es inválida o está mal configurada. Verifica tu clave de acceso.")
            except Exception:
                pass
        if response.status_code != 200:
            try:
                error_json = response.json()
                if "error" in error_json and (
                    "API key" in error_json["error"].get("message", "") or
                    "invalid" in error_json["error"].get("message", "") or
                    "expired" in error_json["error"].get("message", "") or
                    error_json["error"].get("reason", "") == "API_KEY_INVALID"
                ):
                    print("[GEMINI API ERROR]", json.dumps(error_json["error"], indent=2, ensure_ascii=False))
                    raise HTTPException(status_code=500, detail="Error: la API key es inválida o está mal configurada. Verifica tu clave de acceso.")
            except Exception:
                pass
            print(f"DEBUG: Error calling Gemini API: {response.status_code}")
            raise HTTPException(status_code=500, detail="Ocurrió un error inesperado al comunicarse con Gemini API. Revisa la API KEY e intenta más tarde.")
        
        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            # Try to parse JSON from response
            try:
                # Extract JSON from the response text
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    # Fallback: parse manually
                    return {
                        "calificacion": "Compatible",
                        "recomendacion": "Revisar por reclutador",
                        "justificacion": content
                    }
            except json.JSONDecodeError:
                return {
                    "calificacion": "Compatible",
                    "recomendacion": "Revisar por reclutador",
                    "justificacion": content
                }
        else:
            raise HTTPException(status_code=500, detail="Invalid response from Gemini API")
            
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling Gemini API: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with CV upload form"""
    return templates.TemplateResponse("index.html", {"request": request, "jobs": jobs})

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    """Admin page for managing job postings"""
    return templates.TemplateResponse("admin.jinja2", {"request": request, "jobs": jobs})

@app.post("/upload-cv")
async def upload_cv(
    file: UploadFile = File(...),
    job_index: int = Form(0),
    api_key: str = Form(None)
):
    """Upload and analyze CV"""
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Validate file type
    if not file.filename or not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")
    
    # Validate job index
    if job_index >= len(jobs):
        raise HTTPException(status_code=400, detail="Invalid job index")
    
    # Save file temporarily
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            cv_text = extract_text_from_pdf(file_path)
        else:
            cv_text = extract_text_from_docx(file_path)
        
        if not cv_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        # Analyze with Gemini
        job_description = jobs[job_index]["description"]
        analysis_result = analyze_cv_with_gemini(cv_text, job_description, api_key_override=api_key)
        
        # Fallback para mensaje_candidato
        if 'mensaje_candidato' not in analysis_result or not analysis_result['mensaje_candidato']:
            if analysis_result.get('recomendacion') == 'Agendar entrevista':
                analysis_result['mensaje_candidato'] = '¡Felicidades! Tu perfil es muy relevante para la vacante. Pronto nos pondremos en contacto para agendar una entrevista.'
            elif analysis_result.get('recomendacion') == 'Revisar por reclutador':
                analysis_result['mensaje_candidato'] = 'Gracias por tu interés. Tu perfil será revisado por nuestro equipo y podríamos contactarte para próximos pasos.'
            else:
                analysis_result['mensaje_candidato'] = 'Gracias por postularte. Te sugerimos fortalecer tu experiencia y habilidades para futuras oportunidades.'
        
        # Clean up file
        os.remove(file_path)
        
        return {
            "filename": file.filename,
            "job_title": jobs[job_index]["title"],
            "analysis": analysis_result
        }
        
    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise e

@app.post("/add-job")
async def add_job(
    title: str = Form(...),
    description: str = Form(...)
):
    """Add a new job posting"""
    new_job = {
        "title": title,
        "description": description
    }
    jobs.append(new_job)
    return {"message": "Job added successfully", "job": new_job}

@app.put("/edit-job/{job_index}")
async def edit_job(
    job_index: int,
    title: str = Form(...),
    description: str = Form(...)
):
    """Edit an existing job posting"""
    if job_index >= len(jobs):
        raise HTTPException(status_code=400, detail="Invalid job index")
    
    jobs[job_index] = {
        "title": title,
        "description": description
    }
    return {"message": "Job updated successfully", "job": jobs[job_index]}

@app.delete("/delete-job/{job_index}")
async def delete_job(job_index: int):
    """Delete a job posting"""
    if job_index >= len(jobs):
        raise HTTPException(status_code=400, detail="Invalid job index")
    
    if len(jobs) <= 1:
        raise HTTPException(status_code=400, detail="Cannot delete the last job")
    
    deleted_job = jobs.pop(job_index)
    return {"message": "Job deleted successfully", "job": deleted_job}

@app.get("/jobs")
async def get_jobs():
    """Get all job postings"""
    return {"jobs": jobs} 
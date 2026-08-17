import os
from fastapi import FastAPI, HTTPException, Depends, Header, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

from pydantic import BaseModel, EmailStr
from typing import Optional

from backend.database import init_db, get_user_by_email, get_user_by_id, create_user
from backend.auth import (
    hash_password, verify_password, create_access_token,
    decode_access_token, verify_google_token
)

app = FastAPI(title="iLovePDF - Fullstack PDF Management Platform", version="1.0.0")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# Initialize Database tables
init_db()

# Mounting static files and templates safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

if not os.path.exists(TEMPLATES_DIR):
    cwd_templates = os.path.join(os.getcwd(), "templates")
    if os.path.exists(cwd_templates):
        TEMPLATES_DIR = cwd_templates

if not os.path.exists(STATIC_DIR):
    cwd_static = os.path.join(os.getcwd(), "static")
    if os.path.exists(cwd_static):
        STATIC_DIR = cwd_static

@app.get("/static/{filepath:path}")
def serve_static_file(filepath: str):
    candidates = [
        os.path.join(BASE_DIR, "static", filepath),
        os.path.join(os.getcwd(), "static", filepath),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", filepath),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", filepath),
        os.path.join("/var/task", "static", filepath),
        os.path.join("/var/task", filepath)
    ]
    for p in candidates:
        if os.path.exists(p) and os.path.isfile(p):
            return FileResponse(p)
    raise HTTPException(status_code=404, detail=f"Static file '{filepath}' not found")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

if not os.path.exists(TEMPLATES_DIR):
    cwd_templates = os.path.join(os.getcwd(), "templates")
    if os.path.exists(cwd_templates):
        TEMPLATES_DIR = cwd_templates

if not os.path.exists(STATIC_DIR):
    cwd_static = os.path.join(os.getcwd(), "static")
    if os.path.exists(cwd_static):
        STATIC_DIR = cwd_static

if os.path.exists(STATIC_DIR):
    try:
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    except Exception:
        pass

if os.path.exists(TEMPLATES_DIR):
    try:
        templates = Jinja2Templates(directory=TEMPLATES_DIR)
    except Exception:
        templates = None
else:
    templates = None

# Pydantic Schemas
class RegisterSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class GoogleAuthSchema(BaseModel):
    credential: str

class DemoGoogleAuthSchema(BaseModel):
    email: EmailStr
    full_name: str
    picture: Optional[str] = None

# Dependency to get current user from Bearer Token
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    user_id = int(payload.get("sub"))
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found"
        )
    return user

def get_template_html(filename: str) -> Optional[str]:
    candidates = [
        os.path.join(BASE_DIR, "templates", filename),
        os.path.join(os.getcwd(), "templates", filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", filename),
        os.path.join("/var/task", "templates", filename),
        os.path.join("/var/task", filename)
    ]
    for p in candidates:
        if os.path.exists(p) and os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content and len(content.strip()) > 0:
                        return content
            except Exception:
                pass
    return None

# Routes
@app.get("/")
@app.get("/api")
@app.get("/api/index")
def read_root(request: Request):
    html_content = get_template_html("index.html")
    if html_content:
        return HTMLResponse(content=html_content)
    if templates and TEMPLATES_DIR and os.path.exists(os.path.join(TEMPLATES_DIR, "index.html")):
        try:
            return templates.TemplateResponse(request=request, name="index.html")
        except Exception:
            pass
    return HTMLResponse("<!DOCTYPE html><html><head><title>PDFCraft</title></head><body><h1>PDFCraft Backend Active</h1></body></html>")

@app.get("/auth")
@app.get("/login")
def read_auth(request: Request):
    html_content = get_template_html("auth.html")
    if html_content:
        return HTMLResponse(content=html_content)
    if templates and TEMPLATES_DIR and os.path.exists(os.path.join(TEMPLATES_DIR, "auth.html")):
        try:
            return templates.TemplateResponse(request=request, name="auth.html")
        except Exception:
            pass
    return HTMLResponse("<!DOCTYPE html><html><head><title>PDFCraft Auth</title></head><body><h1>PDFCraft Auth</h1></body></html>")

@app.post("/api/auth/register")
def register(data: RegisterSchema):
    existing_user = get_user_by_email(data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists"
        )
    
    if len(data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )
    
    hashed = hash_password(data.password)
    user = create_user(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hashed,
        auth_provider="email"
    )
    
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    return {
        "message": "User registered successfully",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "auth_provider": user["auth_provider"],
            "picture": user["picture"]
        }
    }

@app.post("/api/auth/login")
def login(data: LoginSchema):
    user = get_user_by_email(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if user["auth_provider"] == "google" and not user["hashed_password"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account uses Google Sign-In. Please sign in with Google."
        )
    
    if not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "auth_provider": user["auth_provider"],
            "picture": user["picture"]
        }
    }

@app.post("/api/auth/google")
def google_auth(data: GoogleAuthSchema):
    google_user = verify_google_token(data.credential)
    if not google_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired Google Token"
        )
    
    email = google_user["email"]
    name = google_user["name"]
    picture = google_user.get("picture")
    
    user = get_user_by_email(email)
    if not user:
        user = create_user(
            email=email,
            full_name=name,
            hashed_password=None,
            auth_provider="google",
            picture=picture
        )
    
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    return {
        "message": "Google authentication successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "auth_provider": user["auth_provider"],
            "picture": user["picture"]
        }
    }

@app.post("/api/auth/google-demo")
def google_demo_auth(data: DemoGoogleAuthSchema):
    """
    Demo endpoint allowing instant testing of Google Authentication flow.
    """
    user = get_user_by_email(data.email)
    if not user:
        user = create_user(
            email=data.email,
            full_name=data.full_name,
            hashed_password=None,
            auth_provider="google",
            picture=data.picture or f"https://api.dicebear.com/7.x/avataaars/svg?seed={data.email}"
        )
    
    token = create_access_token({"sub": user["id"], "email": user["email"]})
    return {
        "message": "Google Authentication Successful (Demo Mode)",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "auth_provider": user["auth_provider"],
            "picture": user["picture"]
        }
    }

@app.get("/api/auth/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "auth_provider": current_user["auth_provider"],
        "picture": current_user["picture"],
        "created_at": current_user["created_at"]
    }

# ==========================================================
# REAL PDF PROCESSING API ENDPOINT
# ==========================================================
import tempfile
import uuid
from typing import List
from fastapi import UploadFile, File, Form
from fastapi.responses import FileResponse
from backend import pdf_processor

@app.post("/api/pdf/process")
async def process_pdf(
    files: List[UploadFile] = File(...),
    tool: str = Form(...),
    password: Optional[str] = Form(""),
    degrees: Optional[int] = Form(90),
    watermark_text: Optional[str] = Form("PDFCraft"),
    pages_to_delete: Optional[str] = Form(""),
    position: Optional[str] = Form("bottom-right"),
    page_map: Optional[str] = Form("")
):

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    temp_dir = tempfile.mkdtemp(prefix="pdfcraft_")
    saved_paths = []

    try:
        for file in files:
            file_ext = os.path.splitext(file.filename)[1]
            temp_input_path = os.path.join(temp_dir, f"input_{uuid.uuid4().hex[:8]}{file_ext}")
            with open(temp_input_path, "wb") as f:
                content = await file.read()
                f.write(content)
            saved_paths.append(temp_input_path)

        first_filename = os.path.splitext(files[0].filename)[0]

        if tool in ["merge", "merge_pdf"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_merged.pdf")
            pdf_processor.process_merge_pdfs(saved_paths, out_file)
            media_type = "application/pdf"
            download_name = "pdfcraft_merged.pdf"

        elif tool in ["split", "split_pdf"]:
            out_file = pdf_processor.process_split_pdf(saved_paths[0], temp_dir)
            media_type = "application/zip"
            download_name = f"{first_filename}_split.zip"

        elif tool in ["compress", "compress_pdf"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_compressed.pdf")
            pdf_processor.process_compress_pdf(saved_paths[0], out_file)
            media_type = "application/pdf"
            download_name = f"{first_filename}_compressed.pdf"

        elif tool in ["pdf2word", "pdf_to_word", "pdf_to_docx"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_converted.docx")
            pdf_processor.process_pdf_to_word(saved_paths[0], out_file)
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            download_name = f"{first_filename}.docx"

        elif tool in ["word2pdf", "word_to_pdf", "docx_to_pdf"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_converted.pdf")
            pdf_processor.process_word_to_pdf(saved_paths[0], out_file)
            media_type = "application/pdf"
            download_name = f"{first_filename}.pdf"

        elif tool in ["pdf2excel", "pdf_to_excel"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_data.xlsx")
            pdf_processor.process_pdf_to_excel(saved_paths[0], out_file)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            download_name = f"{first_filename}_data.xlsx"

        elif tool in ["excel2pdf", "excel_to_pdf"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_table.pdf")
            pdf_processor.process_excel_to_pdf(saved_paths[0], out_file)
            media_type = "application/pdf"
            download_name = f"{first_filename}_table.pdf"

        elif tool in ["pdf2ppt", "pdf_to_ppt", "pdf_to_powerpoint"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_slides.pptx")
            pdf_processor.process_pdf_to_ppt(saved_paths[0], out_file)
            media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            download_name = f"{first_filename}_slides.pptx"

        elif tool in ["edit", "edit_pdf", "annotate"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_edited.pdf")
            pdf_processor.process_edit_pdf(saved_paths[0], out_file)
            media_type = "application/pdf"
            download_name = f"{first_filename}_edited.pdf"

        elif tool in ["sign", "e_sign", "esign"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_signed.pdf")
            pdf_processor.process_esign_pdf(saved_paths[0], out_file)
            media_type = "application/pdf"
            download_name = f"{first_filename}_signed.pdf"

        elif tool in ["ai", "ai_summarize", "summarize"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_ai_summary.txt")
            pdf_processor.process_ai_summarize(saved_paths[0], out_file)
            media_type = "text/plain"
            download_name = f"{first_filename}_ai_summary.txt"

        elif tool in ["protect", "encrypt"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_protected.pdf")
            pdf_processor.process_protect_pdf(saved_paths[0], out_file, password=password or "pdfcraft")
            media_type = "application/pdf"
            download_name = f"{first_filename}_protected.pdf"

        elif tool in ["unlock", "decrypt"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_unlocked.pdf")
            pdf_processor.process_unlock_pdf(saved_paths[0], out_file, password=password or "")
            media_type = "application/pdf"
            download_name = f"{first_filename}_unlocked.pdf"

        elif tool in ["watermark", "watermark_pdf"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_watermarked.pdf")
            pdf_processor.process_watermark_pdf(saved_paths[0], out_file, watermark_text=watermark_text or "PDFCraft")
            media_type = "application/pdf"
            download_name = f"{first_filename}_watermarked.pdf"

        elif tool in ["rotate", "rotate_pdf"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_rotated.pdf")
            pdf_processor.process_rotate_pdf(saved_paths[0], out_file, degrees=int(degrees or 90))
            media_type = "application/pdf"
            download_name = f"{first_filename}_rotated.pdf"

        elif tool in ["jpg_to_pdf", "images_to_pdf"]:
            out_file = os.path.join(temp_dir, "converted_images.pdf")
            pdf_processor.process_images_to_pdf(saved_paths, out_file)
            media_type = "application/pdf"
            download_name = "pdfcraft_images.pdf"

        elif tool in ["extract_text", "pdf2txt"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_text.txt")
            pdf_processor.process_extract_text(saved_paths[0], out_file)
            media_type = "text/plain"
            download_name = f"{first_filename}_extracted.txt"

        elif tool in ["page_numbers", "add_page_numbers"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_numbered.pdf")
            pdf_processor.process_page_numbers(saved_paths[0], out_file, position=position or "bottom-right")
            media_type = "application/pdf"
            download_name = f"{first_filename}_numbered.pdf"

        elif tool in ["delete_pages", "remove_pages"]:
            out_file = os.path.join(temp_dir, f"{first_filename}_organized.pdf")
            pdf_processor.process_delete_pages(saved_paths[0], out_file, pages_to_delete=pages_to_delete or "")
            media_type = "application/pdf"
            download_name = f"{first_filename}_organized.pdf"

        elif tool in ["reorder", "reorder_pdf", "canvas_studio", "visual_studio"]:
            import json
            map_data = []
            if page_map:
                try:
                    map_data = json.loads(page_map)
                except Exception:
                    pass
            out_file = os.path.join(temp_dir, f"{first_filename}_canvas_studio.pdf")
            pdf_processor.process_reorder_pdf(saved_paths[0], out_file, map_data)
            media_type = "application/pdf"
            download_name = f"{first_filename}_canvas_studio.pdf"


        else:
            out_file = os.path.join(temp_dir, f"{first_filename}_processed.pdf")
            pdf_processor.process_compress_pdf(saved_paths[0], out_file)
            media_type = "application/pdf"
            download_name = f"{first_filename}_processed.pdf"

        headers = {
            "Content-Disposition": f'attachment; filename="{download_name}"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
        return FileResponse(
            path=out_file,
            filename=download_name,
            media_type=media_type,
            headers=headers
        )

    except Exception as e:
        print("PDF processing error:", e)
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")



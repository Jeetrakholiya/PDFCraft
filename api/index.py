import os
import sys

# Ensure root project directory is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

try:
    from backend.main import app
except Exception as err:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    app = FastAPI(title="PDFCraft Fallback Engine")
    
    @app.get("/{full_path:path}")
    def catch_all(full_path: str):
        return HTMLResponse(
            f"<!DOCTYPE html><html><head><title>PDFCraft Status</title></head>"
            f"<body style='font-family:sans-serif;padding:2rem;background:#0f172a;color:#f8fafc;'>"
            f"<h2>PDFCraft Serverless Engine Active</h2>"
            f"<p>Diagnostic message: <code>{err}</code></p>"
            f"</body></html>"
        )

import os
import sys

# Ensure root directory is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

try:
    from backend.main import app
    handler = app
except Exception as err:
    import traceback
    tb_str = traceback.format_exc()
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    app = FastAPI(title="PDFCraft Error Diagnostic")
    handler = app
    
    @app.get("/{full_path:path}")
    def catch_all(full_path: str):
        return HTMLResponse(
            f"<!DOCTYPE html><html><head><title>PDFCraft Diagnostic</title></head>"
            f"<body style='font-family:sans-serif;padding:2rem;background:#0f172a;color:#f8fafc;'>"
            f"<h2 style='color:#f87171;'>PDFCraft Startup Diagnostic</h2>"
            f"<pre style='color:#fca5a5;background:#1e293b;padding:1rem;border-radius:0.5rem;overflow:auto;'>{tb_str}</pre>"
            f"</body></html>"
        )

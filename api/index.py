import os
import sys
import traceback

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

try:
    from backend.main import app
except Exception as err:
    tb_str = traceback.format_exc()
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    app = FastAPI(title="PDFCraft Error Diagnostic")
    
    @app.get("/{full_path:path}")
    def catch_all(full_path: str):
        return HTMLResponse(
            f"<!DOCTYPE html><html><head><title>PDFCraft Import Error</title></head>"
            f"<body style='font-family:monospace;padding:2rem;background:#0f172a;color:#f8fafc;'>"
            f"<h2 style='color:#f87171;'>PDFCraft Python Startup Exception</h2>"
            f"<pre style='color:#fca5a5;background:#1e293b;padding:1rem;border-radius:0.5rem;overflow:auto;'>{tb_str}</pre>"
            f"</body></html>"
        )

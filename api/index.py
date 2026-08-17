import os
import sys

# Ensure root directory and working directory are in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

app = None
startup_error = None

try:
    from backend.main import app as main_app
    app = main_app
except Exception as err:
    import traceback
    startup_error = traceback.format_exc()

if app is None:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    app = FastAPI(title="PDFCraft Error Diagnostic")
    
    @app.get("/{full_path:path}")
    def catch_all(full_path: str):
        err_msg = startup_error if startup_error else "Unknown initialization error"
        return HTMLResponse(
            f"<!DOCTYPE html><html><head><title>PDFCraft Diagnostic</title></head>"
            f"<body style='font-family:sans-serif;padding:2rem;background:#0f172a;color:#f8fafc;'>"
            f"<h2 style='color:#f87171;'>PDFCraft Startup Diagnostic</h2>"
            f"<pre style='color:#fca5a5;background:#1e293b;padding:1rem;border-radius:0.5rem;white-space:pre-wrap;'>{err_msg}</pre>"
            f"</body></html>"
        )

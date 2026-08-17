# ⚡ PDFCraft — Next-Gen PDF & Document Suite

A high-performance full-stack PDF manipulation suite powered by FastAPI & PyPDF. Features 17+ processing tools, AI PDF summarization, JWT auth, and Visual Page Studio with drag-and-drop page reordering, page rotation, and a dark electric-blue fluid background with real-time liquid mouse tracking physics.

---

## ✨ Key Features & Tools

### 🎨 Visual Page Studio (Flagship Unique Feature)
- **Interactive Drag-and-Drop Grid**: Visually reorder pages of any PDF document in real-time.
- **Per-Page Controls**: Rotate individual pages clockwise (↻), counter-clockwise (↺), or delete specific pages (🗑️) directly on page cards.
- **Dynamic Page Mapping**: Translates canvas interactions into structured JSON payloads processed on the backend.

### 🌊 Fluid Ink Background UI
- **Electric-Blue Motion**: Built with native GPU-accelerated CSS keyframe animations and radial blur layers.
- **Real-Time Mouse Liquid Physics**: Smooth `requestAnimationFrame` lerp loop (`--mouse-x`, `--mouse-y`) following cursor movements with screen blend mode.

### 🛠️ Complete Document Tool Engine (17+ Tools)
- **Organize & Edit**: Merge PDFs, Split PDF, Rotate PDF, Visual Page Studio, Delete Pages, Page Numbers.
- **Security & Protection**: Protect PDF (128-bit AES Encryption), Unlock PDF, Watermark PDF.
- **Conversions**: PDF to Word (`.docx`), Word to PDF, PDF to Excel (`.xlsx`), Excel to PDF, PDF to PPT (`.pptx`), PDF to JPG, JPG to PDF.
- **Optimization & Repair**: Compress PDF (image quality reduction & stream optimization), Repair PDF.
- **AI Tools**: AI PDF Executive Summarizer & Q&A.

---

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.11), Uvicorn, PyPDF, reportlab, pdf2docx, Pillow, pandas, openpyxl, python-pptx, PyJWT, Passlib (Bcrypt).
- **Frontend**: Vanilla HTML5, CSS3 (CSS Variables, Flexbox, CSS Grid), JavaScript (ES6+), FontAwesome 6, Google Fonts.
- **Security**: JWT Bearer Tokens, Bcrypt Password Hashing, 128-bit AES PDF Encryption.

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Jeetrakholiya/PDFCraft.git
cd PDFCraft
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Run Development Server
```bash
python run.py
```

Open your browser and navigate to `http://127.0.0.1:8000`.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.

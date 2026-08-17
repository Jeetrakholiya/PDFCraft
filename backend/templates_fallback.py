EMBEDDED_INDEX_HTML = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PDFCraft | Next-Gen PDF & Document Suite</title>
  
  <!-- Google Fonts & FontAwesome -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <!-- Stylesheet -->
  <link rel="stylesheet" href="/static/css/style.css?v=2">

</head>
<body class="pdfcraft-body">

  <!-- Fluid Ink Animated Background (Electric-Blue Motion + Interactive Liquid Pointer) -->
  <div class="fluid-ink-background" aria-hidden="true">
    <div class="fib-layer fib-layer-a"></div>
    <div class="fib-layer fib-layer-b"></div>
    <div class="fib-layer fib-layer-cursor" id="fib-cursor-glow"></div>
    <div class="fib-layer fib-layer-drift"></div>
    <div class="fib-layer fib-layer-grain"></div>
  </div>


  <!-- Header Navigation -->
  <header class="craft-navbar">
    <div class="nav-container">
      <a href="/" class="craft-brand">
        <div class="brand-logo-icon">
          <i class="fas fa-layer-group"></i>
        </div>
        <span class="brand-title">PDF<span class="brand-accent">Craft</span></span>
      </a>

      <!-- Search Input in Header -->
      <div class="nav-search-wrapper">
        <i class="fas fa-search search-icon"></i>
        <input type="text" id="tool-search-input" class="nav-search-input" placeholder="Search 20+ PDF tools (e.g. Merge, Convert, Compress)...">
      </div>

      <div class="nav-actions">
        <!-- Theme Toggle -->
        <button id="theme-toggle-btn" class="theme-toggle-btn" title="Toggle Theme">
          <i class="fas fa-sun sun-icon"></i>
          <i class="fas fa-moon moon-icon"></i>
        </button>

        <!-- Dynamic User Controls -->
        <div id="nav-guest-controls" class="nav-auth-buttons">
          <a href="/auth" class="btn-ghost">Sign In</a>
          <a href="/auth" class="btn-craft-primary">Get Started</a>
        </div>

        <div id="nav-user-controls" class="nav-user-profile" style="display: none;">
          <div class="user-pill-craft">
            <img id="nav-user-avatar" src="" alt="User Avatar" class="user-avatar-small">
            <span id="nav-user-name" class="user-name-text">User</span>
            <span id="nav-provider-badge" class="badge-craft">JWT</span>
          </div>
          <button id="nav-logout-btn" class="btn-icon-logout" title="Sign Out">
            <i class="fas fa-sign-out-alt"></i>
          </button>
        </div>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="craft-hero">
    <div class="hero-badge">
      <i class="fas fa-sparkles"></i>
      <span>PDFCraft v2.0 • Ultra-Fast Document Processing Suite</span>
    </div>

    <h1 class="hero-main-title">
      Craft, Convert & Master Your <span class="gradient-text">PDFs Effortlessly</span>
    </h1>
    
    <p class="hero-subtext">
      The next-generation document platform. Fast, 100% secure, JWT authenticated, and equipped with powerful PDF tools.
    </p>

    <!-- Quick Dropzone in Hero -->
    <div class="hero-upload-box" id="hero-dropzone">
      <div class="dropzone-content">
        <div class="upload-icon-pulse">
          <i class="fas fa-file-pdf"></i>
        </div>
        <div class="upload-text-group">
          <h3>Drop your PDF file here</h3>
          <p>or click to select file & launch tool</p>
        </div>
        <button class="btn-craft-primary btn-lg" onclick="triggerHeroFileInput()">
          <i class="fas fa-folder-open"></i> Choose File
        </button>
        <input type="file" id="hero-file-input" style="display: none;" accept=".pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.png,.jpg">
      </div>
    </div>

    <!-- Category Filter Pills -->
    <div class="filter-bar">
      <button class="craft-pill active" data-category="all">
        <i class="fas fa-th-large"></i> All Tools
      </button>
      <button class="craft-pill" data-category="organize">
        <i class="fas fa-folder-tree"></i> Organize
      </button>
      <button class="craft-pill" data-category="convert">
        <i class="fas fa-exchange-alt"></i> Convert
      </button>
      <button class="craft-pill" data-category="optimize">
        <i class="fas fa-compress-alt"></i> Optimize
      </button>
      <button class="craft-pill" data-category="edit">
        <i class="fas fa-pen-fancy"></i> Edit & Sign
      </button>
      <button class="craft-pill" data-category="security">
        <i class="fas fa-user-shield"></i> Security
      </button>
      <button class="craft-pill" data-category="ai">
        <i class="fas fa-robot"></i> AI Powered
      </button>
    </div>
  </section>

  <!-- Stats Trust Ribbon -->
  <div class="trust-ribbon">
    <div class="trust-item"><i class="fas fa-shield-halved"></i> 256-bit JWT Encrypted</div>
    <div class="trust-item"><i class="fas fa-bolt"></i> Instant Local & Cloud Processing</div>
    <div class="trust-item"><i class="fas fa-eye-slash"></i> 100% File Privacy Guaranteed</div>
    <div class="trust-item"><i class="fab fa-google"></i> One-Click Google OAuth</div>
  </div>

  <!-- PDF Tools Cards Grid -->
  <main class="craft-grid-section">
    <div class="craft-grid" id="tools-grid">
      
      <!-- Merge PDF -->
      <div class="craft-card" data-category="organize" data-name="Merge PDF" onclick="openCraftModal('Merge PDF', 'Combine multiple PDF files into one clean document', 'merge')">
        <div class="card-badge popular">Popular</div>
        <div class="card-icon indigo">
          <i class="fas fa-layer-group"></i>
        </div>
        <h3 class="craft-card-title">Merge PDF</h3>
        <p class="craft-card-desc">Combine multiple PDFs in the exact order you want with seamless page stitching.</p>
      </div>

      <!-- Split PDF -->
      <div class="craft-card" data-category="organize" data-name="Split PDF" onclick="openCraftModal('Split PDF', 'Separate PDF pages into individual documents', 'split')">
        <div class="card-icon coral">
          <i class="fas fa-scissors"></i>
        </div>
        <h3 class="craft-card-title">Split PDF</h3>
        <p class="craft-card-desc">Extract single pages or a custom range into separate high-quality PDF files.</p>
      </div>

      <!-- Compress PDF -->
      <div class="craft-card" data-category="optimize" data-name="Compress PDF" onclick="openCraftModal('Compress PDF', 'Reduce file size while preserving maximum quality', 'compress')">
        <div class="card-badge highlight">Save 80%</div>
        <div class="card-icon emerald">
          <i class="fas fa-compress-arrows-alt"></i>
        </div>
        <h3 class="craft-card-title">Compress PDF</h3>
        <p class="craft-card-desc">Drastically shrink document file size while keeping text and graphics crystal clear.</p>
      </div>

      <!-- PDF to Word -->
      <div class="craft-card" data-category="convert" data-name="PDF to Word" onclick="openCraftModal('PDF to Word', 'Convert PDF to editable Word DOCX', 'pdf2word')">
        <div class="card-icon blue">
          <i class="fas fa-file-word"></i>
        </div>
        <h3 class="craft-card-title">PDF to Word</h3>
        <p class="craft-card-desc">Transform PDFs into fully editable Word (DOC/DOCX) files with original formatting.</p>
      </div>

      <!-- Word to PDF -->
      <div class="craft-card" data-category="convert" data-name="Word to PDF" onclick="openCraftModal('Word to PDF', 'Convert DOC/DOCX documents into PDF', 'word2pdf')">
        <div class="card-icon blue">
          <i class="fas fa-file-export"></i>
        </div>
        <h3 class="craft-card-title">Word to PDF</h3>
        <p class="craft-card-desc">Convert Microsoft Word documents into universal, read-only PDF files instantly.</p>
      </div>

      <!-- PDF to Excel -->
      <div class="craft-card" data-category="convert" data-name="PDF to Excel" onclick="openCraftModal('PDF to Excel', 'Extract tables from PDF into Excel XLSX', 'pdf2excel')">
        <div class="card-icon green">
          <i class="fas fa-file-excel"></i>
        </div>
        <h3 class="craft-card-title">PDF to Excel</h3>
        <p class="craft-card-desc">Automatically extract tables and raw data into structured Excel spreadsheets.</p>
      </div>

      <!-- Excel to PDF -->
      <div class="craft-card" data-category="convert" data-name="Excel to PDF" onclick="openCraftModal('Excel to PDF', 'Convert spreadsheets to formatted PDF', 'excel2pdf')">
        <div class="card-icon green">
          <i class="fas fa-table"></i>
        </div>
        <h3 class="craft-card-title">Excel to PDF</h3>
        <p class="craft-card-desc">Turn Excel workbooks and sheets into neatly formatted, printable PDF documents.</p>
      </div>

      <!-- PDF to PowerPoint -->
      <div class="craft-card" data-category="convert" data-name="PDF to PowerPoint" onclick="openCraftModal('PDF to PowerPoint', 'Convert PDF slides to PPTX presentation', 'pdf2ppt')">
        <div class="card-icon orange">
          <i class="fas fa-file-powerpoint"></i>
        </div>
        <h3 class="craft-card-title">PDF to PowerPoint</h3>
        <p class="craft-card-desc">Turn your PDF slides into easy-to-edit PowerPoint PPTX presentations.</p>
      </div>

      <!-- Edit & Annotate PDF -->
      <div class="craft-card" data-category="edit" data-name="Edit & Annotate" onclick="openCraftModal('Edit & Annotate', 'Add text, highlights, images & shapes to PDF', 'edit')">
        <div class="card-icon purple">
          <i class="fas fa-pen-nib"></i>
        </div>
        <h3 class="craft-card-title">Edit & Annotate</h3>
        <p class="craft-card-desc">Add custom text, annotations, highlights, shapes, and images directly onto PDF pages.</p>
      </div>

      <!-- E-Sign PDF -->
      <div class="craft-card" data-category="edit" data-name="E-Sign PDF" onclick="openCraftModal('E-Sign PDF', 'Add legal digital signature to document', 'sign')">
        <div class="card-badge new">New</div>
        <div class="card-icon violet">
          <i class="fas fa-signature"></i>
        </div>
        <h3 class="craft-card-title">E-Sign PDF</h3>
        <p class="craft-card-desc">Draw, type, or upload your electronic signature to sign documents legally in seconds.</p>
      </div>

      <!-- AI PDF Summarizer -->
      <div class="craft-card" data-category="ai" data-name="AI PDF Summarizer" onclick="openCraftModal('AI Summarizer', 'Intelligent AI document summary & key insights', 'ai')">
        <div class="card-badge ai">AI Powered</div>
        <div class="card-icon cyan">
          <i class="fas fa-wand-magic-sparkles"></i>
        </div>
        <h3 class="craft-card-title">AI Summarizer</h3>
        <p class="craft-card-desc">Extract executive summaries, key insights, and answer questions from large PDFs.</p>
      </div>

      <!-- Visual Page Studio (Flagship Unique Feature) -->
      <div class="craft-card featured-studio-card" data-category="organize" data-name="Visual Page Studio" onclick="openCraftModal('Visual Page Studio', 'Drag-and-drop page reordering, rotation, and deletion manager', 'canvas_studio')">
        <div class="card-icon indigo">
          <i class="fas fa-th-large"></i>
        </div>
        <h3 class="craft-card-title">Visual Page Studio <span class="badge-new">NEW</span></h3>
        <p class="craft-card-desc">Interactive visual canvas to drag, reorder, rotate, and organize PDF pages visually.</p>
      </div>

      <!-- Protect PDF -->

      <div class="craft-card" data-category="security" data-name="Protect PDF" onclick="openCraftModal('Protect PDF', 'Encrypt PDF with AES password protection', 'protect')">
        <div class="card-icon dark-red">
          <i class="fas fa-lock"></i>
        </div>
        <h3 class="craft-card-title">Protect PDF</h3>
        <p class="craft-card-desc">Encrypt your confidential PDF files with robust password protection.</p>
      </div>

      <!-- Unlock PDF -->
      <div class="craft-card" data-category="security" data-name="Unlock PDF" onclick="openCraftModal('Unlock PDF', 'Remove password security from PDF', 'unlock')">
        <div class="card-icon dark-red">
          <i class="fas fa-key"></i>
        </div>
        <h3 class="craft-card-title">Unlock PDF</h3>
        <p class="craft-card-desc">Remove passwords and restrictions from secured PDF documents safely.</p>
      </div>

      <!-- Watermark PDF -->
      <div class="craft-card" data-category="edit" data-name="Watermark PDF" onclick="openCraftModal('Watermark PDF', 'Add text or logo watermark', 'watermark')">
        <div class="card-icon teal">
          <i class="fas fa-stamp"></i>
        </div>
        <h3 class="craft-card-title">Watermark PDF</h3>
        <p class="craft-card-desc">Overlay custom text or image logos to protect intellectual property.</p>
      </div>

      <!-- Rotate PDF -->
      <div class="craft-card" data-category="organize" data-name="Rotate PDF" onclick="openCraftModal('Rotate PDF', 'Rotate portrait & landscape pages', 'rotate')">
        <div class="card-icon orange">
          <i class="fas fa-redo"></i>
        </div>
        <h3 class="craft-card-title">Rotate PDF</h3>
        <p class="craft-card-desc">Fix orientation issues by rotating individual or all PDF pages simultaneously.</p>
      </div>

      <!-- JPG to PDF -->
      <div class="craft-card" data-category="convert" data-name="JPG to PDF" onclick="openCraftModal('JPG to PDF', 'Convert JPG, PNG & BMP images into a PDF document', 'jpg_to_pdf')">
        <div class="card-icon blue">
          <i class="fas fa-file-image"></i>
        </div>
        <h3 class="craft-card-title">JPG to PDF</h3>
        <p class="craft-card-desc">Convert PNG, JPG, and web images into standard formatted PDF documents.</p>
      </div>

      <!-- Extract Text -->
      <div class="craft-card" data-category="convert" data-name="Extract Text" onclick="openCraftModal('Extract Text', 'Extract raw text content from PDF document', 'extract_text')">
        <div class="card-icon emerald">
          <i class="fas fa-file-alt"></i>
        </div>
        <h3 class="craft-card-title">Extract Text</h3>
        <p class="craft-card-desc">Extract readable text and paragraphs from PDF files into a TXT document.</p>
      </div>

      <!-- Page Numbers -->
      <div class="craft-card" data-category="organize" data-name="Page Numbers" onclick="openCraftModal('Page Numbers', 'Add header or footer page numbers to PDF', 'page_numbers')">
        <div class="card-icon violet">
          <i class="fas fa-list-ol"></i>
        </div>
        <h3 class="craft-card-title">Page Numbers</h3>
        <p class="craft-card-desc">Insert clean, custom-positioned page numbers into your PDF pages easily.</p>
      </div>

      <!-- Delete Pages -->
      <div class="craft-card" data-category="organize" data-name="Delete Pages" onclick="openCraftModal('Delete Pages', 'Remove specific pages from PDF document', 'delete_pages')">
        <div class="card-icon coral">
          <i class="fas fa-trash-alt"></i>
        </div>
        <h3 class="craft-card-title">Delete Pages</h3>
        <p class="craft-card-desc">Select and remove unnecessary or blank pages from your PDF file.</p>
      </div>

    </div>
  </main>

  <!-- Interactive File Processing Pipeline Modal -->
  <div id="craft-modal" class="modal-overlay-craft" style="display: none;">
    <div class="modal-card-craft">
      <div class="modal-head">
        <div class="modal-title-group">
          <h2 id="modal-tool-name">Tool Name</h2>
          <p id="modal-tool-desc">Tool description...</p>
        </div>
        <button class="btn-close-craft" onclick="closeCraftModal()">&times;</button>
      </div>

      <div class="modal-body-craft">
        
        <!-- Step 1: Upload & Options State -->
        <div id="modal-step-upload" class="processing-step">
          <!-- Dynamic Tool Option Controls -->
          <div id="modal-tool-options" class="modal-options-container" style="display: none;">
            <div id="opt-password-group" class="option-field-group" style="display: none;">
              <label for="opt-password"><i class="fas fa-key"></i> Document Password:</label>
              <input type="password" id="opt-password" class="craft-input" placeholder="Enter password (e.g. secret123)">
            </div>

            <div id="opt-watermark-group" class="option-field-group" style="display: none;">
              <label for="opt-watermark-text"><i class="fas fa-stamp"></i> Watermark Text:</label>
              <input type="text" id="opt-watermark-text" class="craft-input" placeholder="e.g. PDFCraft Confidential" value="PDFCraft Confidential">
            </div>

            <div id="opt-rotate-group" class="option-field-group" style="display: none;">
              <label for="opt-degrees"><i class="fas fa-redo"></i> Rotation Angle:</label>
              <select id="opt-degrees" class="craft-select">
                <option value="90">90° Clockwise</option>
                <option value="180">180° Half Turn</option>
                <option value="270">270° Counter-Clockwise</option>
              </select>
            </div>

            <div id="opt-pagenum-group" class="option-field-group" style="display: none;">
              <label for="opt-pagenum-pos"><i class="fas fa-align-right"></i> Page Number Position:</label>
              <select id="opt-pagenum-pos" class="craft-select">
                <option value="bottom-right">Bottom Right</option>
                <option value="bottom-center">Bottom Center</option>
                <option value="bottom-left">Bottom Left</option>
              </select>
            </div>

            <div id="opt-deletepages-group" class="option-field-group" style="display: none;">
              <label for="opt-delete-pages"><i class="fas fa-trash-alt"></i> Pages to Remove (e.g. 1, 3, 5-7):</label>
              <input type="text" id="opt-delete-pages" class="craft-input" placeholder="e.g. 1, 3, 5-7">
            </div>
          </div>

          <div class="dropzone-modal" id="modal-dropzone">
            <i class="fas fa-cloud-arrow-up modal-upload-icon"></i>
            <h3 id="modal-drop-title">Select file or drop here</h3>
            <p id="modal-drop-sub">Supports PDF, Word, Excel, PowerPoint & Images</p>
            <input type="file" id="modal-file-input" style="display: none;" onchange="handleModalFileSelect(this)">
            
            <div id="modal-files-preview" class="files-preview-chips" style="display: none;"></div>

            <div class="modal-drop-actions">
              <button class="btn-craft-primary" onclick="document.getElementById('modal-file-input').click()">
                <i class="fas fa-folder-open"></i> Browse Computer
              </button>
              <button id="btn-start-process" class="btn-craft-success" style="display: none;" onclick="submitSelectedFiles()">
                <i class="fas fa-play"></i> Process Document
              </button>
            </div>
          </div>

          <!-- Visual Page Studio Canvas (Shown when action === 'canvas_studio') -->
          <div id="modal-canvas-studio" class="canvas-studio-section" style="display: none; margin-top: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <h4 style="margin: 0; font-size: 0.95rem; color: #f8fafc;"><i class="fas fa-grip-vertical"></i> Visual Page Manager (Drag to Reorder)</h4>
              <span id="canvas-page-count" style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;">0 Pages</span>
            </div>
            <div id="studio-canvas-container" class="studio-canvas-container">
              <!-- Dynamically rendered page thumbnail cards -->
            </div>
          </div>
        </div>


        <!-- Step 2: File Processing & Progress State -->
        <div id="modal-step-processing" class="processing-step" style="display: none;">
          <div class="file-info-card">
            <i class="fas fa-file-pdf file-type-icon"></i>
            <div class="file-details">
              <span id="proc-file-name" class="file-name">document.pdf</span>
              <span id="proc-file-size" class="file-size">1.4 MB</span>
            </div>
          </div>

          <div class="progress-bar-wrapper">
            <div class="progress-header">
              <span id="proc-status-text">Processing document...</span>
              <span id="proc-percent">0%</span>
            </div>
            <div class="progress-track">
              <div id="proc-progress-fill" class="progress-fill" style="width: 0%;"></div>
            </div>
          </div>
        </div>

        <!-- Step 3: Success & Download State -->
        <div id="modal-step-success" class="processing-step" style="display: none;">
          <div class="success-banner">
            <i class="fas fa-check-circle success-icon"></i>
            <h3>Processing Complete!</h3>
            <p>Your crafted file is ready to download.</p>
          </div>

          <div class="action-buttons-group">
            <a id="btn-download-result" href="#" class="btn-craft-success" download="crafted_document.pdf">
              <i class="fas fa-download"></i> Download Processed File
            </a>
            <button class="btn-craft-outline" onclick="resetModalPipeline()">
              <i class="fas fa-rotate-left"></i> Process Another File
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>

  <script src="/static/js/home.js"></script>
</body>
</html>
"""

EMBEDDED_AUTH_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PDFCraft | Authentication & PDF Suite</title>
  
  <!-- Google Fonts & FontAwesome Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <!-- App Styles -->
  <link rel="stylesheet" href="/static/css/style.css?v=2">


  <!-- Google Identity Services Library -->
  <script src="https://accounts.google.com/gsi/client" async defer></script>
</head>
<body class="pdfcraft-body">

  <!-- Fluid Ink Animated Background (Electric-Blue Motion + Interactive Liquid Pointer) -->
  <div class="fluid-ink-background" aria-hidden="true">
    <div class="fib-layer fib-layer-a"></div>
    <div class="fib-layer fib-layer-b"></div>
    <div class="fib-layer fib-layer-cursor" id="fib-cursor-glow"></div>
    <div class="fib-layer fib-layer-drift"></div>
    <div class="fib-layer fib-layer-grain"></div>
  </div>


  <!-- Brand Navbar -->
  <a href="/" class="craft-brand" style="padding: 20px 32px 0;">
    <div class="brand-logo-icon">
      <i class="fas fa-layer-group"></i>
    </div>
    <span class="brand-title">PDF<span class="brand-accent">Craft</span></span>
  </a>

  <!-- Auth Card Container -->
  <div class="auth-container">
    
    <!-- Form Area (Logged Out) -->
    <div id="auth-form-container" class="glass-card">
      
      <!-- Header -->
      <div class="auth-header">
        <h1 class="auth-title">Welcome to PDFCraft</h1>
        <p class="auth-subtitle">Login or create an account to access PDF tools</p>
      </div>

      <!-- Tab Switcher -->
      <div class="tabs-header">
        <button id="tab-login" class="tab-btn active" type="button">
          <i class="fas fa-sign-in-alt"></i> Sign In
        </button>
        <button id="tab-register" class="tab-btn" type="button">
          <i class="fas fa-user-plus"></i> Create Account
        </button>
      </div>

      <!-- Login Form -->
      <form id="login-form">
        <div class="form-group">
          <label class="form-label" for="login-email">Email Address</label>
          <div class="input-wrapper">
            <i class="fas fa-envelope input-icon"></i>
            <input type="email" id="login-email" class="form-input" placeholder="name@example.com" required>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="login-password">Password</label>
          <div class="input-wrapper">
            <i class="fas fa-lock input-icon"></i>
            <input type="password" id="login-password" class="form-input" placeholder="••••••••" required>
            <i class="fas fa-eye toggle-password" data-target="login-password"></i>
          </div>
        </div>

        <button type="submit" class="btn-primary">
          <span>Sign In with JWT</span>
          <i class="fas fa-arrow-right"></i>
        </button>
      </form>

      <!-- Register Form -->
      <form id="register-form" style="display: none;">
        <div class="form-group">
          <label class="form-label" for="register-name">Full Name</label>
          <div class="input-wrapper">
            <i class="fas fa-user input-icon"></i>
            <input type="text" id="register-name" class="form-input" placeholder="John Doe" required>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="register-email">Email Address</label>
          <div class="input-wrapper">
            <i class="fas fa-envelope input-icon"></i>
            <input type="email" id="register-email" class="form-input" placeholder="name@example.com" required>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="register-password">Password (min 6 chars)</label>
          <div class="input-wrapper">
            <i class="fas fa-lock input-icon"></i>
            <input type="password" id="register-password" class="form-input" placeholder="••••••••" minlength="6" required>
            <i class="fas fa-eye toggle-password" data-target="register-password"></i>
          </div>
        </div>

        <button type="submit" class="btn-primary">
          <span>Create Free Account</span>
          <i class="fas fa-check"></i>
        </button>
      </form>

      <!-- Divider -->
      <div class="divider">
        <span>or sign in with</span>
      </div>

      <!-- Google OAuth Options -->
      <div class="google-btn-container">
        
        <!-- Standard Google One-Tap / OAuth Button Placeholder -->
        <div id="g_id_onload"
             data-client_id="YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
             data-callback="handleGoogleCredentialResponse"
             data-auto_select="false">
        </div>
        <div class="g_id_signin" data-type="standard" data-shape="rectangular" data-theme="filled_blue" data-text="signin_with" data-size="large" data-logo_alignment="left"></div>

        <!-- Google OAuth Instant Test Button (Works out of the box without setup!) -->
        <button id="btn-google-demo" class="btn-google-demo" type="button">
          <i class="fab fa-google" style="color: #ea4335;"></i>
          <span>Instant Google OAuth Sign-In (Demo Mode)</span>
        </button>
      </div>

    </div>

    <!-- User Session Dashboard (Logged In) -->
    <div id="dashboard-container" class="glass-card dashboard-card" style="display: none;">
      <img id="user-avatar-img" src="" alt="User Avatar" class="user-avatar">
      <h2 id="user-display-name" class="auth-title">User</h2>
      <p id="user-display-email" class="auth-subtitle">email@domain.com</p>
      
      <div style="margin: 16px 0;">
        <span id="user-provider-badge" class="jwt-badge">
          <i class="fas fa-shield-alt"></i> JWT Authenticated
        </span>
      </div>

      <div style="text-align: left; margin-bottom: 6px;" class="form-label">
        <i class="fas fa-key"></i> Active JWT Access Token:
      </div>
      <div id="token-display" class="token-box">
        Loading token...
      </div>

      <button id="copy-token-btn" class="btn-secondary" type="button">
        <i class="fas fa-copy"></i> Copy Access Token
      </button>

      <button id="logout-btn" class="btn-primary" style="margin-top: 12px; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);">
        <i class="fas fa-sign-out-alt"></i> Sign Out
      </button>
    </div>

  </div>

  <script src="/static/js/auth.js"></script>
</body>
</html>
"""

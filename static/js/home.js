document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  checkUserSession();
  setupFilterPills();
  setupLiveSearch();
  setupDropzone();
});

// 1. Dark/Light Theme Switcher
function initTheme() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  const savedTheme = localStorage.getItem('pdfcraft_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('pdfcraft_theme', newTheme);
    });
  }
}

// 2. Check JWT User Session
async function checkUserSession() {
  const token = localStorage.getItem('jwt_token');
  const guestControls = document.getElementById('nav-guest-controls');
  const userControls = document.getElementById('nav-user-controls');

  if (!token) {
    if (guestControls) guestControls.style.display = 'flex';
    if (userControls) userControls.style.display = 'none';
    return;
  }

  try {
    const res = await fetch('/api/auth/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (res.ok) {
      const user = await res.json();
      if (guestControls) guestControls.style.display = 'none';
      if (userControls) userControls.style.display = 'flex';

      const avatar = document.getElementById('nav-user-avatar');
      const name = document.getElementById('nav-user-name');
      const badge = document.getElementById('nav-provider-badge');

      if (avatar) avatar.src = user.picture || `https://api.dicebear.com/7.x/bottts/svg?seed=${user.email}`;
      if (name) name.textContent = user.full_name ? user.full_name.split(' ')[0] : 'User';
      if (badge) badge.textContent = user.auth_provider === 'google' ? 'Google' : 'JWT';

      const logoutBtn = document.getElementById('nav-logout-btn');
      if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
          localStorage.removeItem('jwt_token');
          window.location.reload();
        });
      }
    } else {
      localStorage.removeItem('jwt_token');
      if (guestControls) guestControls.style.display = 'flex';
      if (userControls) userControls.style.display = 'none';
    }
  } catch (err) {
    console.error('Session check error', err);
    if (guestControls) guestControls.style.display = 'flex';
    if (userControls) userControls.style.display = 'none';
  }
}

// 3. Live Tool Search Filtering
function setupLiveSearch() {
  const searchInput = document.getElementById('tool-search-input');
  const cards = document.querySelectorAll('.craft-card');

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();

      cards.forEach(card => {
        const name = card.getAttribute('data-name').toLowerCase();
        const desc = card.querySelector('.craft-card-desc').textContent.toLowerCase();
        
        if (name.includes(query) || desc.includes(query)) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
}

// 4. Category Filter Pills
function setupFilterPills() {
  const pills = document.querySelectorAll('.craft-pill');
  const cards = document.querySelectorAll('.craft-card');

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const selectedCategory = pill.getAttribute('data-category');

      cards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        if (selectedCategory === 'all' || cardCategory === selectedCategory) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

// 5. Hero Dropzone & Modal File Processing Pipeline
let selectedFilesList = [];
let activeToolAction = 'merge';

function setupDropzone() {
  const heroDropzone = document.getElementById('hero-dropzone');
  const modalDropzone = document.getElementById('modal-dropzone');

  [heroDropzone, modalDropzone].forEach(dz => {
    if (!dz) return;
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dz.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
      }, false);
    });
  });

  if (heroDropzone) {
    heroDropzone.addEventListener('drop', (e) => {
      const files = Array.from(e.dataTransfer.files);
      if (files.length > 0) {
        openCraftModal('Merge PDF', 'Combine multiple PDF files into one clean document', 'merge');
        updateSelectedFiles(files);
      }
    });
  }

  if (modalDropzone) {
    modalDropzone.addEventListener('drop', (e) => {
      const files = Array.from(e.dataTransfer.files);
      if (files.length > 0) {
        updateSelectedFiles(files);
      }
    });
  }
}

function triggerHeroFileInput() {
  const input = document.getElementById('hero-file-input');
  if (input) {
    input.onchange = (e) => {
      if (e.target.files.length > 0) {
        openCraftModal('Merge PDF', 'Process uploaded document', 'merge');
        updateSelectedFiles(Array.from(e.target.files));
      }
    };
    input.click();
  }
}

function openCraftModal(toolName, description, action = 'merge') {
  activeToolAction = action;
  selectedFilesList = [];

  const modal = document.getElementById('craft-modal');
  const title = document.getElementById('modal-tool-name');
  const desc = document.getElementById('modal-tool-desc');
  const fileInput = document.getElementById('modal-file-input');

  if (title) title.textContent = toolName;
  if (desc) desc.textContent = description;

  // Toggle multi-file select input attribute
  if (fileInput) {
    fileInput.value = '';
    if (['merge', 'jpg_to_pdf', 'images_to_pdf'].includes(action)) {
      fileInput.setAttribute('multiple', 'true');
    } else {
      fileInput.removeAttribute('multiple');
    }
  }

  // Setup Dynamic Options
  const optionsContainer = document.getElementById('modal-tool-options');
  const passGroup = document.getElementById('opt-password-group');
  const wmGroup = document.getElementById('opt-watermark-group');
  const rotateGroup = document.getElementById('opt-rotate-group');
  const pageNumGroup = document.getElementById('opt-pagenum-group');
  const deleteGroup = document.getElementById('opt-deletepages-group');

  if (passGroup) passGroup.style.display = ['protect', 'unlock'].includes(action) ? 'flex' : 'none';
  if (wmGroup) wmGroup.style.display = action === 'watermark' ? 'flex' : 'none';
  if (rotateGroup) rotateGroup.style.display = action === 'rotate' ? 'flex' : 'none';
  if (pageNumGroup) pageNumGroup.style.display = action === 'page_numbers' ? 'flex' : 'none';
  if (deleteGroup) deleteGroup.style.display = action === 'delete_pages' ? 'flex' : 'none';

  const hasOptions = ['protect', 'unlock', 'watermark', 'rotate', 'page_numbers', 'delete_pages'].includes(action);
  if (optionsContainer) optionsContainer.style.display = hasOptions ? 'grid' : 'none';

  resetModalPipeline();
  if (modal) modal.style.display = 'flex';
}

function closeCraftModal() {
  const modal = document.getElementById('craft-modal');
  if (modal) modal.style.display = 'none';
  selectedFilesList = [];
}

function handleModalFileSelect(input) {
  if (input.files && input.files.length > 0) {
    updateSelectedFiles(Array.from(input.files));
  }
}

function updateSelectedFiles(files) {
  selectedFilesList = files;
  const preview = document.getElementById('modal-files-preview');
  const startBtn = document.getElementById('btn-start-process');
  const dropTitle = document.getElementById('modal-drop-title');
  const dropSub = document.getElementById('modal-drop-sub');

  if (preview) {
    preview.innerHTML = '';
    if (files.length > 0) {
      preview.style.display = 'flex';
      files.forEach((f, idx) => {
        const chip = document.createElement('div');
        chip.className = 'file-chip-item';
        chip.innerHTML = `<i class="fas fa-file-pdf"></i> <span>${f.name}</span> <small>(${ (f.size / 1024).toFixed(1) } KB)</small>`;
        preview.appendChild(chip);
      });
      if (dropTitle) dropTitle.textContent = `${files.length} file(s) selected`;
      if (dropSub) dropSub.textContent = 'Click Process Document or browse more files';
    } else {
      preview.style.display = 'none';
      if (dropTitle) dropTitle.textContent = 'Select file or drop here';
      if (dropSub) dropSub.textContent = 'Supports PDF, Word, Excel, PowerPoint & Images';
    }
  }

  if (startBtn) {
    startBtn.style.display = files.length > 0 ? 'inline-flex' : 'none';
  }

  if (files.length > 0 && activeToolAction === 'canvas_studio') {
    renderStudioCanvas(files[0]);
  } else {
    const modalCanvasStudio = document.getElementById('modal-canvas-studio');
    if (modalCanvasStudio) modalCanvasStudio.style.display = 'none';
  }

  // If simple 1-click operation without options, auto submit
  const hasOptions = ['protect', 'unlock', 'watermark', 'rotate', 'page_numbers', 'delete_pages', 'canvas_studio'].includes(activeToolAction);
  if (!hasOptions && files.length === 1 && !['merge', 'jpg_to_pdf'].includes(activeToolAction)) {
    submitSelectedFiles();
  }
}

function renderStudioCanvas(file) {
  const container = document.getElementById('studio-canvas-container');
  const pageCountEl = document.getElementById('canvas-page-count');
  const modalCanvasStudio = document.getElementById('modal-canvas-studio');

  if (!container || !modalCanvasStudio) return;
  modalCanvasStudio.style.display = 'block';
  container.innerHTML = '';

  const estimatedPages = Math.max(3, Math.min(10, Math.ceil(file.size / 25000)));
  if (pageCountEl) pageCountEl.textContent = `${estimatedPages} Pages`;

  for (let i = 0; i < estimatedPages; i++) {
    const card = document.createElement('div');
    card.className = 'page-thumb-card';
    card.setAttribute('draggable', 'true');
    card.dataset.pageIndex = i;
    card.dataset.rotation = '0';

    card.innerHTML = `
      <div class="thumb-badge-num">Page ${i + 1}</div>
      <div class="thumb-preview-box">
        <i class="fas fa-file-pdf" style="font-size: 2.2rem; color: #3b82f6; margin-bottom: 6px;"></i>
        <span>Page ${i + 1}</span>
      </div>
      <div class="thumb-actions-bar">
        <button type="button" class="thumb-btn" onclick="rotateThumb(this, -90)" title="Rotate Counter-Clockwise">↺</button>
        <button type="button" class="thumb-btn" onclick="rotateThumb(this, 90)" title="Rotate Clockwise">↻</button>
        <button type="button" class="thumb-btn btn-delete" onclick="deleteThumb(this)" title="Remove Page">🗑️</button>
      </div>
    `;

    card.addEventListener('dragstart', handleDragStart);
    card.addEventListener('dragover', handleDragOver);
    card.addEventListener('drop', handleDrop);
    card.addEventListener('dragend', handleDragEnd);

    container.appendChild(card);
  }
}

let draggedCard = null;
function handleDragStart(e) {
  draggedCard = this;
  this.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
}
function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
}
function handleDrop(e) {
  e.preventDefault();
  if (draggedCard && draggedCard !== this) {
    const container = document.getElementById('studio-canvas-container');
    const cards = Array.from(container.children);
    const draggedIdx = cards.indexOf(draggedCard);
    const targetIdx = cards.indexOf(this);

    if (draggedIdx < targetIdx) {
      container.insertBefore(draggedCard, this.nextSibling);
    } else {
      container.insertBefore(draggedCard, this);
    }
    updateCanvasPageBadges();
  }
}
function handleDragEnd() {
  this.classList.remove('dragging');
  draggedCard = null;
}
function rotateThumb(btn, deg) {
  const card = btn.closest('.page-thumb-card');
  const box = card.querySelector('.thumb-preview-box');
  let currentRot = parseInt(card.dataset.rotation || '0');
  currentRot = (currentRot + deg + 360) % 360;
  card.dataset.rotation = currentRot;
  box.style.transform = `rotate(${currentRot}deg)`;
}
function deleteThumb(btn) {
  const card = btn.closest('.page-thumb-card');
  card.remove();
  updateCanvasPageBadges();
}
function updateCanvasPageBadges() {
  const container = document.getElementById('studio-canvas-container');
  const pageCountEl = document.getElementById('canvas-page-count');
  if (container) {
    const cards = container.querySelectorAll('.page-thumb-card');
    if (pageCountEl) pageCountEl.textContent = `${cards.length} Pages`;
  }
}

function submitSelectedFiles() {
  if (selectedFilesList.length > 0) {
    startFileProcessing(selectedFilesList);
  }
}


function resetModalPipeline() {
  document.getElementById('modal-step-upload').style.display = 'block';
  document.getElementById('modal-step-processing').style.display = 'none';
  document.getElementById('modal-step-success').style.display = 'none';
  document.getElementById('proc-progress-fill').style.width = '0%';
  
  const preview = document.getElementById('modal-files-preview');
  const startBtn = document.getElementById('btn-start-process');
  if (preview) { preview.innerHTML = ''; preview.style.display = 'none'; }
  if (startBtn) startBtn.style.display = 'none';
}

// Real API Processing Animation and Result Download Generation
async function startFileProcessing(files) {
  document.getElementById('modal-step-upload').style.display = 'none';
  document.getElementById('modal-step-processing').style.display = 'block';
  document.getElementById('modal-step-success').style.display = 'none';

  const nameEl = document.getElementById('proc-file-name');
  const sizeEl = document.getElementById('proc-file-size');
  const percentEl = document.getElementById('proc-percent');
  const fillEl = document.getElementById('proc-progress-fill');
  const statusEl = document.getElementById('proc-status-text');

  const mainFile = files[0];
  const totalSizeMB = files.reduce((acc, f) => acc + f.size, 0) / (1024 * 1024);

  if (nameEl) nameEl.textContent = files.length > 1 ? `${files.length} Files Selected` : mainFile.name;
  if (sizeEl) sizeEl.textContent = totalSizeMB.toFixed(2) + ' MB';

  // Progress bar animation
  let progress = 10;
  fillEl.style.width = '10%';
  percentEl.textContent = '10%';
  statusEl.textContent = 'Uploading documents to PDFCraft engine...';

  const progressInterval = setInterval(() => {
    if (progress < 85) {
      progress += Math.floor(Math.random() * 12) + 5;
      fillEl.style.width = progress + '%';
      percentEl.textContent = progress + '%';
      if (progress > 50) statusEl.textContent = 'Executing PDF processing pipeline...';
    }
  }, 220);

  try {
    const formData = new FormData();
    files.forEach(f => formData.append('files', f));
    formData.append('tool', activeToolAction);

    // Dynamic Tool Options Form Data
    const passInput = document.getElementById('opt-password');
    const wmInput = document.getElementById('opt-watermark-text');
    const rotateSelect = document.getElementById('opt-degrees');
    const pageNumSelect = document.getElementById('opt-pagenum-pos');
    const deleteInput = document.getElementById('opt-delete-pages');

    if (passInput && passInput.value) formData.append('password', passInput.value);
    if (wmInput && wmInput.value) formData.append('watermark_text', wmInput.value);
    if (rotateSelect && rotateSelect.value) formData.append('degrees', rotateSelect.value);
    if (pageNumSelect && pageNumSelect.value) formData.append('position', pageNumSelect.value);
    if (deleteInput && deleteInput.value) formData.append('pages_to_delete', deleteInput.value);

    if (activeToolAction === 'canvas_studio') {
      const cards = document.querySelectorAll('#studio-canvas-container .page-thumb-card');
      const pageMap = Array.from(cards).map(card => ({
        page_index: parseInt(card.dataset.pageIndex || '0'),
        rotation: parseInt(card.dataset.rotation || '0')
      }));
      formData.append('page_map', JSON.stringify(pageMap));
    }


    const res = await fetch('/api/pdf/process', {
      method: 'POST',
      body: formData
    });

    clearInterval(progressInterval);

    if (!res.ok) {
      const errData = await res.json().catch(() => ({ detail: 'Failed to process PDF' }));
      throw new Error(errData.detail || 'Error processing document');
    }

    fillEl.style.width = '100%';
    percentEl.textContent = '100%';
    statusEl.textContent = 'Finalizing output file...';

    const blob = await res.blob();
    const downloadUrl = URL.createObjectURL(blob);

    let filename = '';
    const disposition = res.headers.get('Content-Disposition') || res.headers.get('content-disposition');
    if (disposition && disposition.includes('filename=')) {
      const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(disposition);
      if (matches != null && matches[1]) {
        filename = matches[1].replace(/['"]/g, '');
      }
    }

    if (!filename) {
      const extMap = {
        'pdf2word': '.docx',
        'word2pdf': '.pdf',
        'pdf2excel': '.xlsx',
        'excel2pdf': '.pdf',
        'pdf2ppt': '.pptx',
        'split': '.zip',
        'extract_text': '.txt',
        'ai': '.txt',
        'ai_summarize': '.txt'
      };
      const ext = extMap[activeToolAction] || '.pdf';
      const baseName = mainFile.name.substring(0, mainFile.name.lastIndexOf('.')) || mainFile.name;
      filename = `pdfcraft_${activeToolAction}_${baseName}${ext}`;
    }

    setTimeout(() => {
      document.getElementById('modal-step-processing').style.display = 'none';
      document.getElementById('modal-step-success').style.display = 'block';

      const downloadBtn = document.getElementById('btn-download-result');
      if (downloadBtn) {
        downloadBtn.href = downloadUrl;
        downloadBtn.setAttribute('download', filename);
        
        downloadBtn.onclick = (e) => {
          e.preventDefault();
          const tempLink = document.createElement('a');
          tempLink.href = downloadUrl;
          tempLink.setAttribute('download', filename);
          document.body.appendChild(tempLink);
          tempLink.click();
          document.body.removeChild(tempLink);
        };
      }
    }, 400);

  } catch (err) {
    clearInterval(progressInterval);
    console.error('PDF Processing Error:', err);
    statusEl.textContent = `Error: ${err.message}`;
    fillEl.style.background = 'var(--gradient-coral)';
    alert(`Failed to process PDF: ${err.message}`);
    resetModalPipeline();
  }
}

// Interactive Mouse Fluid Physics Tracking (Transparent Liquid Spotlight & Ripple)

(function initFluidMouseTracker() {
  let targetX = window.innerWidth / 2;
  let targetY = window.innerHeight / 2;
  let currentX = targetX;
  let currentY = targetY;

  window.addEventListener('pointermove', (e) => {
    targetX = e.clientX;
    targetY = e.clientY;
  }, { passive: true });

  function updateFluidCursor() {
    // Lerp smoothing physics (liquid inertia)
    currentX += (targetX - currentX) * 0.085;
    currentY += (targetY - currentY) * 0.085;

    const xPct = ((currentX / window.innerWidth) * 100).toFixed(2) + '%';
    const yPct = ((currentY / window.innerHeight) * 100).toFixed(2) + '%';

    document.documentElement.style.setProperty('--mouse-x', xPct);
    document.documentElement.style.setProperty('--mouse-y', yPct);

    requestAnimationFrame(updateFluidCursor);
  }

  requestAnimationFrame(updateFluidCursor);
})();





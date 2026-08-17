document.addEventListener('DOMContentLoaded', () => {
  const loginTab = document.getElementById('tab-login');
  const registerTab = document.getElementById('tab-register');
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const authContainer = document.getElementById('auth-form-container');
  const dashboardContainer = document.getElementById('dashboard-container');
  
  // Tab Switching
  if (loginTab && registerTab) {
    loginTab.addEventListener('click', () => {
      loginTab.classList.add('active');
      registerTab.classList.remove('active');
      loginForm.style.display = 'block';
      registerForm.style.display = 'none';
    });

    registerTab.addEventListener('click', () => {
      registerTab.classList.add('active');
      loginTab.classList.remove('active');
      loginForm.style.display = 'none';
      registerForm.style.display = 'block';
    });
  }

  // Password Visibility Toggle
  document.querySelectorAll('.toggle-password').forEach(toggle => {
    toggle.addEventListener('click', () => {
      const targetId = toggle.getAttribute('data-target');
      const input = document.getElementById(targetId);
      if (input.type === 'password') {
        input.type = 'text';
        toggle.classList.replace('fa-eye', 'fa-eye-slash');
      } else {
        input.type = 'password';
        toggle.classList.replace('fa-eye-slash', 'fa-eye');
      }
    });
  });

  // Handle Login Submission
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();
      const password = document.getElementById('login-password').value;

      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();

        if (!res.ok) {
          showToast(data.detail || 'Login failed', 'error');
          return;
        }

        saveTokenAndLogin(data.access_token, data.user);
        showToast('Login successful!', 'success');
      } catch (err) {
        showToast('Network error while logging in', 'error');
      }
    });
  }

  // Handle Register Submission
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fullName = document.getElementById('register-name').value.trim();
      const email = document.getElementById('register-email').value.trim();
      const password = document.getElementById('register-password').value;

      try {
        const res = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ full_name: fullName, email, password })
        });
        const data = await res.json();

        if (!res.ok) {
          showToast(data.detail || 'Registration failed', 'error');
          return;
        }

        saveTokenAndLogin(data.access_token, data.user);
        showToast('Account created successfully!', 'success');
      } catch (err) {
        showToast('Network error while registering', 'error');
      }
    });
  }

  // Demo Google Sign-In Handler
  const demoGoogleBtn = document.getElementById('btn-google-demo');
  if (demoGoogleBtn) {
    demoGoogleBtn.addEventListener('click', async () => {
      const demoEmail = `google.user.${Math.floor(Math.random() * 8999 + 1000)}@gmail.com`;
      const demoName = `Google User ${Math.floor(Math.random() * 899 + 100)}`;
      
      try {
        const res = await fetch('/api/auth/google-demo', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: demoEmail, full_name: demoName })
        });
        const data = await res.json();
        
        if (res.ok) {
          saveTokenAndLogin(data.access_token, data.user);
          showToast('Authenticated via Google OAuth (Demo)!', 'success');
        } else {
          showToast(data.detail || 'Google Auth failed', 'error');
        }
      } catch (err) {
        showToast('Google auth error', 'error');
      }
    });
  }

  // Logout Handler
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('jwt_token');
      authContainer.style.display = 'block';
      dashboardContainer.style.display = 'none';
      showToast('Logged out successfully', 'success');
    });
  }

  // Copy JWT Token Button
  const copyTokenBtn = document.getElementById('copy-token-btn');
  if (copyTokenBtn) {
    copyTokenBtn.addEventListener('click', () => {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        navigator.clipboard.writeText(token);
        showToast('JWT Token copied to clipboard!', 'success');
      }
    });
  }

  // Auto Check Existing Session
  checkExistingSession();
});

// Helper: Save token and display dashboard / redirect to Homepage
function saveTokenAndLogin(token, user) {
  localStorage.setItem('jwt_token', token);
  // Show dashboard briefly or redirect to homepage
  if (window.location.pathname === '/auth' || window.location.pathname === '/login') {
    setTimeout(() => {
      window.location.href = '/';
    }, 1000);
  } else {
    renderDashboard(user, token);
  }
}

async function checkExistingSession() {
  const token = localStorage.getItem('jwt_token');
  if (!token) return;

  try {
    const res = await fetch('/api/auth/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      const user = await res.json();
      renderDashboard(user, token);
    } else {
      localStorage.removeItem('jwt_token');
    }
  } catch (e) {
    console.error('Session check failed', e);
  }
}

function renderDashboard(user, token) {
  const authContainer = document.getElementById('auth-form-container');
  const dashboardContainer = document.getElementById('dashboard-container');
  
  if (authContainer && dashboardContainer) {
    authContainer.style.display = 'none';
    dashboardContainer.style.display = 'block';

    document.getElementById('user-display-name').textContent = user.full_name || 'User';
    document.getElementById('user-display-email').textContent = user.email;
    document.getElementById('user-provider-badge').textContent = user.auth_provider === 'google' ? 'Google Auth' : 'Email/Password';
    document.getElementById('token-display').textContent = token;

    const avatar = document.getElementById('user-avatar-img');
    if (avatar) {
      avatar.src = user.picture || `https://api.dicebear.com/7.x/bottts/svg?seed=${user.email}`;
    }
  }
}

// Global Google Credential Handler for Google OAuth Script
window.handleGoogleCredentialResponse = async function(response) {
  try {
    const res = await fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential: response.credential })
    });
    const data = await res.json();
    if (res.ok) {
      saveTokenAndLogin(data.access_token, data.user);
      showToast('Signed in with Google!', 'success');
    } else {
      showToast(data.detail || 'Google sign in failed', 'error');
    }
  } catch (err) {
    showToast('Failed to authenticate with Google', 'error');
  }
};

// Toast Notifications
function showToast(message, type = 'error') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 4000);
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


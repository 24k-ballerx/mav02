/**
 * MAVERICK INTERNATIONAL SCHOOL PORTAL
 * Main JavaScript - Core functionality
 */

/* ============================================
   UTILITY FUNCTIONS
   ============================================ */

const Portal = {
  // Initialize portal
  init() {
    this.setupSidebar();
    this.setupDropdowns();
    this.setupClock();
    this.setupAnimations();
    this.setupActiveNav();
    this.setupToasts();
    this.loadUser();
  },

  /* ---- Sidebar ---- */
  setupSidebar() {
    const toggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (!toggle || !sidebar) return;

    const openSidebar = () => {
      sidebar.classList.add('open');
      overlay && overlay.classList.add('show');
      document.body.style.overflow = 'hidden';
    };

    const closeSidebar = () => {
      sidebar.classList.remove('open');
      overlay && overlay.classList.remove('show');
      document.body.style.overflow = '';
    };

    toggle.addEventListener('click', () => {
      if (sidebar.classList.contains('open')) closeSidebar();
      else openSidebar();
    });

    overlay && overlay.addEventListener('click', closeSidebar);

    // Close sidebar on resize to desktop
    window.addEventListener('resize', () => {
      if (window.innerWidth > 1024) closeSidebar();
    });
  },

  /* ---- Dropdowns ---- */
  setupDropdowns() {
    document.querySelectorAll('[data-dropdown]').forEach(trigger => {
      const targetId = trigger.dataset.dropdown;
      const menu = document.getElementById(targetId);
      if (!menu) return;

      trigger.addEventListener('click', (e) => {
        e.stopPropagation();
        // Close others
        document.querySelectorAll('.dropdown-menu.show').forEach(m => {
          if (m !== menu) m.classList.remove('show');
        });
        menu.classList.toggle('show');
      });
    });

    document.addEventListener('click', () => {
      document.querySelectorAll('.dropdown-menu.show').forEach(m => m.classList.remove('show'));
    });
  },

  /* ---- Live Clock ---- */
  setupClock() {
    const timeEl = document.getElementById('liveTime');
    const dateEl = document.getElementById('liveDate');
    if (!timeEl && !dateEl) return;

    const update = () => {
      const now = new Date();
      if (timeEl) {
        timeEl.textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      }
      if (dateEl) {
        dateEl.textContent = now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
      }
    };

    update();
    setInterval(update, 1000);
  },

  /* ---- Animate Elements on Scroll ---- */
  setupAnimations() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    }, { threshold: 0.05 });

    document.querySelectorAll('.animate-fadeInUp').forEach(el => {
      observer.observe(el);
    });

    // Counter animations
    document.querySelectorAll('.stat-value[data-count]').forEach(el => {
      const target = parseInt(el.dataset.count);
      const duration = 1200;
      const step = Math.ceil(target / (duration / 16));
      let current = 0;

      const tick = () => {
        current = Math.min(current + step, target);
        el.textContent = current.toLocaleString();
        if (current < target) requestAnimationFrame(tick);
      };

      // Start when visible
      const obs = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) {
          tick();
          obs.disconnect();
        }
      });
      obs.observe(el);
    });
  },

  /* ---- Active Nav Link ---- */
  setupActiveNav() {
    const current = window.location.pathname.split('/').pop() || 'dashboard.html';
    document.querySelectorAll('.nav-link').forEach(link => {
      const href = link.getAttribute('href');
      if (href && href === current) {
        link.classList.add('active');
      }
    });
  },

  /* ---- Toast System ---- */
  setupToasts() {
    // create container
    if (!document.getElementById('toastContainer')) {
      const container = document.createElement('div');
      container.id = 'toastContainer';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
  },

  showToast(message, type = 'info', duration = 3500) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <span class="toast-icon">${icons[type] || icons.info}</span>
      <span class="toast-msg">${message}</span>
    `;

    container.appendChild(toast);
    requestAnimationFrame(() => {
      requestAnimationFrame(() => toast.classList.add('show'));
    });

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 400);
    }, duration);
  },

  /* ---- User Session ---- */
  loadUser() {
    const user = this.getUser();
    if (!user) return;

    document.querySelectorAll('[data-user-name]').forEach(el => {
      el.textContent = user.name;
    });
    document.querySelectorAll('[data-user-role]').forEach(el => {
      el.textContent = user.role;
    });
    document.querySelectorAll('[data-user-initials]').forEach(el => {
      el.textContent = user.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
    });
  },

  getUser() {
    try {
      return JSON.parse(localStorage.getItem('mav_user')) || {
        name: 'Admin User',
        role: 'Administrator',
        email: 'admin@maverick.edu.ng'
      };
    } catch { return null; }
  },

  setUser(userData) {
    localStorage.setItem('mav_user', JSON.stringify(userData));
  },

  logout() {
    localStorage.removeItem('mav_user');
    window.location.href = 'index.html';
  }
};

/* ============================================
   MODAL HELPERS
   ============================================ */
const Modal = {
  open(id) {
    const overlay = document.getElementById(id);
    if (overlay) overlay.classList.add('show');
  },
  close(id) {
    const overlay = document.getElementById(id);
    if (overlay) overlay.classList.remove('show');
  },
  init() {
    document.querySelectorAll('[data-modal-open]').forEach(btn => {
      btn.addEventListener('click', () => this.open(btn.dataset.modalOpen));
    });
    document.querySelectorAll('[data-modal-close]').forEach(btn => {
      btn.addEventListener('click', () => this.close(btn.dataset.modalClose));
    });
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) this.close(overlay.id);
      });
    });
  }
};

/* ============================================
   TABLE SEARCH & FILTER
   ============================================ */
const TableHelper = {
  initSearch(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    if (!input || !table) return;

    input.addEventListener('input', () => {
      const q = input.value.toLowerCase();
      table.querySelectorAll('tbody tr').forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(q) ? '' : 'none';
      });
    });
  }
};

/* ============================================
   INIT ON DOM READY
   ============================================ */
document.addEventListener('DOMContentLoaded', () => {
  Portal.init();
  Modal.init();
});

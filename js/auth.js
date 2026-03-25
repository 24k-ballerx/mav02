/**
 * MAVERICK INTERNATIONAL SCHOOL PORTAL
 * Authentication Logic
 */

const Auth = {
    /* Demo credentials (matching backend seed_users.py) */
    users: [
        { role: 'Administrator', email: 'admin@maverick.edu.ng', password: 'admin123' },
        { role: 'Teacher',       email: 'teacher@maverick.edu.ng', password: 'teacher123' },
        { role: 'Student',       email: 'student@maverick.edu.ng', password: 'student123' },
        { role: 'Parent',        email: 'parent@maverick.edu.ng', password: 'parent123' },
    ],

    init() {
        const form = document.getElementById('loginForm');
        if (!form) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // Quick-fill demo
        document.querySelectorAll('[data-demo-role]').forEach(btn => {
            btn.addEventListener('click', () => {
                const role = btn.dataset.demoRole;
                const user = this.users.find(u => u.role.toLowerCase() === role.toLowerCase());
                if (user) {
                    document.getElementById('loginEmail').value = user.email;
                    document.getElementById('loginPassword').value = user.password;
                    document.getElementById('loginEmail').dispatchEvent(new Event('input'));
                }
            });
        });

        // Password toggle
        const eyeBtn = document.getElementById('togglePassword');
        const pwInput = document.getElementById('loginPassword');
        if (eyeBtn && pwInput) {
            eyeBtn.addEventListener('click', () => {
                const isText = pwInput.type === 'text';
                pwInput.type = isText ? 'password' : 'text';
                eyeBtn.textContent = isText ? '👁️' : '🙈';
            });
        }

        // Input animation
        document.querySelectorAll('.form-control').forEach(input => {
            input.addEventListener('input', () => {
                input.classList.toggle('has-value', input.value.length > 0);
            });
        });
    },

    async handleLogin() {
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;
        const btn = document.getElementById('loginBtn');
        const errorEl = document.getElementById('loginError');

        if (!email || !password) return;

        // Show loading
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span> Signing in...';
        }
        if (errorEl) errorEl.style.display = 'none';

        try {
            const response = await fetch(`${Portal.API_BASE}/auth/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Clear any existing session data to prevent corruption
                localStorage.clear();

                // Backend returns { access, refresh, user: { ... } }
                Portal.setUser(data.user, { 
                    access: data.access, 
                    refresh: data.refresh 
                });
                
                // Success feedback
                if (btn) btn.innerHTML = '<span>✅</span> Success!';
                
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 500);
            } else {
                throw new Error(data.detail || 'Invalid credentials. Please try again.');
            }
        } catch (err) {
            console.error('Login error:', err);
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<span>🔐</span> Sign In';
            }
            if (errorEl) {
                errorEl.textContent = `❌ ${err.message}`;
                errorEl.style.display = 'block';
            }
        }
    },

    /* Guard pages that require login */
    guard() {
        const user = Portal.getUser();
        if (!user) {
            window.location.href = 'index.html';
            return false;
        }
        return true;
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Auth.init();
});

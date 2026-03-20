/**
 * MAVERICK INTERNATIONAL SCHOOL PORTAL
 * Students Module Frontend Logic
 */

const Students = {
    init() {
        this.fetchStudents();
        this.setupSearch();
    },

    async fetchStudents(query = '') {
        const tableBody = document.getElementById('studentsTableBody');
        const loadingRow = document.getElementById('loadingRow');
        
        try {
            const response = await Portal.apiFetch(`/students/${query}`);
            if (!response || !response.ok) {
                throw new Error('Failed to fetch students');
            }

            const data = await response.json();
            const students = data.results || data; // Handle pagination if present

            this.renderStudents(students);
        } catch (err) {
            console.error('Error fetching students:', err);
            if (tableBody) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="7" style="text-align: center; padding: 40px; color: var(--danger);">
                            ❌ Error loading students. Please try again.
                        </td>
                    </tr>
                `;
            }
        }
    },

    renderStudents(students) {
        const tableBody = document.getElementById('studentsTableBody');
        if (!tableBody) return;

        if (students.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 40px; color: var(--text-muted);">
                        No students found.
                    </td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = students.map(student => `
            <tr class="animate-fadeInUp">
                <td>
                    <div class="student-cell">
                        <div class="avatar student-photo" style="background: var(--accent);">
                            ${student.initials || student.first_name[0] + student.last_name[0]}
                        </div>
                        <div class="student-cell-info">
                            <div class="s-name">${student.first_name} ${student.last_name}</div>
                            <div class="s-id">${student.email}</div>
                        </div>
                    </div>
                </td>
                <td><code>${student.student_id || 'N/A'}</code></td>
                <td><span class="badge badge-primary">${student.class_name || 'N/A'}</span></td>
                <td>${student.gender ? student.gender.charAt(0).toUpperCase() + student.gender.slice(1) : 'N/A'}</td>
                <td>${new Date(student.date_joined).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}</td>
                <td><span class="badge badge-success">Active</span></td>
                <td>
                    <div class="action-group">
                        <button class="btn btn-outline btn-icon btn-sm">👁️</button>
                        <button class="btn btn-outline btn-icon btn-sm">✏️</button>
                        <button class="btn btn-danger btn-icon btn-sm">🗑️</button>
                    </div>
                </td>
            </tr>
        `).join('');
    },

    setupSearch() {
        const searchInput = document.getElementById('studentSearch');
        if (!searchInput) return;

        let debounceTimer;
        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const query = searchInput.value.trim();
                this.fetchStudents(query ? `?search=${encodeURIComponent(query)}` : '');
            }, 500);
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Students.init();
});

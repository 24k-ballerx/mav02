/**
 * MAVERICK INTERNATIONAL SCHOOL PORTAL
 * Courses Module Frontend Logic
 */

const Courses = {
    init() {
        this.fetchCourses();
        this.setupSearch();
        this.setupAddForm();
    },

    async fetchCourses(query = '') {
        const grid = document.getElementById('coursesGrid');
        
        try {
            const response = await Portal.apiFetch(`/courses/${query}`);
            if (!response || !response.ok) {
                throw new Error('Failed to fetch courses');
            }

            const data = await response.json();
            const courses = data.results || data; // Handle pagination if present
            this.renderCourses(courses);
        } catch (err) {
            console.error('Error fetching courses:', err);
            if (grid) {
                grid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 60px; color: var(--danger);">
                        ❌ Error loading courses catalog. Please try again.
                    </div>
                `;
            }
        }
    },

    renderCourses(courses) {
        const grid = document.getElementById('coursesGrid');
        if (!grid) return;

        if (courses.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 60px; color: var(--text-muted);">
                    No courses found in the catalog.
                </div>
            `;
            return;
        }

        grid.innerHTML = courses.map(course => {
            const emojiMap = {
                'Mathematics': '➗',
                'English': '📖',
                'Computer Science': '💻',
                'Science': '🔬',
                'Physics': '⚡',
                'Chemistry': '⚗️',
                'Biology': '🧬',
                'History': '📜',
                'Arts': '🎨',
                'Commerce': '💰'
            };
            const emoji = emojiMap[course.department] || '📚';
            const colorClass = this.getColorClass(course.department);

            return `
                <div class="course-card animate-fadeInUp">
                    <div class="course-header ${colorClass}">${emoji}</div>
                    <div class="course-body">
                        <div class="course-name">${course.title}</div>
                        <div class="course-code">${course.code} · ${course.department}</div>
                        <div class="course-meta">
                            <span class="badge badge-primary">All Tracks</span>
                            <span class="badge badge-success">Active</span>
                        </div>
                        <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">
                            Students Enrolled: <strong>${course.student_count || 0}</strong>
                        </div>
                        <div class="progress-bar-wrap">
                            <div class="progress-bar-fill" style="width:0%"></div>
                        </div>
                        <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">0% syllabus covered</div>
                        <div class="course-teacher">
                            <div class="t-avatar">
                                ${course.teacher_details ? (course.teacher_details.initials || course.teacher_details.first_name[0] + course.teacher_details.last_name[0]) : '??'}
                            </div> 
                            ${course.teacher_details ? `Mr/Mrs. ${course.teacher_details.last_name}` : 'No Teacher Assigned'}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    },

    getColorClass(dept) {
        const map = {
            'Mathematics': 'cc-math',
            'English': 'cc-english',
            'Computer Science': 'cc-science',
            'Science': 'cc-science',
            'Physics': 'cc-phy',
            'Chemistry': 'cc-chem',
            'Biology': 'cc-bio',
            'History': 'cc-history',
            'Arts': 'cc-english',
            'Commerce': 'cc-commerce'
        };
        return map[dept] || 'cc-math';
    },

    setupSearch() {
        const searchInput = document.getElementById('courseSearch');
        let debounceTimer;

        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    const query = e.target.value.trim();
                    const queryString = query ? `?search=${encodeURIComponent(query)}` : '';
                    this.fetchCourses(queryString);
                }, 400);
            });
        }
    },

    openAddModal() {
        const modal = document.getElementById('addCourseModal');
        if (modal) modal.style.display = 'flex';
    },

    closeAddModal() {
        const modal = document.getElementById('addCourseModal');
        if (modal) {
            modal.style.display = 'none';
            document.getElementById('addCourseForm').reset();
        }
    },

    setupAddForm() {
        const form = document.getElementById('addCourseForm');
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('acSubmitBtn');
            const originalText = btn.textContent;
            
            const payload = {
                code: document.getElementById('acCode').value.trim(),
                title: document.getElementById('acTitle').value.trim(),
                department: document.getElementById('acDept').value,
                description: document.getElementById('acDesc').value.trim()
            };

            try {
                btn.disabled = true;
                btn.textContent = 'Saving...';

                const response = await Portal.apiFetch('/courses/', {
                    method: 'POST',
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    Portal.showToast('Course added successfully!', 'success');
                    this.closeAddModal();
                    this.fetchCourses(); // Refresh list
                } else {
                    const errorData = await response.json();
                    let errMsg = 'Failed to add course.';
                    if (errorData.code) errMsg += ` ${errorData.code[0]}`;
                    Portal.showToast(errMsg, 'danger');
                }
            } catch (err) {
                console.error(err);
                Portal.showToast('Network error while saving course.', 'danger');
            } finally {
                btn.disabled = false;
                btn.textContent = originalText;
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Courses.init();
});

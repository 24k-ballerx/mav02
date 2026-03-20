/**
 * MAVERICK INTERNATIONAL SCHOOL PORTAL
 * Courses Module Frontend Logic
 */

const Courses = {
    init() {
        this.fetchCourses();
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
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Courses.init();
});

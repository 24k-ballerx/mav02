/**
 * MAVERICK INTERNATIONAL SCHOOL PORTAL
 * Timetable Module Frontend Logic
 */

const Timetable = {
    init() {
        this.currentClass = document.querySelector('.class-btn.active').textContent.trim();
        this.setupClassSelector();
        this.fetchTimetable(this.currentClass);
    },

    setupClassSelector() {
        document.querySelectorAll('.class-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.class-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.currentClass = btn.textContent.trim();
                
                Portal.showToast(`Showing timetable for ${this.currentClass}`, 'info', 2000);
                this.fetchTimetable(this.currentClass);
            });
        });
    },

    async fetchTimetable(targetClass) {
        const tbody = document.getElementById('timetableBody');
        tbody.innerHTML = `<tr><td colspan="6" style="padding:40px; text-align:center;"><div class="spinner" style="margin:0 auto;"></div><p style="margin-top:10px;color:var(--text-muted)">Loading Schedule...</p></td></tr>`;
        
        try {
            const response = await Portal.apiFetch(`/timetable/?target_class=${encodeURIComponent(targetClass)}`);
            if (!response.ok) throw new Error('Failed to fetch format');
            const data = await response.json();
            const entries = data.results || data;
            
            this.renderTimetable(entries);
        } catch (err) {
            console.error(err);
            tbody.innerHTML = `<tr><td colspan="6" style="padding:40px; text-align:center; color:var(--danger)">❌ Failed to load schedule.</td></tr>`;
        }
    },

    renderTimetable(entries) {
        const tbody = document.getElementById('timetableBody');
        if (!tbody) return;

        // Group by period (1-7)
        const periods = {};
        for(let i=1; i<=7; i++) {
            periods[i] = []; // index 0=Mon, 4=Fri
            for(let d=0; d<5; d++) periods[i].push(null);
        }

        // Add typical start times for mapping
        const timeMap = {
            1: '8:00 – 8:40',
            2: '8:40 – 9:20',
            3: '9:20 – 10:00',
            4: '10:20 – 11:00',
            5: '11:00 – 11:40',
            6: '12:20 – 1:00',
            7: '1:00 – 1:40'
        };

        entries.forEach(e => {
            if (periods[e.period]) {
                periods[e.period][e.day_of_week] = e;
                if(e.start_time) {
                    const start = e.start_time.substring(0,5);
                    const end = e.end_time.substring(0,5);
                    timeMap[e.period] = `${start} – ${end}`;
                }
            }
        });

        let html = '';
        const today = new Date().getDay() - 1; // 0=Mon

        // Helper to generate a cell
        const genCell = (entry, dayIndex) => {
            const isToday = dayIndex === today ? 'today-col' : '';
            if (!entry) {
                return `<td class="${isToday}"><div class="tt-cell" style="align-items:center;opacity:0.5">-</div></td>`;
            }

            const dept = entry.course_details ? entry.course_details.department : '';
            const colorClass = this.getColorClass(dept);
            const teacherName = entry.course_details && entry.course_details.teacher_details ? 
                `Mr/Mrs. ${entry.course_details.teacher_details.last_name}` : 'Staff';

            return `
                <td class="${isToday}">
                    <div class="tt-cell">
                        <div class="tt-lesson ${colorClass}">
                            <div class="tt-lesson-name">${entry.course_details ? entry.course_details.title : entry.course}</div>
                            <div class="tt-lesson-teacher">${teacherName}</div>
                            <div class="tt-lesson-room">${entry.room}</div>
                        </div>
                    </div>
                </td>
            `;
        };

        for(let p=1; p<=3; p++) {
            html += `<tr><td><div class="tt-time">${timeMap[p]}<span>Period ${p}</span></div></td>`;
            for(let d=0; d<5; d++) html += genCell(periods[p][d], d);
            html += `</tr>`;
        }

        html += `<tr class="tt-break"><td colspan="6"><div class="tt-break-content">☕ Short Break — 10:00 to 10:20</div></td></tr>`;

        for(let p=4; p<=5; p++) {
            html += `<tr><td><div class="tt-time">${timeMap[p]}<span>Period ${p}</span></div></td>`;
            for(let d=0; d<5; d++) html += genCell(periods[p][d], d);
            html += `</tr>`;
        }

        html += `<tr class="tt-break"><td colspan="6"><div class="tt-break-content">🍽️ Lunch Break — 11:40 to 12:20 PM</div></td></tr>`;

        for(let p=6; p<=7; p++) {
            html += `<tr><td><div class="tt-time">${timeMap[p]}<span>Period ${p}</span></div></td>`;
            for(let d=0; d<5; d++) html += genCell(periods[p][d], d);
            html += `</tr>`;
        }

        tbody.innerHTML = html;
    },

    getColorClass(dept) {
        const map = {
            'Mathematics': 's-math',
            'English': 's-eng',
            'Computer Science': 's-civic',
            'Science': 's-phy',
            'Physics': 's-phy',
            'Chemistry': 's-chem',
            'Biology': 's-bio',
            'History': 's-lit',
            'Arts': 's-eng',
            'Commerce': 's-crs'
        };
        return map[dept] || 's-math';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Timetable.init();
});

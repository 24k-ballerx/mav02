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

        // Group by period (1-10)
        const maxPeriod = Math.max(...entries.map(e => e.period), 8);
        const periods = {};
        for(let i=1; i<=maxPeriod; i++) {
            periods[i] = []; // index 0=Mon, 4=Fri
            for(let d=0; d<5; d++) periods[i].push(null);
        }

        const timeMap = {};
        entries.forEach(e => {
            if (periods[e.period]) {
                periods[e.period][e.day_of_week] = e;
                if(e.start_time && !timeMap[e.period]) {
                    const start = e.start_time.substring(0,5);
                    const end = e.end_time.substring(0,5);
                    timeMap[e.period] = `${start} – ${end}`;
                }
            }
        });

        let html = '';
        const today = new Date().getDay() - 1; // 0=Mon, 4=Fri

        const genCell = (entry, dayIndex) => {
            const isToday = dayIndex === today ? 'today-col' : '';
            if (!entry) {
                return `<td class="${isToday}"><div class="tt-cell" style="align-items:center;opacity:0.5">-</div></td>`;
            }

            const details = entry.course_details || {};
            const dept = details.department || '';
            const colorClass = this.getColorClass(dept);
            const teacherName = details.teacher_details ? 
                `Mr/Mrs. ${details.teacher_details.last_name}` : 'Staff';

            return `
                <td class="${isToday}">
                    <div class="tt-cell">
                        <div class="tt-lesson ${colorClass}">
                            <div class="tt-lesson-name">${details.title || entry.course}</div>
                            <div class="tt-lesson-teacher">${teacherName}</div>
                            <div class="tt-lesson-room">${entry.room}</div>
                        </div>
                    </div>
                </td>
            `;
        };

        for(let p=1; p<=maxPeriod; p++) {
            const timeRange = timeMap[p] || '--:-- – --:--';
            html += `<tr><td><div class="tt-time">${timeRange}<span>Period ${p}</span></div></td>`;
            for(let d=0; d<5; d++) html += genCell(periods[p][d], d);
            html += `</tr>`;

            // Nigerian Break Structure
            if (p === 3) {
                html += `<tr class="tt-break"><td colspan="6"><div class="tt-break-content">☕ Short Break — 10:30 to 10:50</div></td></tr>`;
            } else if (p === 6) {
                html += `<tr class="tt-break"><td colspan="6"><div class="tt-break-content">🍽️ Long Break (Lunch) — 12:50 to 1:30 PM</div></td></tr>`;
            }
        }

        tbody.innerHTML = html;
        console.log(`Rendered ${maxPeriod} periods for ${this.currentClass}`);
    },

    getColorClass(dept) {
        const map = {
            'Mathematics': 's-math',
            'English': 's-eng',
            'Science': 's-bio',
            'Physics': 's-phy',
            'Chemistry': 's-chem',
            'Biology': 's-bio',
            'Arts': 's-eng',
            'History': 's-lit',
            'Commerce': 's-crs',
            'Computer Science': 's-civic'
        };
        return map[dept] || 's-math';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Timetable.init();
});

/**
 * MAVERICK INTERNATIONAL SCHOOL PORTAL
 * Dashboard Logic
 */

const Dashboard = {
    init() {
        this.fetchStats();
        this.updateProfileInfo();
    },

    async fetchStats() {
        try {
            const response = await Portal.apiFetch('/auth/stats/');
            if (!response.ok) throw new Error('Failed to fetch stats');
            
            const stats = await response.json();
            this.renderStats(stats);
        } catch (err) {
            console.error('Error fetching dashboard stats:', err);
        }
    },

    renderStats(stats) {
        const setVal = (id, val) => {
            const el = document.getElementById(id);
            if (el) el.textContent = val.toLocaleString();
        };

        setVal('statTotalStudents', stats.total_students);
        setVal('statTotalTeachers', stats.total_teachers);
        setVal('statTotalCourses', stats.total_courses);
        setVal('statTotalNotices', stats.total_notices);
        
        // Update specific stats in cards if they exist
        const totalNoticesEl = document.querySelector('#noticeStatsCount');
        if (totalNoticesEl) totalNoticesEl.textContent = stats.total_notices.toLocaleString();
    },

    updateProfileInfo() {
        const user = Portal.getUser();
        if (!user) return;

        // Update welcome message
        const welcomeEl = document.querySelector('.welcome-text h2');
        if (welcomeEl) {
            welcomeEl.textContent = `Welcome back, ${user.first_name}! 👋`;
        }
    }
};

// Helper for finding elements by text content (since I don't want to add IDs to every single thing yet)
if (!window.NodeList.prototype.forEach) {
    window.NodeList.prototype.forEach = Array.prototype.forEach;
}

document.addEventListener('DOMContentLoaded', () => {
    Dashboard.init();
});

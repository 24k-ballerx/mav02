/**
 * MAVERICK INTERNATIONAL SCHOOL PORTAL
 * Notices & Announcements Frontend Logic
 */

const Notices = {
    init() {
        this.fetchNotices();
        this.setupCompose();
        this.setupFilters();
    },

    async fetchNotices(queryParams = '') {
        const noticesList = document.getElementById('noticesList');
        const loading = document.getElementById('noticesLoading');
        
        try {
            const response = await Portal.apiFetch(`/notices/${queryParams}`);
            if (!response || !response.ok) throw new Error('Failed to fetch notices');

            const data = await response.json();
            const notices = data.results || data;

            if (loading) loading.style.display = 'none';
            this.renderNotices(notices);
        } catch (err) {
            console.error('Error fetching notices:', err);
            if (noticesList) {
                noticesList.innerHTML = `
                    <div class="card" style="padding: 40px; text-align: center; color: var(--danger);">
                        ❌ Error loading announcements. Please try again.
                    </div>
                `;
            }
        }
    },

    renderNotices(notices) {
        const noticesList = document.getElementById('noticesList');
        if (!noticesList) return;

        // Keep the toolbar/loading etc if they are inside, or just clear and prepend?
        // Let's assume noticesList is the container forcards.
        
        if (notices.length === 0) {
            noticesList.innerHTML = `
                <div class="card" style="padding: 60px; text-align: center; color: var(--text-muted);">
                    No announcements found.
                </div>
            `;
            return;
        }

        noticesList.innerHTML = notices.map((notice, index) => {
            const date = new Date(notice.created_at).toLocaleDateString('en-US', {
                month: 'short', day: 'numeric', year: 'numeric'
            });
            const initials = notice.author_details ? notice.author_details.initials : '??';
            const authorName = notice.author_details ? `${notice.author_details.first_name} ${notice.author_details.last_name}` : 'Unknown';
            const role = notice.author_details ? notice.author_details.role : 'Staff';
            
            let accentColor = 'var(--primary)';
            if (notice.category === 'urgent') accentColor = 'var(--danger)';
            else if (notice.category === 'event') accentColor = 'var(--accent)';
            else if (notice.category === 'finance') accentColor = 'var(--gold)';
            else if (notice.category === 'academic') accentColor = '#8e44ad';

            return `
                <div class="notice-card ${notice.is_urgent ? 'notice-urgent' : ''} animate-fadeInUp" style="animation-delay: ${index * 0.1}s">
                    <div class="notice-accent" style="background: ${accentColor};"></div>
                    <div class="notice-body">
                        <div class="notice-head">
                            <div class="notice-title">${notice.is_urgent ? '🚨 ' : ''}${notice.title}</div>
                            <span class="badge ${notice.is_urgent ? 'badge-danger' : 'badge-info'}">${notice.category_display}</span>
                        </div>
                        <div class="notice-meta">
                            <span class="notice-meta-item">📅 ${date}</span>
                            <span class="notice-meta-item">👥 ${notice.audience_display}</span>
                            <span class="notice-meta-item">👁 ${notice.views} views</span>
                        </div>
                        <div class="notice-excerpt">
                            ${notice.content}
                        </div>
                        <div class="notice-footer">
                            <div class="notice-author">
                                <div class="notice-author-av" style="background: ${this.getGradientForCategory(notice.category)}">${initials}</div> 
                                Posted by <strong>${authorName}</strong> (${role})
                            </div>
                            <button class="btn btn-outline btn-sm" onclick="Notices.viewDetails(${notice.id})">Read More →</button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    },

    getGradientForCategory(cat) {
        if (cat === 'urgent') return 'linear-gradient(135deg, var(--danger), #c0392b)';
        if (cat === 'event') return 'linear-gradient(135deg, var(--accent), #2ecc71)';
        if (cat === 'finance') return 'linear-gradient(135deg, #c9a84c, #e8c96d)';
        return 'linear-gradient(135deg, var(--primary), var(--accent))';
    },

    setupCompose() {
        const publishBtn = document.querySelector('.compose-panel .btn-primary');
        if (!publishBtn) return;

        publishBtn.onclick = async () => {
            const panel = document.querySelector('.compose-panel');
            const title = panel.querySelector('input[type="text"]').value;
            const category = panel.querySelector('select:nth-of-type(1)').value;
            const audience = panel.querySelector('select:nth-of-type(2)').value;
            const content = panel.querySelector('textarea').value;

            if (!title || !content) {
                Portal.showToast('Please fill in both title and message.', 'warning');
                return;
            }

            publishBtn.disabled = true;
            publishBtn.textContent = 'Publishing...';

            try {
                const response = await Portal.apiFetch('/notices/', {
                    method: 'POST',
                    body: JSON.stringify({
                        title,
                        content,
                        category,
                        audience,
                        is_urgent: category === 'urgent'
                    })
                });

                if (response.ok) {
                    Portal.showToast('Announcement published successfully!', 'success');
                    // Reset form
                    panel.querySelector('input[type="text"]').value = '';
                    panel.querySelector('textarea').value = '';
                    // Refresh list
                    this.fetchNotices();
                } else {
                    throw new Error('Failed to post notice');
                }
            } catch (err) {
                console.error('Error posting notice:', err);
                Portal.showToast('Failed to publish notice. Check permissions.', 'danger');
            } finally {
                publishBtn.disabled = false;
                publishBtn.textContent = '📢 Publish Notice';
            }
        };
    },

    setupFilters() {
        const searchInput = document.querySelector('.search-bar input');
        const categorySelect = document.querySelector('select.form-control');
        
        const update = () => {
            const search = searchInput ? searchInput.value : '';
            const cat = categorySelect ? categorySelect.value : 'All Categories';
            
            let query = `?search=${encodeURIComponent(search)}`;
            if (cat !== 'All Categories') query += `&category=${cat.toLowerCase().replace(' events', 'event')}`;
            
            this.fetchNotices(query);
        };

        if (categorySelect) categorySelect.addEventListener('change', update);
        
        let debounce;
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                clearTimeout(debounce);
                debounce = setTimeout(update, 500);
            });
        }
    },

    viewDetails(id) {
        // Increment view count via API and maybe show a modal?
        // Currently we just fetch and refresh to show incremented views
        Portal.apiFetch(`/notices/${id}/`).then(() => this.fetchNotices());
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Notices.init();
});

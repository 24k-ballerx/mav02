const Results = {
    currentTab: 'report',

    init() {
        this.fetchResults();
        this.fetchClassResults();
        this.setupFilters();
        this.setupTabs();
    },

    async fetchResults(queryParams = '') {
        const tableBody = document.getElementById('resultsTableBody');
        if (!tableBody) return;
        
        try {
            // Fetch results for the current student (or filtered by admin)
            const response = await Portal.apiFetch(`/results/${queryParams}`);
            if (!response || !response.ok) throw new Error('Failed to fetch results');

            const data = await response.json();
            const results = data.results || data;

            this.renderReportCard(results);
            if (results.length > 0) this.updateStudentInfo(results[0]);
        } catch (err) {
            console.error('Error fetching results:', err);
            tableBody.innerHTML = `<tr><td colspan="7" class="text-center" style="padding:40px; color:var(--danger);">❌ Error loading results.</td></tr>`;
        }
    },

    async fetchClassResults(queryParams = '') {
        const tableBody = document.getElementById('classResultsTableBody');
        if (!tableBody) return;

        try {
            const response = await Portal.apiFetch(`/results/${queryParams}`);
            if (!response || !response.ok) throw new Error('Failed to fetch class results');

            const data = await response.json();
            const results = data.results || data;

            this.renderClassResults(results);
        } catch (err) {
            console.error('Error fetching class results:', err);
            tableBody.innerHTML = `<tr><td colspan="7" class="text-center" style="padding:40px; color:var(--danger);">❌ Error loading class results.</td></tr>`;
        }
    },

    renderReportCard(results) {
        const tableBody = document.getElementById('resultsTableBody');
        if (!tableBody) return;

        if (results.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="7" class="text-center" style="padding:40px; color:var(--text-muted);">No results found for this term.</td></tr>`;
            this.updateSummary(0, 0);
            return;
        }

        let totalPoints = 0;
        tableBody.innerHTML = results.map((res, index) => {
            totalPoints += res.total_score;
            const scorePercent = res.total_score;
            let gradient = 'linear-gradient(90deg, #1e5aad, #27ae60)';
            if (scorePercent < 50) gradient = 'linear-gradient(90deg, #e74c3c, #c0392b)';
            else if (scorePercent < 70) gradient = 'linear-gradient(90deg, #c9a84c, #e8c96d)';

            return `
                <tr class="animate-fadeInUp" style="animation-delay: ${index * 0.05}s">
                    <td>${index + 1}</td>
                    <td><strong>${res.course.title}</strong><br><small style="color:var(--text-muted)">${res.course.code}</small></td>
                    <td>${res.ca_score}</td>
                    <td>${res.exam_score}</td>
                    <td>
                        <div class="score-bar">
                            <div class="score-bar-track"><div class="score-bar-fill" style="width: ${scorePercent}%; background: ${gradient}"></div></div>
                            <span class="score-bar-val">${res.total_score}</span>
                        </div>
                    </td>
                    <td><span class="badge grade-${res.grade.charAt(0)}">${res.grade}</span></td>
                    <td>${res.remarks || 'N/A'}</td>
                </tr>
            `;
        }).join('');

        const average = (totalPoints / results.length).toFixed(1);
        this.updateSummary(totalPoints, average, results.length * 100);
    },

    renderClassResults(results) {
        const tableBody = document.getElementById('classResultsTableBody');
        if (!tableBody) return;

        if (results.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="7" class="text-center" style="padding:40px; color:var(--text-muted);">No records found matching criteria.</td></tr>`;
            return;
        }

        // Sort by total score descending for positions
        const sorted = [...results].sort((a, b) => b.total_score - a.total_score);

        tableBody.innerHTML = sorted.map((res, index) => {
            const pos = index + 1;
            const medal = pos === 1 ? '🥇 ' : pos === 2 ? '🥈 ' : pos === 3 ? '🥉 ' : '';
            return `
                <tr class="animate-fadeInUp" style="animation-delay: ${index * 0.05}s">
                    <td>${index + 1}</td>
                    <td><strong>${res.student.full_name || res.student.first_name + ' ' + res.student.last_name}</strong></td>
                    <td>${res.ca_score}</td>
                    <td>${res.exam_score}</td>
                    <td><strong>${res.total_score}</strong></td>
                    <td><span class="badge grade-${res.grade.charAt(0)}">${res.grade}</span></td>
                    <td>${medal}${pos}${this.getOrdinal(pos)}</td>
                </tr>
            `;
        }).join('');
    },

    getOrdinal(n) {
        const s = ["th", "st", "nd", "rd"], v = n % 100;
        return (s[(v - 20) % 10] || s[v] || s[0]);
    },

    updateStudentInfo(firstResult) {
        if (!firstResult || !firstResult.student) return;
        const s = firstResult.student;
        document.querySelectorAll('#rcStudentName').forEach(el => el.textContent = `${s.first_name} ${s.last_name}`);
        document.querySelectorAll('#rcStudentID').forEach(el => el.textContent = s.student_id || 'N/A');
        document.querySelectorAll('#rcStudentClass').forEach(el => el.textContent = s.class_name || 'N/A');
    },

    updateSummary(total, average, max) {
        const totalEl = document.getElementById('rcTotalScore');
        const averageEl = document.getElementById('rcAverage');
        if (totalEl) totalEl.textContent = `${total} / ${max}`;
        if (averageEl) averageEl.textContent = `${average}%`;
    },

    setupFilters() {
        const termSelect = document.getElementById('termFilter');
        const yearSelect = document.getElementById('yearFilter');
        const searchInput = document.getElementById('studentSearch');
        
        const update = () => {
            const term = termSelect ? termSelect.value : '';
            const year = yearSelect ? yearSelect.value : '';
            const search = searchInput ? searchInput.value : '';
            const params = `?term=${term}&academic_year=${year}&search=${encodeURIComponent(search)}`;
            
            if (this.currentTab === 'report') this.fetchResults(params);
            else this.fetchClassResults(params);
        };

        [termSelect, yearSelect].forEach(el => el && el.addEventListener('change', update));
        
        let debounce;
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                clearTimeout(debounce);
                debounce = setTimeout(update, 500);
            });
        }
    },

    setupTabs() {
        // Intercept the global showTab call to track state
        const originalShowTab = window.showTab;
        window.showTab = (tab) => {
            this.currentTab = tab;
            originalShowTab(tab);
            // Refresh current tab data
            const term = document.getElementById('termFilter')?.value || '';
            const year = document.getElementById('yearFilter')?.value || '';
            const search = document.getElementById('studentSearch')?.value || '';
            const params = `?term=${term}&academic_year=${year}&search=${encodeURIComponent(search)}`;
            
            if (tab === 'report') this.fetchResults(params);
            else if (tab === 'table') this.fetchClassResults(params);
        };
    },

    handleFileSelect(event) {
        const file = event.target.files[0];
        const label = document.getElementById('dropZoneText');
        if (file) {
            label.textContent = `Selected: ${file.name}`;
            label.style.color = 'var(--accent)';
        } else {
            label.textContent = 'Click to choose file or drag & drop';
            label.style.color = 'var(--text-primary)';
        }
    },

    async uploadScores() {
        const fileInput = document.getElementById('upFile');
        const classSelect = document.getElementById('upClass');
        const subjectSelect = document.getElementById('upSubject');
        const termSelect = document.getElementById('upTerm');
        
        const file = fileInput.files[0];
        if (!file) {
            Portal.showToast('Please select a CSV file first.', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('class', classSelect.value);
        formData.append('subject', subjectSelect.value);
        formData.append('term', termSelect.value);

        const btn = document.getElementById('upBtn');
        const originalText = btn.innerHTML;
        btn.innerHTML = 'Uploading... <div class="spinner" style="width:14px;height:14px;border-width:2px;display:inline-block;vertical-align:middle;margin-left:8px;"></div>';
        btn.disabled = true;

        try {
            // Using mav_access and Bearer to match JWT backend
            const token = localStorage.getItem('mav_access');
            if (!token) throw new Error('You must be logged in to upload results.');

            const headers = { 
                'Authorization': `Bearer ${token}`
                // Note: Content-Type is NOT set for FormData to let browser add boundary
            };
            
            const response = await fetch(`${Portal.API_BASE}/results/upload/`, {
                method: 'POST',
                headers: headers,
                body: formData
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || `Upload failed with status ${response.status}`);
            
            Portal.showToast(`Success! ${data.message}`, 'success');
            
            // Output warnings if any
            if (data.errors && data.errors.length > 0) {
                console.warn('Upload issues:', data.errors);
                Portal.showToast(`Finished with ${data.errors.length} skipped records (see console).`);
            }
            
            // clear form
            fileInput.value = '';
            document.getElementById('dropZoneText').textContent = 'Click to choose file or drag & drop';
            document.getElementById('dropZoneText').style.color = 'var(--text-primary)';
            
            // Switch to class results to view uploaded data
            setTimeout(() => { 
                if (typeof showTab === 'function') showTab('table'); 
            }, 1500);
            
        } catch (err) {
            console.error('Upload Error:', err);
            Portal.showToast(err.message, 'error');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Results.init();
});

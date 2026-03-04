/**
 * Enigma LIMS – Shared Application Utilities
 */

/* ─── Toast Notifications ──────────────────────────────────────────── */
function showToast(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = 'position:fixed;top:1rem;right:1rem;z-index:9999;display:flex;flex-direction:column;gap:0.5rem;width:22rem;pointer-events:none;';
        document.body.appendChild(container);
    }
    const colors = { success:'#22c55e', error:'#ef4444', warning:'#f59e0b', info:'#2E86DE' };
    const icons  = { success:'fa-check-circle', error:'fa-exclamation-circle', warning:'fa-exclamation-triangle', info:'fa-info-circle' };
    const c = colors[type] || colors.info;
    const toast = document.createElement('div');
    toast.setAttribute('data-toast','');
    toast.style.cssText = `display:flex;align-items:flex-start;gap:0.75rem;padding:0.875rem 1rem;background:#1e293b;border:1px solid #334155;border-left:4px solid ${c};border-radius:0.5rem;color:#f1f5f9;box-shadow:0 10px 25px rgba(0,0,0,0.5);pointer-events:all;transition:all 0.35s ease;`;
    toast.innerHTML = `<i class="fas ${icons[type]||'fa-info-circle'}" style="color:${c};margin-top:2px;flex-shrink:0;"></i><span style="font-size:0.875rem;flex:1;line-height:1.4;">${message}</span><button onclick="this.closest('[data-toast]').remove()" style="background:none;border:none;color:#64748b;cursor:pointer;padding:0;line-height:1;pointer-events:all;" title="Dismiss"><i class="fas fa-times" style="font-size:0.75rem;"></i></button>`;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity='0'; toast.style.transform='translateX(110%)'; setTimeout(()=>toast.remove(),350); }, 4500);
}

/* ─── Loading Overlay ───────────────────────────────────────────────── */
function showLoading(show) {
    let overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;z-index:9998;';
        overlay.innerHTML = `<div style="background:#1e293b;border:1px solid #334155;border-radius:0.75rem;padding:1.5rem 2.25rem;display:flex;align-items:center;gap:1rem;box-shadow:0 25px 50px rgba(0,0,0,0.6);"><div style="width:2rem;height:2rem;border:3px solid #334155;border-top-color:#2E86DE;border-radius:50%;animation:lims-spin 0.75s linear infinite;"></div><span style="color:#f1f5f9;font-weight:500;font-size:0.95rem;">Loading...</span></div>`;
        const st = document.createElement('style');
        st.textContent = '@keyframes lims-spin{to{transform:rotate(360deg)}} @keyframes lims-pulse{0%,100%{opacity:1}50%{opacity:.5}}';
        document.head.appendChild(st);
        document.body.appendChild(overlay);
    }
    overlay.style.display = show ? 'flex' : 'none';
}

/* ─── Date Formatting ───────────────────────────────────────────────── */
function formatDate(d) {
    if (!d) return 'N/A';
    try { return new Date(d).toLocaleDateString('en-US',{year:'numeric',month:'short',day:'numeric'}); }
    catch(e){ return d; }
}
function formatDateTime(d) {
    if (!d) return 'N/A';
    try { return new Date(d).toLocaleString('en-US',{year:'numeric',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}); }
    catch(e){ return d; }
}

/* ─── Status Badges ─────────────────────────────────────────────────── */
function getStatusBadge(status) {
    const map = {
        pending:     ['#f59e0b','#431407','Pending'],
        testing:     ['#3b82f6','#1e3a8a','Testing'],
        completed:   ['#22c55e','#052e16','Completed'],
        approved:    ['#a855f7','#2e1065','Approved'],
        rejected:    ['#ef4444','#450a0a','Rejected'],
        in_progress: ['#3b82f6','#1e3a8a','In Progress'],
        active:      ['#22c55e','#052e16','Active'],
        inactive:    ['#6b7280','#1f2937','Inactive'],
        maintenance: ['#f59e0b','#431407','Maintenance'],
        urgent:      ['#f59e0b','#431407','Urgent'],
        stat:        ['#ef4444','#450a0a','STAT'],
        normal:      ['#6b7280','#1f2937','Normal'],
    };
    const key = (status||'').toLowerCase().replace(/\s+/g,'_');
    const [fg,bg,label] = map[key] || ['#6b7280','#1f2937',status||'—'];
    return `<span style="display:inline-flex;align-items:center;padding:0.2rem 0.65rem;font-size:0.72rem;font-weight:600;border-radius:9999px;background:${bg};color:${fg};border:1px solid ${fg}55;white-space:nowrap;">${label}</span>`;
}
function getResultStatusBadge(status) {
    const map = {
        normal:   ['#22c55e','#052e16','Normal',''],
        abnormal: ['#f59e0b','#431407','Abnormal',''],
        critical: ['#ef4444','#450a0a','CRITICAL','animation:lims-pulse 1.2s ease infinite;'],
    };
    const key = (status||'').toLowerCase();
    const [fg,bg,label,anim] = map[key] || ['#6b7280','#1f2937',status||'—',''];
    return `<span style="display:inline-flex;align-items:center;padding:0.2rem 0.65rem;font-size:0.72rem;font-weight:700;border-radius:9999px;background:${bg};color:${fg};border:1px solid ${fg}55;${anim}">${label}</span>`;
}

/* ─── Auth Helpers ──────────────────────────────────────────────────── */
function checkAuth() {
    if (!localStorage.getItem('enigma_token')) { window.location.href = 'index.html'; return false; }
    return true;
}
function getCurrentUser() {
    try { const u = localStorage.getItem('enigma_user'); return u ? JSON.parse(u) : null; } catch(e){ return null; }
}
function setCurrentUser(user) {
    try { localStorage.setItem('enigma_user', JSON.stringify(user)); } catch(e){}
}

/* ─── Sidebar Initialisation ────────────────────────────────────────── */
function initSidebar(activePage) {
    const user = getCurrentUser();
    if (user) {
        const avEl    = document.getElementById('user-avatar');
        const nameEl  = document.getElementById('user-name');
        const roleEl  = document.getElementById('user-role');
        if (avEl)   avEl.textContent   = (user.full_name || user.username || 'U').charAt(0).toUpperCase();
        if (nameEl) nameEl.textContent = user.full_name || user.username || 'User';
        if (roleEl) {
            const r = user.role || 'user';
            roleEl.textContent = r.charAt(0).toUpperCase() + r.slice(1);
        }
        if (user.role === 'admin') {
            const an = document.getElementById('admin-nav');
            if (an) an.style.display = 'block';
        }
    }
    if (activePage) {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === activePage + '.html') item.classList.add('active');
        });
    }
}

/* ─── Logout ────────────────────────────────────────────────────────── */
function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('enigma_token');
        localStorage.removeItem('enigma_user');
        window.location.href = 'index.html';
    }
}

/* ─── Empty State ───────────────────────────────────────────────────── */
function renderEmptyState(colSpan, message = 'No records found', icon = 'fa-inbox') {
    return `<tr><td colspan="${colSpan}" style="padding:3.5rem 1rem;text-align:center;"><div style="color:#475569;"><i class="fas ${icon}" style="font-size:2.5rem;opacity:0.4;display:block;margin-bottom:0.75rem;"></i><p style="font-size:0.95rem;font-weight:500;color:#64748b;">${message}</p><p style="font-size:0.8rem;margin-top:0.25rem;color:#475569;">Try adjusting your search or filters</p></div></td></tr>`;
}

/* ─── Modal Helpers ─────────────────────────────────────────────────── */
function openModal(id) {
    const m = document.getElementById(id);
    if (m) { m.style.display = 'flex'; document.body.style.overflow = 'hidden'; }
}
function closeModal(id) {
    const m = document.getElementById(id);
    if (m) { m.style.display = 'none'; document.body.style.overflow = ''; }
}

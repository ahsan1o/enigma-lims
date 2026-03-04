const Auth = {
  getToken() { return localStorage.getItem('enigma_token'); },
  getUser() {
    const u = localStorage.getItem('enigma_user');
    return u ? JSON.parse(u) : null;
  },
  setSession(token, user) {
    localStorage.setItem('enigma_token', token);
    localStorage.setItem('enigma_user', JSON.stringify(user));
  },
  clearSession() {
    localStorage.removeItem('enigma_token');
    localStorage.removeItem('enigma_user');
  },
  isLoggedIn() { return !!this.getToken(); },
  requireAuth() {
    if (!this.isLoggedIn()) {
      window.location.href = 'index.html';
      return false;
    }
    return true;
  },
  requireAdmin() {
    if (!this.requireAuth()) return false;
    const user = this.getUser();
    if (!user || user.role !== 'admin') {
      window.location.href = 'dashboard.html';
      return false;
    }
    return true;
  },
  /* setupNav — call once per page after requireAuth.
     • Fills userName / userRole / userAvatar in the sidebar footer.
     • Hides every element with [data-admin-only] for non-admin users.
     • Applies a friendly role label in the sidebar. */
  setupNav() {
    const user = this.getUser();
    if (!user) return;
    const $ = id => document.getElementById(id);
    if ($('userName'))  $('userName').textContent  = user.full_name || user.username;
    if ($('userAvatar')) $('userAvatar').textContent = (user.full_name || user.username || 'A').charAt(0).toUpperCase();
    if ($('userRole')) {
      const labels = { admin: 'Super Admin', technician: 'Lab Technician', supervisor: 'Supervisor', doctor: 'Doctor' };
      $('userRole').textContent = labels[user.role] || (user.role || '').charAt(0).toUpperCase() + (user.role || '').slice(1);
    }
    if (user.role !== 'admin') {
      document.querySelectorAll('[data-admin-only]').forEach(el => { el.style.display = 'none'; });
    }
  },
  logout() {
    this.clearSession();
    window.location.href = 'index.html';
  }
};

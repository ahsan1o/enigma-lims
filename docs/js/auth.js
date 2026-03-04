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
  logout() {
    this.clearSession();
    window.location.href = 'index.html';
  }
};

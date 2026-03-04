/**
 * Enigma LIMS — Command Palette (Ctrl+K / Cmd+K)
 * Searches patients and samples in real-time, navigate with keyboard.
 */
(function() {
  const CSS = `
    #cmdPalette { display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.65); backdrop-filter:blur(6px); align-items:flex-start; justify-content:center; padding-top:10vh; }
    #cmdPalette.open { display:flex; }
    #cmdBox { background:#fff; border-radius:16px; width:100%; max-width:580px; border:1px solid #e2e8f0; box-shadow:0 25px 50px -12px rgba(0,0,0,0.35); overflow:hidden; }
    #cmdInput { width:100%; border:none; outline:none; font-size:15px; padding:16px 18px; background:transparent; color:#1e293b; font-family:inherit; }
    #cmdInput::placeholder { color:#94a3b8; }
    #cmdDivider { height:1px; background:#f1f5f9; }
    #cmdResults { max-height:360px; overflow-y:auto; }
    #cmdResults::-webkit-scrollbar { width:4px; }
    #cmdResults::-webkit-scrollbar-thumb { background:#cbd5e1; border-radius:2px; }
    .cmd-item { display:flex; align-items:center; gap:12px; padding:10px 18px; cursor:pointer; transition:background .1s; border-bottom:1px solid #f8fafc; }
    .cmd-item:hover, .cmd-item.selected { background:#eff6ff; }
    .cmd-item .cmd-icon { width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:13px; }
    .cmd-item .cmd-main { font-size:13px; font-weight:600; color:#1e293b; line-height:1.3; }
    .cmd-item .cmd-sub { font-size:11px; color:#94a3b8; margin-top:1px; }
    .cmd-item .cmd-badge { margin-left:auto; font-size:10px; font-weight:700; padding:2px 8px; border-radius:999px; flex-shrink:0; }
    #cmdFooter { padding:8px 18px; background:#f8fafc; border-top:1px solid #f1f5f9; display:flex; gap:16px; }
    #cmdFooter span { font-size:11px; color:#94a3b8; display:flex; align-items:center; gap:4px; }
    #cmdFooter kbd { background:#e2e8f0; border-radius:4px; padding:1px 5px; font-size:10px; color:#475569; font-family:monospace; }
    #cmdEmpty { padding:32px; text-align:center; color:#94a3b8; font-size:13px; }
    #cmdLoading { padding:24px; text-align:center; color:#94a3b8; font-size:13px; }
  `;

  function injectStyles() {
    const s = document.createElement('style');
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function buildHTML() {
    const div = document.createElement('div');
    div.id = 'cmdPalette';
    div.innerHTML = `
      <div id="cmdBox" role="dialog" aria-modal="true" aria-label="Command palette">
        <div style="display:flex;align-items:center;padding:0 18px;">
          <i class="fas fa-search" style="color:#94a3b8;font-size:14px;flex-shrink:0;"></i>
          <input id="cmdInput" type="text" placeholder="Search patients, samples… (type to start)" autocomplete="off" spellcheck="false">
          <kbd onclick="closePalette()" style="cursor:pointer;background:#f1f5f9;border:1px solid #e2e8f0;border-radius:6px;padding:2px 7px;font-size:11px;color:#64748b;font-family:monospace;flex-shrink:0;">ESC</kbd>
        </div>
        <div id="cmdDivider"></div>
        <div id="cmdResults">
          <div id="cmdEmpty" style="display:none;">No results found</div>
          <div id="cmdLoading" style="display:none;"><i class="fas fa-spinner fa-spin" style="margin-right:6px;"></i>Searching…</div>
        </div>
        <div id="cmdFooter">
          <span><kbd>↑</kbd><kbd>↓</kbd> Navigate</span>
          <span><kbd>↵</kbd> Open</span>
          <span><kbd>ESC</kbd> Close</span>
        </div>
      </div>`;
    document.body.appendChild(div);
    div.addEventListener('click', e => { if (e.target === div) closePalette(); });
  }

  let selectedIdx = -1;
  let currentResults = [];
  let debounceTimer = null;

  function openPalette() {
    const el = document.getElementById('cmdPalette');
    if (!el) return;
    el.classList.add('open');
    document.getElementById('cmdInput').value = '';
    document.getElementById('cmdResults').innerHTML = '';
    document.getElementById('cmdEmpty').style.display = 'none';
    document.getElementById('cmdLoading').style.display = 'none';
    selectedIdx = -1;
    currentResults = [];
    setTimeout(() => document.getElementById('cmdInput').focus(), 50);
  }

  function closePalette() {
    const el = document.getElementById('cmdPalette');
    if (el) el.classList.remove('open');
  }

  window.closePalette = closePalette;

  function badge(text, fg, bg) {
    return `<span class="cmd-badge" style="background:${bg};color:${fg};">${text}</span>`;
  }

  function renderResults(patients, samples) {
    const container = document.getElementById('cmdResults');
    currentResults = [];

    let html = '';

    if (patients.length) {
      html += `<div style="padding:6px 18px 4px;font-size:10px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;background:#f8fafc;border-bottom:1px solid #f1f5f9;">Patients</div>`;
      patients.slice(0, 5).forEach(p => {
        currentResults.push({ type: 'patient', id: p.id, href: 'patients.html' });
        html += `<div class="cmd-item" data-idx="${currentResults.length-1}" onclick="navigatePalette(${currentResults.length-1})">
          <div class="cmd-icon" style="background:#eff6ff;color:#3b82f6;"><i class="fas fa-user"></i></div>
          <div>
            <div class="cmd-main">${p.full_name||p.name||'—'}</div>
            <div class="cmd-sub">${p.age ? p.age+'y' : ''} ${p.gender||''} · ${p.phone||'No phone'}</div>
          </div>
          ${badge('Patient','#3b82f6','#eff6ff')}
        </div>`;
      });
    }

    if (samples.length) {
      html += `<div style="padding:6px 18px 4px;font-size:10px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;background:#f8fafc;border-bottom:1px solid #f1f5f9;border-top:1px solid #f1f5f9;">Samples</div>`;
      samples.slice(0, 5).forEach(s => {
        currentResults.push({ type: 'sample', id: s.id, href: 'samples.html' });
        const statusColors = { pending:'#f59e0b', testing:'#3b82f6', completed:'#22c55e', approved:'#a855f7', rejected:'#ef4444' };
        const sc = statusColors[(s.status||'pending').toLowerCase()] || '#64748b';
        html += `<div class="cmd-item" data-idx="${currentResults.length-1}" onclick="navigatePalette(${currentResults.length-1})">
          <div class="cmd-icon" style="background:#f0fdf4;color:#22c55e;"><i class="fas fa-vial"></i></div>
          <div>
            <div class="cmd-main" style="font-family:monospace;">${s.sample_id||s.id||'—'}</div>
            <div class="cmd-sub">${s.patient_name||'—'} · ${s.sample_type||'—'}</div>
          </div>
          ${badge((s.status||'').charAt(0).toUpperCase()+(s.status||'').slice(1), sc, sc+'18')}
        </div>`;
      });
    }

    if (!patients.length && !samples.length) {
      container.innerHTML = '<div id="cmdEmpty">No results found for your search</div>';
      return;
    }

    container.innerHTML = html;
    selectedIdx = -1;
    updateSelection();
  }

  window.navigatePalette = function(idx) {
    const item = currentResults[idx];
    if (!item) return;
    closePalette();
    window.location.href = item.href;
  };

  function updateSelection() {
    document.querySelectorAll('.cmd-item').forEach((el, i) => {
      el.classList.toggle('selected', i === selectedIdx);
      if (i === selectedIdx) el.scrollIntoView({ block: 'nearest' });
    });
  }

  async function doSearch(query) {
    if (!query || query.length < 2) {
      document.getElementById('cmdResults').innerHTML = '';
      document.getElementById('cmdEmpty').style.display = 'none';
      document.getElementById('cmdLoading').style.display = 'none';
      currentResults = [];
      return;
    }
    document.getElementById('cmdLoading').style.display = 'block';
    try {
      const [pData, sData] = await Promise.all([
        (typeof API !== 'undefined' ? API.getPatients(query).catch(()=>null) : null),
        (typeof API !== 'undefined' ? API.getSamples('', query).catch(()=>null) : null)
      ]);
      document.getElementById('cmdLoading').style.display = 'none';
      const patients = Array.isArray(pData) ? pData : (pData?.items||[]);
      const samples  = Array.isArray(sData) ? sData : (sData?.items||[]);
      renderResults(patients, samples);
    } catch(e) {
      document.getElementById('cmdLoading').style.display = 'none';
      document.getElementById('cmdResults').innerHTML = '<div id="cmdEmpty">Search error — is the server running?</div>';
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    injectStyles();
    buildHTML();

    document.getElementById('cmdInput').addEventListener('input', function() {
      clearTimeout(debounceTimer);
      const q = this.value.trim();
      debounceTimer = setTimeout(() => doSearch(q), 280);
    });

    document.addEventListener('keydown', e => {
      const palette = document.getElementById('cmdPalette');

      // Open: Ctrl+K or Cmd+K
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (palette && palette.classList.contains('open')) { closePalette(); } else { openPalette(); }
        return;
      }

      if (!palette || !palette.classList.contains('open')) return;

      if (e.key === 'Escape') { e.preventDefault(); closePalette(); return; }

      const items = document.querySelectorAll('.cmd-item');
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIdx = Math.min(selectedIdx + 1, items.length - 1);
        updateSelection();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIdx = Math.max(selectedIdx - 1, 0);
        updateSelection();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedIdx >= 0 && currentResults[selectedIdx]) {
          navigatePalette(selectedIdx);
        }
      }
    });
  });
})();

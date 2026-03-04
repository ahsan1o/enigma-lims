/**
 * Enigma LIMS — Help & Onboarding System
 * Provides: per-page help modal + first-visit tour + role-aware workflow guides + field tooltips
 */

// ─── Per-Page Help Content ──────────────────────────────────────────────────────
const HELP_CONTENT = {
  dashboard: {
    icon: 'fa-home',
    color: 'blue',
    title: 'Dashboard',
    description: 'Your lab at a glance. See live stats for patients, samples, pending results, and today\'s completed tests.',
    descriptionByRole: {
      technician: 'Your daily work hub. See how many samples are waiting, how many results need entry, and follow the 5-step workflow for every patient visit: Register → Sample → Order → Results → Report.',
      admin: 'Complete system overview. Monitor all lab activity, sample status, result distributions. Use the Admin section in the sidebar to configure Tests & Prices, Billing, Users, and Instruments.'
    },
    actions: [
      'Check pending results count — work through those first',
      'Click "New Patient" to register a brand-new patient and start their visit in one flow',
      'Click "Existing Patient" to start a visit for a patient already in the system',
      'Use the 5-step workflow guide to navigate any patient visit manually',
      'Click Refresh to update all statistics',
      'Charts show sample and result status distributions'
    ],
    actionsAdmin: [
      'Monitor lab-wide statistics and trends in real time',
      'Use the Admin section (sidebar) for system configuration',
      'Set up Tests & Prices before technicians can order them',
      'Create user accounts for lab staff in Users'
    ],
    linked: [
      { label: 'Patients', href: 'patients.html', icon: 'fa-users' },
      { label: 'Samples', href: 'samples.html', icon: 'fa-vial' },
      { label: 'Results', href: 'results.html', icon: 'fa-chart-bar' }
    ],
    next: null
  },

  patients: {
    icon: 'fa-users',
    color: 'blue',
    title: 'Patients',
    description: 'The patient registry. Every lab visit must be linked to a patient record. Register a patient once — they can have unlimited future visits, samples, and test orders.',
    actions: [
      'Click "Add Patient" to register a new patient',
      'Required fields: Name, Age, Gender — phone is optional but useful',
      'Search by name or phone number using the search box',
      'Click "History" to see all past visits and results for a patient',
      'A patient is registered only once — repeat visits reuse the same record'
    ],
    linked: [
      { label: 'Samples', href: 'samples.html', icon: 'fa-vial', note: 'Next step: collect a sample' },
      { label: 'Reports', href: 'reports.html', icon: 'fa-file-medical', note: 'Reports show patient details' }
    ],
    next: { label: 'Register a Sample', href: 'samples.html', icon: 'fa-vial' }
  },

  samples: {
    icon: 'fa-vial',
    color: 'green',
    title: 'Samples',
    description: 'A sample is the physical specimen collected from a patient (blood, urine, stool, etc.). Each sample gets a unique barcode ID and tracks its progress through the lab.',
    actions: [
      'Click "Register Sample" to log a newly collected specimen',
      'Select the patient this sample belongs to',
      'Choose sample type: Blood, Urine, Stool, Swab, etc.',
      'Print and stick the barcode label on the physical tube',
      'Status flow: Pending → Testing → Completed → Approved'
    ],
    linked: [
      { label: 'Patients', href: 'patients.html', icon: 'fa-users', note: 'Patient must be registered first' },
      { label: 'Orders', href: 'orders.html', icon: 'fa-clipboard-list', note: 'Next: order tests on this sample' }
    ],
    next: { label: 'Create a Test Order', href: 'orders.html', icon: 'fa-clipboard-list' }
  },

  tests: {
    icon: 'fa-microscope',
    color: 'cyan',
    title: 'Tests & Prices',
    description: 'ADMIN ONLY — The test catalog. Define all laboratory tests your lab offers: test code, name, reference range (what is normal), unit of measurement, and price (PKR). Set this up once.',
    actions: [
      'Click "Add Test" to add a new test to the catalog',
      'Test Code: short identifier like CBC, LFT, RFT, BS — appears on reports',
      'Set Normal Range (e.g. 70–110 for blood glucose) for automatic result flagging',
      'Set Unit (mg/dL, g/L, %, mmol/L, etc.)',
      'Set Price in PKR — this appears automatically on patient reports and bill summary',
      'Tests here become available options when technicians create orders'
    ],
    linked: [
      { label: 'Test Panels', href: 'panels.html', icon: 'fa-layer-group', note: 'Bundle tests into quick-order groups' },
      { label: 'Orders', href: 'orders.html', icon: 'fa-clipboard-list', note: 'Tests are selected when ordering' }
    ],
    next: null
  },

  orders: {
    icon: 'fa-clipboard-list',
    color: 'amber',
    title: 'Test Orders',
    description: 'A test order links a sample to the specific test that needs to be run. Select the sample and the test — the system shows the price and tracks everything through to the report.',
    actions: [
      'Click "New Order" to create a test order for a sample',
      'Scan the barcode on the sample tube OR select from the dropdown',
      'Select the test to run — the price is shown next to each option',
      'Select the referring doctor (recommended — appears on the report)',
      'Set priority: Normal / Urgent / STAT (immediate)',
      'Create multiple orders for the same sample (one per test)'
    ],
    linked: [
      { label: 'Samples', href: 'samples.html', icon: 'fa-vial', note: 'Each order is linked to a sample' },
      { label: 'Results', href: 'results.html', icon: 'fa-chart-bar', note: 'Next: enter the result values' }
    ],
    next: { label: 'Enter Results', href: 'results.html', icon: 'fa-chart-bar' }
  },

  results: {
    icon: 'fa-chart-bar',
    color: 'purple',
    title: 'Results',
    description: 'Enter the measured test values here. The system automatically compares each value to the reference range and flags it as Normal, Abnormal, or Critical.',
    actions: [
      'Scan the sample barcode (green bar at top) to jump directly to entry',
      'Find the order and click "Enter Result"',
      'Type the measured value — Normal / Abnormal / Critical is flagged automatically',
      'Critical results show a red alert banner at the top of the page',
      'Click "Approve" once the result is verified — only approved results appear on reports'
    ],
    linked: [
      { label: 'Orders', href: 'orders.html', icon: 'fa-clipboard-list', note: 'Results are entered for ordered tests' },
      { label: 'Reports', href: 'reports.html', icon: 'fa-file-medical', note: 'Approved results appear on reports' }
    ],
    next: { label: 'Print Report', href: 'reports.html', icon: 'fa-file-medical' }
  },

  reports: {
    icon: 'fa-file-medical',
    color: 'rose',
    title: 'Reports',
    description: 'The final patient-facing document. Shows all test results, reference ranges, status flags (Normal/Abnormal/Critical), and the total bill. Print and hand to the patient.',
    actions: [
      'Find the patient or sample ID in the list',
      'Click "View" to open the full report',
      'The report shows test results, reference ranges, and status flags',
      'The Bill Summary at the bottom shows each test price and the total amount',
      'Click "Print" to print — hand to the patient or referring doctor',
      'Reports appear once at least one result is approved'
    ],
    linked: [
      { label: 'Results', href: 'results.html', icon: 'fa-chart-bar', note: 'Results must be approved first' },
      { label: 'Patients', href: 'patients.html', icon: 'fa-users', note: 'Patient info appears on report' }
    ],
    next: null
  },

  instruments: {
    icon: 'fa-cogs',
    color: 'rose',
    title: 'Instruments',
    description: 'ADMIN ONLY — Lab equipment registry. Track analyzers, centrifuges, and other instruments including model numbers, serial numbers, calibration dates, and operational status.',
    actions: [
      'Click "Add Instrument" to register a piece of lab equipment',
      'Set calibration date and next service date for maintenance tracking',
      'Mark instruments as Active, Inactive, or Under Maintenance',
      'Link tests to instruments so results are traceable to a specific machine'
    ],
    linked: [],
    next: null
  },

  users: {
    icon: 'fa-user-shield',
    color: 'indigo',
    title: 'Users',
    description: 'ADMIN ONLY — Staff accounts and access control. Two roles: Super Admin (full access) and Lab Technician (core workflow only: Patients, Samples, Orders, Results, Reports).',
    actions: [
      'Click "Add User" to create a new staff account',
      'Role "Super Admin" — sees everything including Tests, Billing, Instruments, Users, Audit',
      'Role "Lab Technician" — sees only Patients, Samples, Orders, Results, Reports',
      'Default accounts: admin / admin123 (Super Admin) and tech / tech123 (Technician)',
      'Change default passwords immediately after first login',
      'Deactivate accounts without deleting — history is preserved'
    ],
    linked: [],
    next: null
  },

  billing: {
    icon: 'fa-receipt',
    color: 'green',
    title: 'Billing',
    description: 'ADMIN ONLY — Patient invoicing and payment collection. Note: test prices on reports are automatic from the Tests catalog. This module is for formal invoicing.',
    actions: [
      'Click "New Invoice" to create a formal bill for a patient visit',
      'Add line items for each service or test',
      'Click "Pay" to record a payment received',
      'Filter invoices by status: Unpaid, Partial, Paid',
      'Tip: Set test prices in Tests & Prices — they appear automatically on patient reports'
    ],
    linked: [
      { label: 'Patients', href: 'patients.html', icon: 'fa-users', note: 'Invoice is linked to a patient' },
      { label: 'Tests & Prices', href: 'tests.html', icon: 'fa-microscope', note: 'Set test prices for automatic billing' }
    ],
    next: null
  },

  panels: {
    icon: 'fa-layer-group',
    color: 'indigo',
    title: 'Test Panels',
    description: 'ADMIN ONLY — Predefined test bundles for quick ordering. A "Liver Function Tests" panel might include ALT, AST, ALP, Bilirubin — order all at once instead of one by one.',
    actions: [
      'Click "New Panel" to create a test bundle',
      'Give it a descriptive name (e.g. "Liver Function Tests", "Kidney Profile")',
      'Select all tests that belong in this panel',
      'Technicians can then order this panel in one step instead of ordering each test individually'
    ],
    linked: [
      { label: 'Tests & Prices', href: 'tests.html', icon: 'fa-microscope', note: 'Tests must be in catalog first' },
      { label: 'Orders', href: 'orders.html', icon: 'fa-clipboard-list', note: 'Order a full panel at once' }
    ],
    next: null
  },

  reagents: {
    icon: 'fa-flask-vial',
    color: 'amber',
    title: 'Reagents',
    description: 'ADMIN ONLY — Reagent and consumable inventory. Track stock levels, expiry dates, and get low-stock alerts when supplies run low.',
    actions: [
      'Click "Add Reagent" to register a reagent or consumable',
      'Set the minimum stock level to trigger a low-stock alert',
      'Update current stock count when new supplies arrive',
      'Check the alert banner at the top for items needing attention',
      'Link reagents to instruments for organized tracking'
    ],
    linked: [
      { label: 'Instruments', href: 'instruments.html', icon: 'fa-cogs', note: 'Link reagents to instruments' }
    ],
    next: null
  },

  audit: {
    icon: 'fa-history',
    color: 'indigo',
    title: 'Audit Log',
    description: 'ADMIN ONLY — Complete activity trail for compliance. Every significant action is automatically recorded: who did it, when, and what changed.',
    actions: [
      'Filter by entity type: patients, samples, results, tests, etc.',
      'Each entry shows: user, timestamp, action, and what changed',
      'Use for compliance reporting or investigating discrepancies',
      'Enable auto-refresh to monitor live activity'
    ],
    linked: [],
    next: null
  },
};

// ─── Tour Steps ────────────────────────────────────────────────────────────────
const TOUR_STEPS = [
  {
    icon: 'fa-flask',
    iconBg: 'bg-blue-600',
    step: null,
    title: 'Welcome to Enigma LIMS',
    body: 'This is your Laboratory Information Management System. The workflow is simple: <strong>Register Patient → Collect Sample → Order Tests → Enter Results → Print Report</strong>.',
    sub: '<strong>Two quick-start buttons are on the dashboard:</strong> <span style="color:#1d4ed8">New Patient</span> — for a first-time visitor. <span style="color:#1d4ed8">Existing Patient</span> — for a returning patient. Both guide you through the same 3-step wizard. There are two roles: Lab Technician (sees the 5-step core workflow) and Super Admin (sees everything).',
    link: null
  },
  {
    icon: 'fa-users',
    iconBg: 'bg-blue-500',
    step: 1,
    title: 'Step 1 — Register the Patient',
    body: 'Every lab visit starts with a patient. Use the <strong>New Patient</strong> button on the dashboard for first-time visitors, or <strong>Existing Patient</strong> for repeat patients. You can also go to <strong>Patients → Add Patient</strong> directly.',
    sub: 'Register a patient only once. They can return for future visits without re-registering — the system keeps their full test history. Use "Existing Patient" to find them by name or phone number.',
    link: { href: 'patients.html', label: 'Go to Patients →' }
  },
  {
    icon: 'fa-vial',
    iconBg: 'bg-green-500',
    step: 2,
    title: 'Step 2 — Receive the Sample',
    body: 'Go to <strong>Samples → Register Sample</strong>. Select the patient and the sample type (Blood, Urine, Stool, etc.). The system assigns a unique barcode ID automatically.',
    sub: 'Print the barcode label and stick it on the physical tube. Use the scanner field anywhere in the system to look up samples instantly.',
    link: { href: 'samples.html', label: 'Go to Samples →' }
  },
  {
    icon: 'fa-clipboard-list',
    iconBg: 'bg-amber-500',
    step: 3,
    title: 'Step 3 — Order the Tests',
    body: 'Go to <strong>Orders → New Order</strong>. Select the sample and the test to run. Each test shows its price (e.g. CBC — PKR 500). The price appears automatically on the final report.',
    sub: 'One sample can have multiple test orders — one per test. Prices are set by the admin in Tests & Prices.',
    link: { href: 'orders.html', label: 'Go to Orders →' }
  },
  {
    icon: 'fa-chart-bar',
    iconBg: 'bg-purple-500',
    step: 4,
    title: 'Step 4 — Enter the Results',
    body: 'Go to <strong>Results</strong>. Scan the barcode or search manually. Enter the measured value. The system flags Normal / Abnormal / Critical against the reference range automatically.',
    sub: 'Click Approve once results are verified. Only approved results appear on the patient report.',
    link: { href: 'results.html', label: 'Go to Results →' }
  },
  {
    icon: 'fa-file-medical',
    iconBg: 'bg-rose-500',
    step: 5,
    title: 'Step 5 — Print the Report',
    body: 'Go to <strong>Reports</strong>. Find the patient and click View. The report shows all results, reference ranges, and a <strong>Bill Summary</strong> with each test price and total amount in PKR.',
    sub: 'Print the report and hand it to the patient. That completes one full patient visit. The bill is right there on the report — no separate invoice needed.',
    link: { href: 'reports.html', label: 'Go to Reports →' }
  }
];

// ─── Color map ─────────────────────────────────────────────────────────────────
const COLOR_MAP = {
  blue:   { bg: 'bg-blue-50',   border: 'border-blue-200',   text: 'text-blue-700',   icon: 'bg-blue-100 text-blue-600',   btn: 'bg-blue-600 hover:bg-blue-700' },
  green:  { bg: 'bg-green-50',  border: 'border-green-200',  text: 'text-green-700',  icon: 'bg-green-100 text-green-600', btn: 'bg-green-600 hover:bg-green-700' },
  cyan:   { bg: 'bg-cyan-50',   border: 'border-cyan-200',   text: 'text-cyan-700',   icon: 'bg-cyan-100 text-cyan-600',   btn: 'bg-cyan-600 hover:bg-cyan-700' },
  amber:  { bg: 'bg-amber-50',  border: 'border-amber-200',  text: 'text-amber-700',  icon: 'bg-amber-100 text-amber-600', btn: 'bg-amber-600 hover:bg-amber-700' },
  purple: { bg: 'bg-purple-50', border: 'border-purple-200', text: 'text-purple-700', icon: 'bg-purple-100 text-purple-600',btn: 'bg-purple-600 hover:bg-purple-700' },
  rose:   { bg: 'bg-rose-50',   border: 'border-rose-200',   text: 'text-rose-700',   icon: 'bg-rose-100 text-rose-600',   btn: 'bg-rose-600 hover:bg-rose-700' },
  indigo: { bg: 'bg-indigo-50', border: 'border-indigo-200', text: 'text-indigo-700', icon: 'bg-indigo-100 text-indigo-600',btn: 'bg-indigo-600 hover:bg-indigo-700' }
};

// ─── Tooltip System ─────────────────────────────────────────────────────────────
(function initTooltips() {
  document.addEventListener('DOMContentLoaded', function() {
    const tip = document.createElement('div');
    tip.id = 'lims-tooltip';
    tip.style.cssText = 'position:fixed;z-index:9999;background:#1e293b;color:#f1f5f9;padding:.4rem .75rem;border-radius:.5rem;font-size:.72rem;line-height:1.4;max-width:230px;pointer-events:none;opacity:0;transition:opacity .15s;box-shadow:0 4px 12px rgba(0,0,0,.25);white-space:normal;';
    document.body.appendChild(tip);
    document.addEventListener('mouseover', function(e) {
      const el = e.target.closest('[data-tooltip]');
      if (!el) return;
      tip.textContent = el.dataset.tooltip;
      tip.style.opacity = '1';
    });
    document.addEventListener('mousemove', function(e) {
      if (tip.style.opacity === '0') return;
      const x = e.clientX + 12, y = e.clientY - 8;
      tip.style.left = Math.min(x, window.innerWidth - 240) + 'px';
      tip.style.top  = Math.max(y - 40, 4) + 'px';
    });
    document.addEventListener('mouseout', function(e) {
      if (e.target.closest('[data-tooltip]')) tip.style.opacity = '0';
    });
  });
})();

// ─── Help Modal ────────────────────────────────────────────────────────────────
const Help = {
  _modalEl: null,

  _ensureModal() {
    if (this._modalEl) return;
    const el = document.createElement('div');
    el.id = 'helpModal';
    el.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(0,0,0,0.45);backdrop-filter:blur(4px);z-index:999;align-items:center;justify-content:center;padding:1rem;';
    el.innerHTML = '<div id="helpModalInner" class="bg-white rounded-2xl w-full max-w-md border border-gray-200 shadow-2xl overflow-hidden"></div>';
    el.addEventListener('click', e => { if (e.target === el) Help.closeHelp(); });
    document.body.appendChild(el);
    this._modalEl = el;
  },

  openHelp(pageKey) {
    this._ensureModal();
    const c = HELP_CONTENT[pageKey];
    if (!c) return;
    const col = COLOR_MAP[c.color] || COLOR_MAP.blue;

    // Role-aware content
    const user = (typeof Auth !== 'undefined') ? Auth.getUser() : null;
    const role = user?.role || 'technician';
    const description = (c.descriptionByRole && c.descriptionByRole[role]) || c.description;
    const actions = (role === 'admin' && c.actionsAdmin) ? c.actionsAdmin : c.actions;
    const roleBadge = role === 'admin'
      ? '<span class="ml-1.5 text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded font-semibold">Admin</span>'
      : '<span class="ml-1.5 text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded font-semibold">Technician</span>';

    const linksHtml = c.linked.length
      ? c.linked.map(l => `
          <a href="${l.href}" class="flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
            <i class="fas ${l.icon} text-gray-400 w-4 text-center text-xs"></i>
            <div>
              <div class="text-xs font-semibold text-gray-700">${l.label}</div>
              ${l.note ? `<div class="text-xs text-gray-400">${l.note}</div>` : ''}
            </div>
            <i class="fas fa-arrow-right text-gray-300 text-xs ml-auto"></i>
          </a>`).join('')
      : '<p class="text-xs text-gray-400">Standalone module</p>';

    const nextHtml = c.next
      ? `<div class="px-5 pb-5"><a href="${c.next.href}" class="w-full ${col.btn} text-white px-4 py-2.5 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition-colors">
           <i class="fas ${c.next.icon}"></i> Next: ${c.next.label} <i class="fas fa-arrow-right text-xs"></i>
         </a></div>`
      : '';

    document.getElementById('helpModalInner').innerHTML = `
      <div class="${col.bg} ${col.border} border-b px-5 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl ${col.icon} flex items-center justify-center">
            <i class="fas ${c.icon} text-sm"></i>
          </div>
          <div>
            <div class="text-xs font-semibold ${col.text} uppercase tracking-wider flex items-center">Help — ${c.title}${roleBadge}</div>
            <div class="text-gray-500 text-xs">How this page works</div>
          </div>
        </div>
        <button onclick="Help.closeHelp()" class="text-gray-400 hover:text-gray-600 p-1 transition-colors"><i class="fas fa-times"></i></button>
      </div>
      <div class="px-5 py-4 space-y-4 max-h-[60vh] overflow-y-auto">
        <p class="text-gray-700 text-sm leading-relaxed">${description}</p>
        <div>
          <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">What to do here</p>
          <ul class="space-y-1.5">
            ${actions.map(a => `<li class="flex items-start gap-2 text-xs text-gray-600"><i class="fas fa-check text-green-500 mt-0.5 flex-shrink-0"></i>${a}</li>`).join('')}
          </ul>
        </div>
        ${c.linked.length ? `<div>
          <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Linked to</p>
          <div class="grid grid-cols-1 gap-2">${linksHtml}</div>
        </div>` : ''}
      </div>
      ${nextHtml}
    `;

    this._modalEl.style.display = 'flex';
  },

  closeHelp() {
    if (this._modalEl) this._modalEl.style.display = 'none';
  },

  init(pageKey) {
    document.addEventListener('DOMContentLoaded', () => {
      const header = document.querySelector('.sticky.top-0');
      if (!header) return;
      const rightSlot = header.querySelector('.flex.items-center.gap-3, .flex.items-center.gap-2, button[onclick]')?.parentElement || header.lastElementChild;
      if (!rightSlot) return;

      const btn = document.createElement('button');
      btn.title = 'Help — how this page works';
      btn.className = 'w-8 h-8 rounded-full border border-gray-300 bg-white hover:bg-blue-50 hover:border-blue-400 text-gray-500 hover:text-blue-600 flex items-center justify-center transition-colors text-sm font-bold flex-shrink-0';
      btn.innerHTML = '?';
      btn.onclick = () => Help.openHelp(pageKey);
      rightSlot.appendChild(btn);
    });
  }
};

// ─── Onboarding Tour ───────────────────────────────────────────────────────────
(function() {
  const TECH_KEY  = 'enigma_tour_done';
  const ADMIN_KEY = 'enigma_admin_tour_done';

  const ADMIN_TOUR_STEPS = [
    {
      icon: 'fa-shield-alt', iconBg: 'bg-blue-700', step: null,
      title: 'Welcome, Super Admin',
      body: 'You have full access to Enigma LIMS. Before your technicians can start working, you need to set up a few things. This tour walks you through the <strong>admin setup checklist</strong>.',
      sub: 'Your sidebar has a core section (visible to all staff) and an <strong>Admin section</strong> below a divider — only you can see those.',
      link: null
    },
    {
      icon: 'fa-microscope', iconBg: 'bg-cyan-600', step: 1,
      title: 'Step 1 — Add Tests & Prices',
      body: 'Go to <strong>Admin → Tests & Prices</strong>. Add every test your lab offers (e.g. CBC, Blood Sugar, Urine R/E). Set the price for each test.',
      sub: 'Prices flow automatically to Orders and appear on patient Reports in the Bill Summary. Technicians cannot add or edit tests.',
      link: { href: 'tests.html', label: 'Go to Tests & Prices →' }
    },
    {
      icon: 'fa-layer-group', iconBg: 'bg-indigo-600', step: 2,
      title: 'Step 2 — Create Test Panels (Optional)',
      body: 'Go to <strong>Admin → Test Panels</strong>. Bundle related tests into a panel (e.g. "Liver Function Tests" = ALT + AST + ALP + Bilirubin).',
      sub: 'Technicians can then order an entire panel in one click instead of ordering each test individually. Skip this if you don\'t need bundles.',
      link: { href: 'panels.html', label: 'Go to Test Panels →' }
    },
    {
      icon: 'fa-user-shield', iconBg: 'bg-violet-600', step: 3,
      title: 'Step 3 — Create Staff Accounts',
      body: 'Go to <strong>Admin → Users</strong>. Create a named account for each lab technician. Set their role to <em>Technician</em>. They will only see the core 5-step workflow.',
      sub: 'The default <code>tech / tech123</code> account is a placeholder — create real named accounts and deactivate or delete the defaults.',
      link: { href: 'users.html', label: 'Go to Users →' }
    },
    {
      icon: 'fa-cogs', iconBg: 'bg-gray-600', step: 4,
      title: 'Step 4 — Register Instruments (Optional)',
      body: 'Go to <strong>Admin → Instruments</strong>. Register your lab equipment (analyzers, centrifuges, etc.) with serial numbers, calibration dates, and maintenance schedules.',
      sub: 'Instruments can be linked to tests and reagents for full traceability. Skip for now if you just need to get started.',
      link: { href: 'instruments.html', label: 'Go to Instruments →' }
    },
    {
      icon: 'fa-check-circle', iconBg: 'bg-green-600', step: null,
      title: 'Setup Complete — You\'re Ready',
      body: 'Your lab is configured. Technicians can now log in and follow the 5-step patient workflow: <strong>Patient → Sample → Order → Results → Report</strong>.',
      sub: 'Use the Audit Log to review all activity. Use Billing for financial reports. The ? button on every page explains what it does and what comes next.',
      link: null
    }
  ];

  let currentStep = 0;
  let activeSteps = [];
  let tourEl = null;

  function buildTour(steps) {
    activeSteps = steps;
    const el = document.createElement('div');
    el.id = 'tourOverlay';
    el.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.75);backdrop-filter:blur(6px);z-index:1000;display:flex;align-items:center;justify-content:center;padding:1rem;';
    document.body.appendChild(el);
    tourEl = el;
    renderStep(0);
  }

  function renderStep(step) {
    const s = activeSteps[step];
    const total = activeSteps.length;
    const isLast = step === total - 1;

    const dots = activeSteps.map((_, i) =>
      `<span class="w-2 h-2 rounded-full transition-all ${i === step ? 'bg-blue-500 scale-125' : 'bg-gray-300'}"></span>`
    ).join('');

    const linkBtn = s.link
      ? `<a href="${s.link.href}" class="text-xs text-blue-600 hover:text-blue-700 underline underline-offset-2">${s.link.label}</a>`
      : '';

    const stepLabel = s.step
      ? `<div class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-0.5">Step ${s.step} of ${total - 2}</div>`
      : `<div class="text-xs font-bold text-blue-500 uppercase tracking-widest mb-0.5">${step === 0 ? 'Welcome' : 'Done'}</div>`;

    tourEl.innerHTML = `
      <div class="bg-white rounded-2xl w-full max-w-sm shadow-2xl border border-gray-200 overflow-hidden">
        <div class="relative">
          <div class="h-1.5 bg-gray-100">
            <div class="h-full bg-blue-500 transition-all duration-500 rounded-full" style="width:${((step + 1) / total * 100).toFixed(0)}%"></div>
          </div>
          <button onclick="Tour.skip()" class="absolute top-3 right-4 text-gray-400 hover:text-gray-600 text-xs transition-colors">Skip tour</button>
        </div>
        <div class="p-6">
          <div class="flex items-center gap-4 mb-4">
            <div class="w-14 h-14 rounded-2xl ${s.iconBg} flex items-center justify-center flex-shrink-0 shadow-sm">
              <i class="fas ${s.icon} text-white text-2xl"></i>
            </div>
            <div>
              ${stepLabel}
              <h2 class="text-gray-900 font-bold text-base leading-tight">${s.title}</h2>
            </div>
          </div>
          <p class="text-gray-600 text-sm leading-relaxed mb-2">${s.body}</p>
          <p class="text-gray-400 text-xs leading-relaxed mb-4">${s.sub}</p>
          ${linkBtn ? `<div class="mb-4">${linkBtn}</div>` : ''}
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5">${dots}</div>
            <div class="flex items-center gap-2">
              ${step > 0 ? `<button onclick="Tour.prev()" class="px-3 py-2 text-sm text-gray-500 hover:text-gray-700 transition-colors">← Back</button>` : ''}
              <button onclick="${isLast ? 'Tour.done()' : 'Tour.next()'}" class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl text-sm font-semibold transition-colors">
                ${isLast ? 'Start Using LIMS' : 'Next →'}
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  function getStorageKey() {
    const user = (typeof Auth !== 'undefined') ? Auth.getUser() : null;
    return (user && user.role === 'admin') ? ADMIN_KEY : TECH_KEY;
  }

  window.Tour = {
    next() { currentStep = Math.min(currentStep + 1, activeSteps.length - 1); renderStep(currentStep); },
    prev() { currentStep = Math.max(currentStep - 1, 0); renderStep(currentStep); },
    skip() { localStorage.setItem(getStorageKey(), '1'); tourEl?.remove(); tourEl = null; },
    done() { localStorage.setItem(getStorageKey(), '1'); tourEl?.remove(); tourEl = null; }
  };

  Help.startTour = function() {
    document.addEventListener('DOMContentLoaded', () => {
      const user = (typeof Auth !== 'undefined') ? Auth.getUser() : null;
      const isAdmin = user && user.role === 'admin';
      const key = isAdmin ? ADMIN_KEY : TECH_KEY;
      if (localStorage.getItem(key)) return;
      setTimeout(() => buildTour(isAdmin ? ADMIN_TOUR_STEPS : TOUR_STEPS), 600);
    });
  };
})();


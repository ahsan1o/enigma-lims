/**
 * Enigma LIMS — Help & Onboarding System
 * Provides: per-page help modal + first-visit tour + workflow guide
 */

const HELP_CONTENT = {
  dashboard: {
    icon: 'fa-home',
    color: 'blue',
    title: 'Dashboard',
    description: 'Your lab at a glance. See live stats for patients, samples, pending results, and today\'s completed tests. Charts show the overall state of your lab workflow.',
    actions: [
      'Check how many samples are pending results today',
      'Monitor the sample and result status charts',
      'Click "Refresh" to get the latest data',
      'Use the Workflow Guide below to navigate to any step'
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
      'Enter name, age, gender — phone and address are optional',
      'Search by name or phone number using the search box',
      'Edit or delete existing patients from the table'
    ],
    linked: [
      { label: 'Samples', href: 'samples.html', icon: 'fa-vial', note: 'Samples are linked to patients' },
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
      'Click "Register Sample" to receive a new specimen',
      'Select the patient and sample type (blood, urine, etc.)',
      'Use the blue barcode scanner bar to instantly look up any sample',
      'Track status: Pending → Testing → Completed → Approved'
    ],
    linked: [
      { label: 'Patients', href: 'patients.html', icon: 'fa-users', note: 'Patient must exist first' },
      { label: 'Orders', href: 'orders.html', icon: 'fa-clipboard-list', note: 'Tests are ordered on a sample' }
    ],
    next: { label: 'Create an Order', href: 'orders.html', icon: 'fa-clipboard-list' }
  },

  tests: {
    icon: 'fa-microscope',
    color: 'cyan',
    title: 'Tests',
    description: 'The test catalog — all laboratory tests your lab offers. Each test has a name, reference range (what\'s normal), unit of measurement, and price. Set this up once.',
    actions: [
      'Click "Add Test" to add a new test to the catalog',
      'Set the normal range (e.g. 70–110 for blood glucose)',
      'Set the unit (mg/dL, g/L, %, etc.)',
      'Tests here are available for selection when creating orders'
    ],
    linked: [
      { label: 'Orders', href: 'orders.html', icon: 'fa-clipboard-list', note: 'Tests are selected when ordering' }
    ],
    next: null
  },

  orders: {
    icon: 'fa-clipboard-list',
    color: 'amber',
    title: 'Orders',
    description: 'A test order links a sample to the tests that need to be run. A doctor orders "CBC + LFT + Blood Sugar" for a patient\'s sample — that becomes one order with multiple tests.',
    actions: [
      'Click "New Order" to create a test order',
      'Select the sample (or scan its barcode)',
      'Pick one or more tests from the catalog',
      'The order status updates as results are entered'
    ],
    linked: [
      { label: 'Samples', href: 'samples.html', icon: 'fa-vial', note: 'Each order is for a sample' },
      { label: 'Tests', href: 'tests.html', icon: 'fa-microscope', note: 'Tests come from the catalog' },
      { label: 'Results', href: 'results.html', icon: 'fa-chart-bar', note: 'Results are entered for ordered tests' }
    ],
    next: { label: 'Enter Results', href: 'results.html', icon: 'fa-chart-bar' }
  },

  results: {
    icon: 'fa-chart-bar',
    color: 'purple',
    title: 'Results',
    description: 'Where lab technicians enter measured test values. The system automatically compares each value to the reference range and flags it as Normal, Abnormal, or Critical.',
    actions: [
      'Scan the barcode (green bar) to jump directly to result entry',
      'Select the test, enter the measured value',
      'The system flags Normal / Abnormal / Critical automatically',
      'Click "Approve" once results are verified — only approved results appear on reports'
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
    description: 'The final patient-facing document. Once results are approved, a report is generated showing all test values, reference ranges, and the lab\'s approval signature. Print and hand to the patient.',
    actions: [
      'Find the patient or sample in the list',
      'Click to open the full report',
      'Print the report using your browser\'s print function',
      'Reports are only available once results are approved'
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
    description: 'Lab equipment registry. Track analyzers, centrifuges, and other instruments — including model numbers, serial numbers, calibration dates, and operational status.',
    actions: [
      'Click "Add Instrument" to register a new piece of equipment',
      'Set the calibration date and next service date',
      'Mark instruments as Active or Out-of-Service',
      'Useful for audit trails and maintenance scheduling'
    ],
    linked: [],
    next: null
  },

  users: {
    icon: 'fa-user-shield',
    color: 'indigo',
    title: 'Users',
    description: 'Staff accounts and access control. Only administrators can manage users. Create accounts for lab technicians, doctors, and other staff with appropriate roles.',
    actions: [
      'Click "Add User" to create a new staff account',
      'Set role: Admin (full access) or Technician (lab operations)',
      'Activate or deactivate accounts without deleting them',
      'Change passwords as needed for security'
    ],
    linked: [],
    next: null
  },

  billing: {
    icon: 'fa-receipt',
    color: 'green',
    title: 'Billing',
    description: 'Patient invoicing and payment tracking. Generate bills for lab services, record payments, and track outstanding balances.',
    actions: [
      'Click "New Invoice" to create a bill for a patient visit',
      'Add line items (each test or service with amount)',
      'Click "Pay" on any invoice to record a payment',
      'Filter by status: Unpaid, Partial, Paid',
      'Export to CSV for accounting records'
    ],
    linked: [
      { label: 'Patients', href: 'patients.html', icon: 'fa-users', note: 'Invoice is linked to a patient' },
      { label: 'Samples', href: 'samples.html', icon: 'fa-vial', note: 'Optionally linked to a sample' }
    ],
    next: null
  },

  panels: {
    icon: 'fa-layer-group',
    color: 'indigo',
    title: 'Test Panels',
    description: 'Predefined test bundles for quick ordering. A CBC Panel might include Hemoglobin, WBC, Platelets and RBC — order all at once instead of individually.',
    actions: [
      'Click "New Panel" to create a test bundle',
      'Give it a name (e.g. "Liver Function Tests")',
      'Select all tests that belong in this panel',
      'Use panels in Orders for faster test selection'
    ],
    linked: [
      { label: 'Tests', href: 'tests.html', icon: 'fa-microscope', note: 'Tests come from the catalog' },
      { label: 'Orders', href: 'orders.html', icon: 'fa-clipboard-list', note: 'Order an entire panel at once' }
    ],
    next: null
  },

  reagents: {
    icon: 'fa-flask-vial',
    color: 'amber',
    title: 'Reagents',
    description: 'Reagent and consumable inventory management. Track stock levels, expiry dates, and get alerts when items run low.',
    actions: [
      'Click "Add Reagent" to register a new reagent or consumable',
      'Set minimum stock level to trigger low-stock alerts',
      'Update current stock when new supplies arrive',
      'Check the alert banner for items needing attention',
      'Link reagents to instruments for organized tracking'
    ],
    linked: [
      { label: 'Instruments', href: 'instruments.html', icon: 'fa-cogs', note: 'Reagents can be linked to instruments' }
    ],
    next: null
  },

  audit: {
    icon: 'fa-history',
    color: 'indigo',
    title: 'Audit Log',
    description: 'Complete activity trail for compliance and security. Every action in the system is recorded — who did what, when, and what changed.',
    actions: [
      'Filter by entity type (patients, samples, results, etc.)',
      'Search for specific actions',
      'View old and new values for any change',
      'Enable auto-refresh to monitor activity in real-time'
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
    body: 'This is your complete Laboratory Information Management System. Everything follows a simple 5-step workflow — from registering a patient to printing their report.',
    sub: 'Let\'s take a quick 60-second tour so you know exactly what to do.',
    link: null
  },
  {
    icon: 'fa-users',
    iconBg: 'bg-blue-500',
    step: 1,
    title: 'Step 1 — Register the Patient',
    body: 'Every lab visit starts with a patient record. Go to <strong>Patients</strong> and click "Add Patient". Enter their name, age, and gender.',
    sub: 'You only register a patient once. They can come back for future visits without re-registering.',
    link: { href: 'patients.html', label: 'Go to Patients' }
  },
  {
    icon: 'fa-vial',
    iconBg: 'bg-green-500',
    step: 2,
    title: 'Step 2 — Receive the Sample',
    body: 'Go to <strong>Samples</strong> and click "Register Sample". Select the patient and the type of sample (blood, urine, etc.). The system assigns a unique barcode.',
    sub: 'Attach the printed barcode label to the physical sample tube. The scanner on this page lets you look up samples instantly.',
    link: { href: 'samples.html', label: 'Go to Samples' }
  },
  {
    icon: 'fa-clipboard-list',
    iconBg: 'bg-amber-500',
    step: 3,
    title: 'Step 3 — Create an Order',
    body: 'Go to <strong>Orders</strong> and click "New Order". Select the sample and choose which tests to run — CBC, LFT, Blood Sugar, etc.',
    sub: 'One sample can have multiple tests. Tests are defined in the Tests catalog — set that up once for your lab.',
    link: { href: 'orders.html', label: 'Go to Orders' }
  },
  {
    icon: 'fa-chart-bar',
    iconBg: 'bg-purple-500',
    step: 4,
    title: 'Step 4 — Enter Results',
    body: 'Go to <strong>Results</strong>. Scan the sample barcode or search manually. Enter the measured value for each test.',
    sub: 'The system automatically compares values to reference ranges and flags them as Normal, Abnormal, or Critical. Click Approve when done.',
    link: { href: 'results.html', label: 'Go to Results' }
  },
  {
    icon: 'fa-file-medical',
    iconBg: 'bg-rose-500',
    step: 5,
    title: 'Step 5 — Print the Report',
    body: 'Go to <strong>Reports</strong> to find the complete patient report with all test results, reference ranges, and lab details.',
    sub: 'Reports are ready once results are approved. Print and hand to the patient or referring doctor.',
    link: { href: 'reports.html', label: 'Go to Reports' }
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
            <div class="text-xs font-semibold ${col.text} uppercase tracking-wider">Help — ${c.title}</div>
            <div class="text-gray-500 text-xs">How this page works</div>
          </div>
        </div>
        <button onclick="Help.closeHelp()" class="text-gray-400 hover:text-gray-600 p-1 transition-colors"><i class="fas fa-times"></i></button>
      </div>
      <div class="px-5 py-4 space-y-4 max-h-[60vh] overflow-y-auto">
        <p class="text-gray-700 text-sm leading-relaxed">${c.description}</p>
        <div>
          <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">What to do here</p>
          <ul class="space-y-1.5">
            ${c.actions.map(a => `<li class="flex items-start gap-2 text-xs text-gray-600"><i class="fas fa-check text-green-500 mt-0.5 flex-shrink-0"></i>${a}</li>`).join('')}
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
    // Inject ? button into sticky header
    document.addEventListener('DOMContentLoaded', () => {
      const header = document.querySelector('.sticky.top-0');
      if (!header) return;
      const rightSlot = header.querySelector('.flex.items-center.gap-3, .flex.items-center.gap-2, button[onclick]')?.parentElement || header.lastElementChild;
      if (!rightSlot) return;

      const btn = document.createElement('button');
      btn.title = 'Help — how this page works';
      btn.className = 'w-8 h-8 rounded-full border border-gray-300 bg-white hover:bg-gray-50 text-gray-500 hover:text-blue-600 flex items-center justify-center transition-colors text-sm font-bold flex-shrink-0';
      btn.innerHTML = '?';
      btn.onclick = () => Help.openHelp(pageKey);
      rightSlot.appendChild(btn);
    });
  }
};

// ─── Onboarding Tour ───────────────────────────────────────────────────────────
(function() {
  const STORAGE_KEY = 'enigma_tour_done';
  let currentStep = 0;
  let tourEl = null;

  function buildTour() {
    const el = document.createElement('div');
    el.id = 'tourOverlay';
    el.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.75);backdrop-filter:blur(6px);z-index:1000;display:flex;align-items:center;justify-content:center;padding:1rem;';
    document.body.appendChild(el);
    tourEl = el;
    renderStep(0);
  }

  function renderStep(step) {
    const s = TOUR_STEPS[step];
    const total = TOUR_STEPS.length;
    const isLast = step === total - 1;

    const dots = TOUR_STEPS.map((_, i) =>
      `<span class="w-2 h-2 rounded-full transition-all ${i === step ? 'bg-blue-500 scale-125' : 'bg-gray-300'}"></span>`
    ).join('');

    const linkBtn = s.link
      ? `<a href="${s.link.href}" class="text-xs text-blue-600 hover:text-blue-700 underline underline-offset-2">${s.link.label} &rarr;</a>`
      : '';

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
              ${s.step ? `<div class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-0.5">Step ${s.step} of 5</div>` : '<div class="text-xs font-bold text-blue-500 uppercase tracking-widest mb-0.5">Welcome</div>'}
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

  window.Tour = {
    next() { currentStep = Math.min(currentStep + 1, TOUR_STEPS.length - 1); renderStep(currentStep); },
    prev() { currentStep = Math.max(currentStep - 1, 0); renderStep(currentStep); },
    skip() { localStorage.setItem(STORAGE_KEY, '1'); tourEl?.remove(); tourEl = null; },
    done() { localStorage.setItem(STORAGE_KEY, '1'); tourEl?.remove(); tourEl = null; }
  };

  Help.startTour = function() {
    if (localStorage.getItem(STORAGE_KEY)) return;
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(buildTour, 600);
    });
  };
})();

// ── API helpers ───────────────────────────────────────────────────────────────
async function api(method, path, body = null) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

const get = (path) => api("GET", path);
const post = (path, body) => api("POST", path, body);
const patch = (path, body) => api("PATCH", path, body);

// ── Toast ─────────────────────────────────────────────────────────────────────
function toast(msg, type = "success") {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.className = `show ${type}`;
  setTimeout(() => el.className = "", 3000);
}

// ── Dashboard ─────────────────────────────────────────────────────────────────
async function loadDashboard() {
  try {
    const data = await get("/api/dashboard");
    document.getElementById("stat-students").textContent = data.total_students;
    document.getElementById("stat-teachers").textContent = data.active_teachers;
    document.getElementById("stat-overdue-count").textContent = data.overdue_fees_count;
    document.getElementById("stat-overdue-amount").textContent = "PKR " + data.overdue_fees_amount.toLocaleString();
    document.getElementById("stat-payrolls").textContent = data.pending_payrolls;
  } catch (e) {
    console.error("Dashboard load failed", e);
  }
}

// ── Unpaid students table ─────────────────────────────────────────────────────
async function loadUnpaidStudents() {
  const tbody = document.getElementById("unpaid-tbody");
  if (!tbody) return;
  try {
    const data = await get("/api/students/unpaid");
    tbody.innerHTML = data.students.map(s => `
      <tr>
        <td>${s.name}</td>
        <td>${s.student_id}</td>
        <td><span class="badge badge-unpaid">${s.unpaid_months} month${s.unpaid_months > 1 ? "s" : ""}</span></td>
        <td>
          <button class="btn btn-success btn-sm" onclick="openMarkPaid(${s.student_id}, '${s.name}')">✓ Mark paid</button>
        </td>
      </tr>
    `).join("") || `<tr><td colspan="4" style="text-align:center;color:var(--muted);padding:24px">All fees settled ✓</td></tr>`;
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="4" style="color:var(--danger)">Failed to load</td></tr>`;
  }
}

// ── Mark paid modal ───────────────────────────────────────────────────────────
let activeStudentId = null;

function openMarkPaid(studentId, name) {
  activeStudentId = studentId;
  document.getElementById("modal-student-name").textContent = name;
  document.getElementById("mark-paid-modal").classList.add("open");
}

function closeMarkPaid() {
  document.getElementById("mark-paid-modal").classList.remove("open");
  activeStudentId = null;
}

async function confirmMarkPaid() {
  if (!activeStudentId) return;
  const amount = parseFloat(document.getElementById("payment-amount").value) || 0;
  try {
    await post(`/api/students/${activeStudentId}/mark-paid?amount=${amount}`);
    toast(`Payment recorded for student #${activeStudentId}`);
    closeMarkPaid();
    loadUnpaidStudents();
    if (document.getElementById("stat-overdue-count")) loadDashboard();
  } catch (e) {
    toast(e.message, "error");
  }
}

// ── Payroll table ─────────────────────────────────────────────────────────────
async function loadPayrolls() {
  const tbody = document.getElementById("payroll-tbody");
  if (!tbody) return;
  try {
    const data = await get("/api/payroll/");
    tbody.innerHTML = data.payrolls.map(p => `
      <tr>
        <td>#${p.id}</td>
        <td>${p.teacher_id}</td>
        <td>${p.month}</td>
        <td>PKR ${p.total_amount.toLocaleString()}</td>
        <td><span class="badge badge-${p.status}">${p.status}</span></td>
        <td style="display:flex;gap:6px">
          ${p.status === "draft" ? `<button class="btn btn-primary btn-sm" onclick="approvePayroll(${p.id})">Approve</button>` : ""}
          ${p.status === "approved" ? `<button class="btn btn-success btn-sm" onclick="markPayrollPaid(${p.id})">Mark Paid</button>` : ""}
        </td>
      </tr>
    `).join("") || `<tr><td colspan="6" style="text-align:center;color:var(--muted);padding:24px">No payrolls yet</td></tr>`;
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="6" style="color:var(--danger)">Failed to load</td></tr>`;
  }
}

async function approvePayroll(id) {
  try {
    await post(`/api/payroll/${id}/approve`);
    toast("Payroll approved");
    loadPayrolls();
  } catch (e) { toast(e.message, "error"); }
}

async function markPayrollPaid(id) {
  try {
    await post(`/api/payroll/${id}/mark-paid`);
    toast("Payroll marked as paid");
    loadPayrolls();
  } catch (e) { toast(e.message, "error"); }
}

// ── Cron triggers ─────────────────────────────────────────────────────────────
async function triggerCron(endpoint, label) {
  try {
    const data = await post(`/api/cron/${endpoint}`);
    toast(`${label} complete`);
    console.log(data);
  } catch (e) { toast(e.message, "error"); }
}

// ── Login ─────────────────────────────────────────────────────────────────────
async function handleLogin(e) {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  try {
    await post("/auth/login", { username, password });
    window.location.href = "/dashboard";
  } catch (e) {
    toast("Invalid credentials", "error");
  }
}

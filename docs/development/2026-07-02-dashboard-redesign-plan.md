# Dashboard Redesign Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Overhaul the Admin and Staff dashboards with premium visual styling, rich data widgets, and intuitive user experiences.

---

### Task 1: Controller Context Updates

**Files:**
- Modify: `admin/routes.py`
- Modify: `staff/routes.py`

- [ ] **Step 1: Expand Admin Dashboard Controller**
  Modify `dashboard()` route in `admin/routes.py` to query and pass:
  - `recent_bookings`: list of last 5 bookings.
  - `pending_staff`: list of staff members where `role == 'staff'` and `is_approved == False`.
  - `upcoming_treks`: list of 5 treks with status `Open` or `Approved` starting in the future.
- [ ] **Step 2: Expand Staff Dashboard Controller**
  Modify `dashboard()` route in `staff/routes.py` to calculate and pass:
  - `total_assigned`: count of assigned treks.
  - `total_hikers`: total number of bookings on those assigned treks.
  - `next_departure`: the closest upcoming assigned trek.

---

### Task 2: Custom Styles & Global Shell Overhaul

**Files:**
- Modify: `static/css/custom.css`
- Modify: `templates/base.html`

- [ ] **Step 1: Add dashboard utility styles**
  Append styled gradients, cards, and sidebar helper rules to `static/css/custom.css`.
- [ ] **Step 2: Beautify main shell**
  Give `templates/base.html` a glassmorphic top navigation bar with clean branding, container paddings, and font improvements.

---

### Task 3: Template Overhauls

**Files:**
- Modify: `templates/admin/dashboard.html`
- Modify: `templates/staff/dashboard.html`

- [ ] **Step 1: Overhaul templates/admin/dashboard.html**
  Create the premium dashboard grids, metric cards, pending guides alarm panel, and recent booking tables.
- [ ] **Step 2: Overhaul templates/staff/dashboard.html**
  Create guide metrics cards (expeditions, total hikers, next departure details) and style the expeditions table.

---

### Task 4: Verification & Validation

- [ ] **Step 1: Run unit tests**
  Execute `python -m unittest test_app.py` to ensure core db and route behaviors remain fully functional.
- [ ] **Step 2: Visual checkout**
  Run server locally (`python app.py`) and verify that dashboards render beautifully on both desktop and mobile layouts.

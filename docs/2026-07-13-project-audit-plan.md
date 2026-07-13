# Project Document Alignment Implementation Plan

---

### Task 1: Backend Controller Updates

**Files:**
- Modify: `routes/admin.py`
- Modify: `routes/staff.py`
- Create: `routes/api.py`
- Modify: `app/__init__.py`

- [ ] **Step 1: Implement Admin edit trek POST action**
  Add POST action `'edit'` under `manage_treks()` in `routes/admin.py` with validation guards.
- [ ] **Step 2: Add API blueprint and endpoints**
  Create `routes/api.py` with endpoints for treks, bookings, and users. Register it in `app/__init__.py`.
- [ ] **Step 3: Update bookings completion trigger on Completed trek status**
  Update `edit_trek()` in `routes/staff.py` to auto-complete bookings when trek status becomes `'Completed'`.

---

### Task 2: Template Modifications

**Files:**
- Modify: `templates/admin/manage_treks.html`
- Modify: `templates/admin/dashboard.html`
- Modify: `templates/staff/edit_trek.html`

- [ ] **Step 1: Add Admin Edit Modal & Button**
  Embed the edit button and Modal `#editModal{{ trek.id }}` in `templates/admin/manage_treks.html`.
- [ ] **Step 2: Integrate Started status in dropdowns**
  Add `<option value="Started">` in `templates/staff/edit_trek.html` and `templates/admin/manage_treks.html`.
- [ ] **Step 3: Render popular treks chart**
  Load Chart.js via CDN and setup a script rendering the bar chart inside `templates/admin/dashboard.html`.

---

### Task 3: Testing & Verification

**Files:**
- Modify: `tests/test_app.py`

- [ ] **Step 1: Write test coverage**
  Add test cases for:
  - Admin Edit Trek
  - API resource endpoints
  - Auto-completion of bookings
- [ ] **Step 2: Run verification tests**
  Execute test suite to confirm 100% correct execution.

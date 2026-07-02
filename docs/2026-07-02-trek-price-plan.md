# Trek Price Integration Implementation Plan

---

### Task 1: Schema & Controller Updates

**Files:**
- Modify: `models.py`
- Modify: `admin/routes.py`
- Modify: `staff/routes.py`

- [ ] **Step 1: Add column to Trek model**
  Add `price = db.Column(db.Float, nullable=True)` to `class Trek` in `models.py`.
- [ ] **Step 2: Update admin/routes.py**
  Extract `price = float(request.form.get('price')) if request.form.get('price') else 0.0` in the `create` action of `manage_treks()` and save it.
- [ ] **Step 3: Update staff/routes.py**
  Extract `price = float(request.form.get('price')) if request.form.get('price') else 0.0` in `create_trek()` and save it.

---

### Task 2: Schema Migration & Seeding

- [ ] **Step 1: Write migration statement**
  Update database structure to append `price` column using a python alter statements execution script.

---

### Task 3: Template Updates

**Files:**
- Modify: `templates/admin/manage_treks.html`
- Modify: `templates/staff/dashboard.html`
- Modify: `templates/trekker/dashboard.html`
- Modify: `templates/trekker/my_bookings.html`
- Modify: `templates/admin/view_bookings.html`

- [ ] **Step 1: Add form input fields**
  - Add price input to Admin and Staff trek creation modal forms.
- [ ] **Step 2: Render prices**
  - Display price inside admin, staff, and trekker cards and tables.

---

### Task 4: Automated Testing & Verification

**Files:**
- Modify: `test_app.py`

- [ ] **Step 1: Update mock treks**
  Update `test_app.py` instantiations to verify price parameters on insertion.
- [ ] **Step 2: Run verification tests**
  Validate all tests pass cleanly.

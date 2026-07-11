# Staff Trek Proposal Implementation Plan

---

### Task 1: Route Controller Updates

**Files:**
- Modify: `staff/routes.py`

- [ ] **Step 1: Add create_trek route**
  Create a new POST handler `@staff_bp.route('/staff/create_trek', methods=['POST'])` that extracts form inputs and creates a new `Trek` model with `'Pending'` status and `assigned_staff_id=current_user.id`.

---

### Task 2: Template Modifications

**Files:**
- Modify: `templates/staff/dashboard.html`

- [ ] **Step 1: Add Propose Button**
  Add a **"Propose New Trek"** button next to the page header.
- [ ] **Step 2: Add Propose Modal**
  Add the modal markup containing inputs for name, location, difficulty, duration, capacity, start/end dates, altitude, length, and safety gear.

---

### Task 3: Test Automation

**Files:**
- Modify: `test_app.py`

- [ ] **Step 1: Add Propose Unit Test**
  Append a `test_staff_propose_trek` test method to `TrekAppTestCase` verifying route posting, status marking, and database record fields.

---

### Task 4: Verification

- [ ] **Step 1: Run unit tests**
  Execute `python -m unittest test_app.py` and confirm all 10 tests pass successfully.

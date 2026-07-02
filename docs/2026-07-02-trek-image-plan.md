# Trek Cover Image Integration Implementation Plan

---

### Task 1: Schema & Controller Updates

**Files:**
- Modify: `models.py`
- Modify: `admin/routes.py`
- Modify: `staff/routes.py`

- [ ] **Step 1: Add column to Trek model**
  Add `image_url = db.Column(db.String(500), nullable=True)` to `class Trek` in `models.py`.
- [ ] **Step 2: Update admin/routes.py**
  Extract `image_url = request.form.get('image_url')` in `manage_treks()` and save it.
- [ ] **Step 3: Update staff/routes.py**
  Extract `image_url = request.form.get('image_url')` in `create_trek()` and save it.

---

### Task 2: Schema Migration

- [ ] **Step 1: Execute migration helper**
  Run database migration statements appending `image_url` column to the `treks` table.

---

### Task 3: Template Overhauls

**Files:**
- Modify: `templates/admin/manage_treks.html`
- Modify: `templates/staff/dashboard.html`
- Modify: `templates/trekker/dashboard.html`
- Modify: `templates/trekker/my_bookings.html`
- Modify: `templates/admin/view_bookings.html`

- [ ] **Step 1: Add form input fields**
  - Add optional text input for Image URL inside creation/proposal modals.
- [ ] **Step 2: Render thumbnails and card images**
  - Insert cover images at the top of Trekker finder cards.
  - Insert rounded thumbnails next to Trek names inside management and booking grids.

---

### Task 4: Automated Testing & Verification

**Files:**
- Modify: `test_app.py`

- [ ] **Step 1: Update mock treks**
  Verify parameter inclusion.
- [ ] **Step 2: Run verification tests**
  Confirm test suites execute successfully.

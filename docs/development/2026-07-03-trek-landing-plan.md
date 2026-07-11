# Landing Page Treks & Visual Card Implementation Plan

---

### Task 1: Controller Data Passing

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Retrieve featured treks**
  Import `Trek` and query up to 3 open/approved treks, passing them to the index template:
  ```python
  from models import Trek
  featured_treks = Trek.query.filter(Trek.status.in_(['Approved', 'Open'])).limit(3).all()
  return render_template('index.html', featured_treks=featured_treks)
  ```

---

### Task 2: Custom Stylesheets

**Files:**
- Modify: `static/css/custom.css`

- [ ] **Step 1: Add card styling rules**
  Add styles for:
  - `.trek-card-visual` (rounded corners, transitions, shadows)
  - `.trek-card-img-container` (fixed height, gradient overlays)
  - `.trek-card-badge-overlay` (crimson red ribbon styling)
  - `.trek-card-meta-row` (overlay flex positions, white text)
  - `.trek-card-title-maroon` (wine red text, centered styling)
  - `.trek-card-link-red` (maroon underlined links)

---

### Task 3: Template Integration

**Files:**
- Modify: `templates/index.html`
- Modify: `templates/trekker/dashboard.html`

- [ ] **Step 1: Update index.html**
  - Add "Featured Treks" navbar link.
  - Insert the featured treks showcase section displaying cards styled like the reference image.
  - Add details modal blocks for each featured trek.
- [ ] **Step 2: Update templates/trekker/dashboard.html**
  - Re-engineer cards to use the new visual overlays, thumbnails, and modal-popup details.

---

### Task 4: Testing & Verification

**Files:**
- Modify: `test_app.py`

- [ ] **Step 1: Run verification checks**
  Verify the test suite passes, and ensure compilation works.

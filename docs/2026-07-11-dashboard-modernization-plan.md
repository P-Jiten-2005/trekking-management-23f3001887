# Dashboard Modernization Plan

---

### Task 1: Append Stylesheets

**Files:**
- Modify: `static/css/custom.css`

- [ ] **Step 1: Set neutral background**
  Override body background color using `#f4f6f4`.
- [ ] **Step 2: Append `.metric-card-modern`**
  Declare layout constraints, shadows, transitions, and top-borders.
- [ ] **Step 3: Append `.table-modern`**
  Set rounded borders, uppercase header labels, row spacing, and soft hover colors.
- [ ] **Step 4: Standardize Buttons**
  Verify `.btn` definitions map button shapes and focus outlines to design tokens.

---

### Task 2: Template Modifications

**Files:**
- Modify: `templates/admin/dashboard.html`
- Modify: `templates/staff/dashboard.html`
- Modify: `templates/trekker/dashboard.html`

- [ ] **Step 1: Apply styles to Admin Dashboard**
  Change four metric cards to `.metric-card-modern` and apply table classes and empty state layouts.
- [ ] **Step 2: Apply styles to Staff Dashboard**
  Change three metric cards to `.metric-card-modern` and update theassigned treks table and empty state.
- [ ] **Step 3: Apply styles to Trekker Dashboard**
  Clean up filters and search form blocks, and replace the empty treks list indicator with a custom card container.

---

### Task 3: Testing & Verification

- [ ] **Step 1: Run unit tests**
  Ensure the Flask templates compile and render cleanly and all 12 tests pass successfully.

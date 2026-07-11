# Footer Redesign Plan

---

### Task 1: Style Definitions

**Files:**
- Modify: `static/css/custom.css`

- [x] **Step 1: Append styles**
  Define styles for `.footer-custom`, `.footer-link`, and `.btn-footer` representing modern transitions, hover lifts, shadows, and focus rings.

---

### Task 2: Template Modifications

**Files:**
- Modify: `templates/base.html`
- Modify: `templates/index.html`

- [x] **Step 1: Import Bootstrap Icons**
  Add the Bootstrap Icons link in the head block of both `templates/base.html` and `templates/index.html`.
- [x] **Step 2: Replace footer**
  Replace the legacy footer element inside `templates/index.html` with the new Contact Us & action buttons footer structure.

---

### Task 3: Testing & Verification

- [x] **Step 1: Run unit tests**
  Ensure the Flask templates compile and render cleanly and all 12 tests pass successfully.

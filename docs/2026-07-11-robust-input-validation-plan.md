# Input Validation & Defensive Coding Implementation Plan

---

### Task 1: Controller Refactoring

**Files:**
- Modify: `admin/routes.py`
- Modify: `staff/routes.py`
- Modify: `trekker/routes.py`

- [ ] **Step 1: Refactor admin/routes.py**
  Add try-except parsing blocks, date comparison validation, and positive value checks to `manage_treks()`.
- [ ] **Step 2: Refactor staff/routes.py**
  Add try-except parsing blocks, date comparison validation, and positive value checks to `create_trek()` and `edit_trek()`.
- [ ] **Step 3: Refactor trekker/routes.py**
  Add regex validation for `contact` number to `edit_profile()`.

---

### Task 2: Template Form Updates

**Files:**
- Modify: `templates/trekker/edit_profile.html`

- [ ] **Step 1: Update edit_profile.html**
  Add phone pattern and tel validations to the contact input.

---

### Task 3: Unit Testing Validation

**Files:**
- Modify: `test_app.py`

- [ ] **Step 1: Add new test cases**
  Add test cases asserting:
  - Invalid numeric inputs (ValueError prevention check).
  - Invalid date orders (dates integrity check).
  - Profile contact update pattern validation check.
- [ ] **Step 2: Run test suite verification**
  Ensure all unit tests pass cleanly.

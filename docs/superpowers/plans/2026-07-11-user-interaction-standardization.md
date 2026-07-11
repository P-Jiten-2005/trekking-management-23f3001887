# User Interaction Standardization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standardize interaction components (modals, search buttons, dropdown difficulty selectors, cards) across 5 Jinja template files to unify design and layout, followed by verification.

**Architecture:** Update HTML/Jinja template syntax to use consistent Bootstrap class names, remove emoji styling decorations from dropdown fields, and normalize modal footer/action triggers.

**Tech Stack:** Bootstrap 5, Jinja2, HTML5

## Global Constraints

- Compile Jinja templates and run tests: `python -m unittest test_app.py` verifying all 12 tests pass successfully.
- Stage modifications and commit locally: `git commit -m "feat: standardize form dropdown options, interactive buttons, and modals inside views"`.
- Write your summary report to: `D:\Jiten\Trek\modernization-task-interact-report.md`.
- Report status as DONE or BLOCKED.

---

### Task 1: Update Admin Templates

**Files:**
- Modify: `D:/Jiten/Trek/templates/admin/manage_treks.html`
- Modify: `D:/Jiten/Trek/templates/admin/user_management.html`

- [ ] **Step 1: Standardize Create Trek button in manage_treks.html**
  Replace line 10 button with Bootstrap icon representation instead of emoji.
- [ ] **Step 2: Standardize search form card style and button color in manage_treks.html**
  Update the form container card to `border-0 shadow-sm` and its search button to `btn-primary`.
- [ ] **Step 3: Remove emojis from difficulty select options in manage_treks.html**
  Remove 🟢, 🟡, and 🔴 from easy, moderate, hard options in the create modal.
- [ ] **Step 4: Standardize search form card style and button color in user_management.html**
  Update form container card to `border-0 shadow-sm` and search button to `btn-primary`.

---

### Task 2: Update Trekker Dashboard Template

**Files:**
- Modify: `D:/Jiten/Trek/templates/trekker/dashboard.html`

- [ ] **Step 1: Standardize difficulty filter dropdown options**
  Unify dropdown filter to use "All Difficulties" without emojis.
- [ ] **Step 2: Standardize filter button classes**
  Remove `py-2` from the submit button.
- [ ] **Step 3: Normalize details modal content styling**
  Remove inline border radius and border/shadow overrides from the modal content container.
- [ ] **Step 4: Standardize modal footer buttons**
  Replace green `btn-success w-100 py-3 rounded-3 fw-bold` with unified blue `btn-primary w-100` action.

---

### Task 3: Update Index Page Template

**Files:**
- Modify: `D:/Jiten/Trek/templates/index.html`

- [ ] **Step 1: Normalize details modal content styling**
  Remove inline border-radius styling from the modal content container.
- [ ] **Step 2: Standardize modal footer buttons and alerts**
  Remove success styling, extra paddings, custom borders/border-radii on buttons, and pad margins. Change buttons to `btn-primary` and clean up the alert container styling.

---

### Task 3: Update Staff Dashboard Template

**Files:**
- Modify: `D:/Jiten/Trek/templates/staff/dashboard.html`

- [ ] **Step 1: Remove emojis from difficulty selection inside proposal modal**
  Remove 🟢, 🟡, and 🔴 from easy, moderate, hard options.
- [ ] **Step 2: Standardize proposal submit button**
  Change submit button style from `btn-success` to `btn-primary`.

---

### Task 4: Testing and Completion

**Files:**
- Test: Run `python -m unittest test_app.py`
- Create: `D:\Jiten\Trek\modernization-task-interact-report.md`

- [ ] **Step 1: Verify all tests compile and pass**
  Run test suite and confirm 12/12 pass.
- [ ] **Step 2: Commit local git changes**
  Run git commit with the specified message.
- [ ] **Step 3: Write report**
  Write progress report to `D:\Jiten\Trek\modernization-task-interact-report.md`.

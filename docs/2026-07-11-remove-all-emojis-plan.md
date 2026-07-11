# Emoji Removal Implementation Plan

---

### Task 1: Clean Template Files

**Files:**
- Modify: `templates/base.html`
- Modify: `templates/index.html`
- Modify: `templates/auth/register.html`
- Modify: `templates/admin/dashboard.html`
- Modify: `templates/admin/manage_treks.html`
- Modify: `templates/admin/user_management.html`
- Modify: `templates/staff/dashboard.html`
- Modify: `templates/trekker/dashboard.html`

- [ ] **Step 1: Clean base.html**
  Remove `🏔️` from brand brand name.
- [ ] **Step 2: Clean index.html**
  Remove mountain, boot, hands, leaf, hospital, alarm, bus, tree, stopwatch, location, star, shield, and peak emojis. Replace rating with text.
- [ ] **Step 3: Clean register.html**
  Remove emojis from slider role labels.
- [ ] **Step 4: Clean admin dashboard & user management**
  Remove crown, star, and status emojis.
- [ ] **Step 5: Clean admin manage treks**
  Remove schedule badges and metadata list emojis.
- [ ] **Step 6: Clean staff dashboard**
  Remove greetings, metadata, and proposed modal emojis.
- [ ] **Step 7: Clean trekker dashboard**
  Remove metadata, star rating, and detail modal emojis.

---

### Task 2: Testing & Verification

- [ ] **Step 1: Run verification tests**
  Ensure test suites compile and pass successfully.

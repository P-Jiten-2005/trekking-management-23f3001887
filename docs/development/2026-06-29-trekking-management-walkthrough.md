# Trekking Management Application - Walkthrough

The Trekking Management Application has been successfully developed, integrated, and verified.

## 1. Accomplished Work

We built a modular, secure, and responsive Flask web application utilizing SQLite and Flask-Login.

### Major Subsystems Developed:
1. **Core Factory & Seeding (`app.py`, `config.py`, `models.py`, `extensions.py`)**:
   - Programmatic database generation.
   - Separated SQLAlchemy and LoginManager instances to `extensions.py` to prevent circular imports and `__main__` namespace duplication during CLI/manual runs.
   - Seeded default Admin account (`admin@trek.com` / `admin123`).
2. **Access Control (`decorators.py`)**:
   - Custom `@role_required` check that verifies authentication, role level, whitelist status, and staff approval status.
3. **Authentication Blueprint (`auth`)**:
   - Custom routes and views for Login, Logout, Trekker registration, and Staff registration (which defaults to pending approval).
4. **Admin Blueprint (`admin`)**:
   - Metric dashboards showing global stats.
   - Trek creation, route management, and staff assignment.
   - Staff approval and blacklist controls.
   - **Trek schedule classification and sorting**: classifies treks relative to `date.today()` into Past, Active, or Future, and sorts all query lists by start date descending.
   - **Alphabetical sorting**: sorts user listings alphabetically by name in the management tab.
   - **Staff Promotion**: allows administrators to promote approved staff members to Admin, keeping their trek assignments active.
5. **Staff Blueprint (`staff`)**:
   - Dashboard of assigned treks.
   - Participant list viewing and slot/status updates with strict validation guards.
6. **Trekker Blueprint (`trekker`)**:
   - Find treks page with difficulty and location filters.
   - Booking checkouts with overbooking protection.
   - History logs and profile editing.
7. **Premium Styling (`static/css/custom.css`, `templates/base.html`)**:
   - Outdoors aesthetic with custom HSL gradient background, cards, and structured tables.

---

## 2. Test Verification

We wrote an automated test suite in [test_app.py](file:///D:/Jiten/Trek/test_app.py) verifying the core database relationships and business requirements:
- Seeding of default Admin credentials and roles.
- Default approval states (unapproved for staff, approved for trekkers).
- Valid assignment between treks and staff.
- Booking constraints: treks must be in the `'Open'` state and have available capacity.
- Prevention of overbooking when remaining slots reach 0.
- **Chronological sorting of treks** by start date descending.
- **Staff promotion validation**: ensures role updates to `'admin'` successfully.

### Verification Run Results:
```text
Ran 8 tests in 7.260s

OK
```

All 8 test cases passed, verifying correct logic behavior.

---

## 3. Manual Run Instructions

To launch the portal locally:
1. Ensure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Initialize and seed the database:
   ```bash
   python init_db.py
   ```
3. Run the development server:
   ```bash
   python app.py
   ```
4. Open your browser to `http://127.0.0.1:5000` to interact with the application.

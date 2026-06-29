# Change Log

This file tracks all changes made by the AI agent during the project development lifecycle.

## [2026-06-29]

### Added
- Created `requirements.txt` with application dependencies (`Flask`, `Flask-SQLAlchemy`, `Flask-Login`, `Werkzeug`).
- Created `config.py` with SQL URI pointing to `instance/trekking.db` and Flask session key configurations.
- Created `extensions.py` containing unified `db` and `login_manager` instances to prevent circular import and `__main__` namespace errors.
- Created `models.py` with database tables/relationships:
  - `User`: Admin, Trek Staff, Trekker data. Includes fields for approval (`is_approved`) and whitelisting (`is_blacklisted`).
  - `Trek`: Trek routes details, available slots, status (`Pending`, `Approved`, `Open`, `Closed`, `Completed`), and staff assignment relation.
  - `Booking`: Mapping between users and treks, status tracking (`Booked`, `Cancelled`, `Completed`).
- Created `decorators.py` with custom `@role_required` decorator supporting authentication state checks, blacklist checks, and staff approval redirects.
- Created `auth` Blueprint (`auth/routes.py` and templates):
  - Login & Logout controls.
  - Trekker self-registration (auto-approved).
  - Staff self-registration (defaults to unapproved, redirects to `pending_approval.html` on login).
- Created `admin` Blueprint (`admin/routes.py` and templates):
  - Dashboard displaying metrics.
  - Trek route management (create, delete, approve).
  - Staff whitelisting, approval, and user/staff deactivation/blacklisting.
  - Booking list views.
  - Search engine for treks, staff, and users.
- Created `staff` Blueprint (`staff/routes.py` and templates):
  - Assigned treks overview.
  - Registered trekkers contacts list.
  - Trek details updates (remaining available slots and status) with capacity guards.
- Created `trekker` Blueprint (`trekker/routes.py` and templates):
  - Find Treks dashboard with search queries and difficulty filters.
  - Trek booking with overbooking check and double booking prevention.
  - My Bookings list showing registration history.
  - Profile modification page.
- Created static custom stylesheet `static/css/custom.css` containing premium color tokens, fonts (Outfit), card shadows, and transition states.
- Created layouts:
  - `templates/base.html`: Common container header, navigation bar with role-specific items, alert flashes, and standard bootstrap bundle.
  - `templates/index.html`: Dynamic welcome page showing dashboard links if logged in, otherwise auth choices.
- Created database seed script `init_db.py` to create tables and pre-populate the default Admin account (`admin@trek.com` / `admin123`).
- Created `test_app.py` containing automated unit test suites for database relationships, access levels, slot rules, and overbooking checks.
- Initialized local git repository, added all code and documents, and committed them to `master`.
- Created `.gitignore` file to ignore build folders, environment files, and local SQLite databases.
- Configured git remote pointing to `https://github.com/P-Jiten-2005/trekking-management-23f3001887`.
- Renamed default branch to `main` and pushed codebase to remote.

### Fixed
- Fixed a `RuntimeError` regarding SQLAlchemy registry bindings by moving `db` to a standalone `extensions.py` module, removing circular import chains.
- Fixed a test runner `IntegrityError` by calling `trekker.set_password('password')` on mock users during test creation, ensuring the NOT NULL constraint is satisfied.
- Removed build cache files (`__pycache__`) and local database files (`instance/trekking.db`) from git index tracking so they are ignored under new `.gitignore` rules.

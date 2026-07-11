# Change Log

This file tracks all changes made by the AI agent during the project development lifecycle.

## [2026-07-11]

### Added
- **Robust Input Validation & Casting Defenses**: Implemented defensive try-except validation blocks for numeric casting and date chronological bounds on trek creation (Admin) and proposals (Staff) in `admin/routes.py` and `staff/routes.py`.
- **Indian Phone Regex checks on Profiles**: Integrated backend regex format matching (`^\+91\d{10}$`) for user contact details updates inside `trekker/routes.py`.
- **HTML5 Input Form Enforcement**: Added `tel`, `pattern`, `title`, and `required` parameters to the contact details input in `templates/trekker/edit_profile.html`.
- **Automated Validation Test Cases**: Added `test_admin_create_trek_validation` and `test_trekker_profile_contact_validation` tests to [test_app.py](file:///D:/Jiten/Trek/test_app.py).
- **Created a design specification and implementation plan** for input validation and defensive coding at `docs/superpowers/specs/2026-07-11-robust-input-validation-spec.md` and `docs/2026-07-11-robust-input-validation-plan.md`.
- **Emoji Removal**: Cleaned up 8 template files and `README.md` to remove all informal graphical emojis.
- **Created a design specification and implementation plan** for emoji removal at `docs/superpowers/specs/2026-07-11-remove-all-emojis-spec.md` and `docs/2026-07-11-remove-all-emojis-plan.md`.

---

## [2026-07-03]

### Added
- **Featured Treks Showcase Section**: Integrated a showcase section inside the landing page `templates/index.html` querying up to 3 approved treks from [app.py](file:///D:/Jiten/Trek/app.py). Added navbar anchor links.
- **Trek Visual Card Redesign**: Overhauled trek booking cards inside `templates/trekker/dashboard.html` and the landing page to feature visual image overlays, top-left crimson ribbons ("Best Seller" / "Trending"), bottom meta overlaps (duration and difficulty), centered wine-red titles, star ratings, and an underlined "View Details" trigger launching a Bootstrap modal specs popup with full details and booking/login calls.
- **Visual Card Stylesheets**: Appended card hover transforms, image zoom triggers, gradient underlays, red ribbons, and customized links inside `static/css/custom.css`.
- **Created a design specification and implementation plan** for the landing page featured showcase and visual card overlays at `docs/superpowers/specs/2026-07-03-trek-landing-spec.md` and `docs/2026-07-03-trek-landing-plan.md`.

---

## [2026-07-02]

### Added
- **Created a design specification and implementation plan** for the dashboard redesign at `docs/superpowers/specs/2026-07-02-dashboard-redesign-spec.md` and `docs/2026-07-02-dashboard-redesign-plan.md`.
- **Created a design specification and implementation plan** for the staff trek proposal feature at `docs/superpowers/specs/2026-07-02-staff-create-trek-spec.md` and `docs/2026-07-02-staff-create-trek-plan.md`.
- **Created a design specification and implementation plan** for the trek price integration feature at `docs/superpowers/specs/2026-07-02-trek-price-spec.md` and `docs/2026-07-02-trek-price-plan.md`.
- **Added CSS styling classes** for the premium glassmorphic navbar and gradient metric cards (`.glass-navbar`, `.metric-card`, `.action-card`, `bg-grad-*`) to `static/css/custom.css`.
- **Integrated a sticky glassmorphic navigation bar** in `templates/base.html` for clean layout spacing.
- **Redesigned the Admin Dashboard** at `templates/admin/dashboard.html` to feature:
  - Four premium HikerHub gradient cards (Treks, Trekkers, Staff, Bookings).
  - A **Recent Bookings** ledger table.
  - An **Upcoming Departures** schedule table.
  - A **Pending Staff Registrations** alert sidebar to approve new guides directly.
- **Redesigned the Staff Dashboard** at `templates/staff/dashboard.html` to feature:
  - A personalized guide greeting header.
  - Three premium metrics cards: Assigned Treks, Hikers Led, and Next Departure launch details.
  - A clean, status-badged table of assigned expeditions with quick-action links.
  - A **"Propose New Trek"** modal form allowing guides to submit trek proposals directly.
- **Added staff trek proposal capabilities**: Route endpoint `/staff/create_trek` handles trek submissions, saving them with `Pending` status and assigning them to the proposing guide automatically.
- **Added pricing support to treks**: Added `price` column (float, nullable) to the `Trek` schema model in `models.py`.
- **Added price fields and displays**: Integrated price inputs to Admin creation and Staff proposal modals, and displayed prices across all dashboards and booking ledgers (Trekker dashboard, Trekker my bookings, Admin view bookings).
- **Added unit test `test_staff_propose_trek`** inside [test_app.py](file:///D:/Jiten/Trek/test_app.py) validating the staff creation route and database state constraints.
- **Added price parameter checks to tests** inside [test_app.py](file:///D:/Jiten/Trek/test_app.py) to cover model creation assertions.

### Changed
- **Updated route handlers** in `admin/routes.py` and `staff/routes.py` to retrieve the additional context variables (recent bookings, upcoming treks, pending staff, total hikers, next departures) needed for the redesigned dashboard widgets.
- **Modified routes** in `admin/routes.py` and `staff/routes.py` to parse and save `price` form data.

---

## [2026-06-30]

### Added
- **Created a custom Eco-Hikes landing page** at `templates/index.html` featuring a sticky transparent navbar, custom menu, full-screen Himalayan hero background image, and content cards for "What We Do", "Get Involved", and "About".
- **Added landing page style tokens** to `static/css/custom.css` (smooth scroll, glassmorphic navbar transitions, full-screen hero overlays, responsive typography).
- **Created a unified registration interface** at `templates/auth/register.html` with a matching frosted-glass style layout, and integrated a pure-CSS sliding switch/segmented control to toggle between Trekker and Staff guide roles.
- **Added Confirm Password** field and validations to `templates/auth/register.html` and `auth/routes.py`.
- **Added Indian contact format validation** (`+91` prefix followed by exactly 10 digits) using HTML5 `pattern` attributes and backend regex checks inside `auth/routes.py`.
- **Added registration validation tests** (`test_register_validation`) inside `test_app.py`.
- **Expanded landing page "What We Do" section** from 3 cards to 6 cards by adding dedicated feature blocks for **Medical Assistance**, **Emergency Support**, and **Pick & Drop Transit**.
- **Added safety_equipment, altitude, and length columns** to the `Trek` schema model in `models.py`.
- **Added max altitude, route length, and required safety gear** inputs to the Admin's "Create Trek" modal inside `templates/admin/manage_treks.html`.
- **Displayed trek dimensions and safety lists** across Admin's manage table (`templates/admin/manage_treks.html`), Staff assigned view (`templates/staff/dashboard.html`), and Trekker find cards (`templates/trekker/dashboard.html`).

### Changed
- Changed default seeded Admin email from `admin@trek.com` to `Jiten@trek.com` and password from `admin123` to `Jiten@123` across `app.py`, `init_db.py`, `test_app.py`, and `README.md`.
- **Renamed application brand name to HikerHub** across all HTML templates and documentation layout.
- **Updated application caption** in `index.html` to *"Your next adventure starts with the right community"*.
- **Simplified guest access block** on the landing page to render a single, centered **Log In** button instead of dual columns for registering.
- **Redesigned the Log In interface** at `templates/auth/login.html` into a premium frosted-glass design featuring full-screen lock-viewport styling, Himalayan mountain background base layers, a 24px backdrop blur overlay, an elevated centralized form card, custom inputs with focus ring states, and a forest-green submit button (#1E7A44) with dark transitions.
- **Unified registration flows** under a single `/register` route in `auth/routes.py` (redirecting `/register/trekker` and `/register/staff` to this endpoint).
- **Updated Login footer** to link directly to the new unified registration page.
- **Updated README.md** to include a "🔐 Authentication & Validation Highlights" section detailing custom layouts, CSS role switch toggles, password verification checks, and Indian mobile format constraints.
- **Cleaned up README.md** by removing "Getting Started", "Database Inspection Guide", and "Running Unit Tests" sections.

### Deleted
- **Removed obsolete templates** `templates/auth/register_user.html` and `templates/auth/register_staff.html`.

### Fixed
- Fixed a template namespace collision where Flask resolved `dashboard.html` to the admin version for other roles by removing `template_folder` overrides from blueprints and prefixing all `render_template` calls with their subdirectory (e.g. `render_template('trekker/dashboard.html')`).

---

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
  - **Added "Promote Staff to Admin" capability** in `user_management` with confirmation gating.
  - **Added sorting and chronological classification for treks** (Past, Active, Future) based on dates compared to `date.today()`, ordered by `start_date` descending.
  - **Added sorting for users** in the Management view (alphabetically by name).
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
- Created `test_app.py` containing automated unit test suites:
  - Database relationships and model creation.
  - Access controls and approval limits.
  - Overbooking checks.
  - **Added `test_promote_staff_to_admin`** unit test.
  - **Added `test_trek_sorting_by_date`** unit test.
- Initialized local git repository, added all code and documents, and committed them to `master`.
- Created `.gitignore` file to ignore build folders, environment files, and local SQLite databases.
- Configured git remote pointing to `https://github.com/P-Jiten-2005/trekking-management-23f3001887`.
- Renamed default branch to `main` and pushed codebase to remote.
- **Created a visually rich and detailed `README.md`** file in the root directory.

### Fixed
- Fixed a `RuntimeError` regarding SQLAlchemy registry bindings by moving `db` to a standalone `extensions.py` module, removing circular import chains.
- Fixed a test runner `IntegrityError` by calling `trekker.set_password('password')` on mock users during test creation, ensuring the NOT NULL constraint is satisfied.
- Removed build cache files (`__pycache__`) and local database files (`instance/trekking.db`) from git index tracking so they are ignored under new `.gitignore` rules.

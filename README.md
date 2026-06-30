# 🏔️ HikerHub - Trekking Management System

**HikerHub** is a premium, feature-rich web portal designed for trekking agencies, guides, and adventure enthusiasts. It streamlines booking workflows, trek assignments, guide coordinations, and participant tracking, replacing messy spreadsheets and manual planning with a unified, role-based dashboard system.

---

## 🌟 Key Features

### 👑 Admin Suite
- **Global Overview Dashboard**: Quick-glance metrics for total treks, registered trekkers, active staff, and overall bookings.
- **Trek Route Builder**: Add, review, approve, and delete trek events.
- **Staff Assignment Matrix**: Assign approved guides/staff members to specific routes.
- **Chronological Classifications & Sorting**: Treks are automatically categorized into **Past 🕰️**, **Active 🏃‍♂️**, or **Future 📅** schedules and sorted with the newest/future treks first.
- **User Directory**: View, approve new guide registrations, and whitelist or blacklist/deactivate users & staff members.
- **Staff Promotion**: Promote active guides to Administrator status directly with confirmation verification checks.
- **Search Engine**: Search treks and users by names, email addresses, or IDs.

### 🥾 Trek Staff Portal
- **My Expeditions**: Dashboard listing assigned treks, departure dates, capacity status, and participant headcounts.
- **Trekkers Log**: View contact cards and registration details of participants booked on assigned treks.
- **Capacity Management**: Adjust remaining available slots and toggle trek status (`Pending`, `Approved`, `Open`, `Closed`, `Completed`) with robust capacity validation guards.

### ⛺ Trekker (User) Experience
- **Adventure Finder**: Search open treks by keywords or filter routes by difficulty (`Easy`, `Moderate`, `Hard`).
- **Atomic Checkout**: Direct booking with automatic slot decrementing, overbooking prevention, and double-booking protection.
- **Expedition History**: Personal ledger tracking active bookings and completed historic treks.
- **Profile Customizer**: Update personal details and contact numbers.

---

## 🛠️ Technology Stack

- **Backend Logic**: Python 3.10+ / Flask / Flask-Login (session controls)
- **Database Layer**: SQLite / Flask-SQLAlchemy (relational mapping & transactions)
- **UI Template System**: Jinja2 / HTML5
- **Front-end Design**: Vanilla CSS3 / Bootstrap 5 (Responsive Layout, custom Outfit typography, outdoors-themed visual palettes, card hover animations)

---

## 📂 Codebase Directory Mapping

```text
Trek/
├── .agents/                # AI Agent tracks (Changelog and Workspace Context)
│   ├── changelog.md
│   └── context.md
├── auth/                   # Authentication Blueprints (Login, Registration, Logout)
│   └── routes.py
├── admin/                  # Admin Dashboard, user management, and trek controls
│   └── routes.py
├── staff/                  # Staff dashboard and trek updates
│   └── routes.py
├── trekker/                # Trekker searching and checkout controls
│   └── routes.py
├── static/
│   └── css/
│       └── custom.css      # Premium custom outdoors stylesheet
├── templates/              # Jinja2 HTML layout templates
│   ├── base.html           # Unified navigation, flashes, and styling links
│   ├── index.html          # Public landing portal
│   ├── auth/               # Login & Register views
│   ├── admin/              # Admin pages
│   ├── staff/              # Staff pages
│   └── trekker/            # Trekker pages
├── docs/                   # Specifications, implementation plans, and walkthroughs
├── app.py                  # Core Application Factory & WSGI entry point
├── config.py               # Key and database configurations
├── extensions.py           # Unified SQLAlchemy & LoginManager instances
├── decorators.py           # Custom @role_required access controller
├── init_db.py              # Script to build tables and seed admin credentials
├── test_app.py             # Automated unit test suite
├── logfile.md              # Turn-by-turn chat and changes logger
└── requirements.txt        # Package dependencies
```

---

## 🚀 Getting Started

Follow these steps to run the project locally on your machine:

### 1. Clone & Navigate
```bash
git clone https://github.com/P-Jiten-2005/trekking-management-23f3001887.git
cd trekking-management-23f3001887
```

### 2. Set Up Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize and Seed Database
Generate the database file and populate the default administrator credentials:
```bash
python init_db.py
```
* **Default Admin Login**: `Jiten@trek.com`
* **Default Admin Password**: `Jiten@123`

### 5. Launch the Server
```bash
python app.py
```
Open your browser and navigate to **`http://127.0.0.1:5000`** to access the system.

---

## 🔐 Authentication & Validation Highlights

* **Frosted-Glass Redesign**: The login (`/login`) and unified registration (`/register`) pages utilize a full-screen, responsive lock-viewport structure with a backdrop blur overlay on a majestic Himalayan mountain base layer.
* **Segmented CSS Role Slider**: The registration page features a pure-CSS sliding switch using radio buttons to select between **Trekker 🏕️** and **Trek Staff 🏔️** with zero JavaScript dependencies.
* **Password Match Checks**: Requires entering matching values in both `Password` and `Confirm Password` fields.
* **Indian Phone Validation**: Limits contact details to Indian numbers starting with country code `+91` followed by exactly 10 digits (validated via HTML5 pattern matching and regex backend checks).

---

## 🗄️ Database Inspection Guide

All application state is saved locally in:
📁 **Database File**: `instance/trekking.db`

### Inspecting Database Content
- **VS Code**: Install the extension **SQLite Viewer** (by *qwtel*), and click directly on the `instance/trekking.db` file.
- **GUI Desktop**: Install **DB Browser for SQLite** (from [sqlitebrowser.org](https://sqlitebrowser.org/)), open the app, and browse the database file.
- **Command Line**: Run `flask shell` to query records using SQLAlchemy:
  ```python
  from extensions import db
  from models import User
  for u in User.query.all():
      print(u.name, u.email, u.role)
  ```

---

## 🧪 Running Unit Tests

An automated test suite is provided to verify role registrations, assignment logic, overbooking protections, date sorting rules, and form validation triggers:
```bash
python -m unittest test_app.py
```

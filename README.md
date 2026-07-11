# HikerHub - Trekking Management System

**HikerHub** is a web application that helps manage trekking activities. It allows users to book treks, agencies to organize trips, guides to manage assigned treks, and participants to track their bookings. The system brings all these features together in one place, making trek management easier and more organized.

---

## Key Features

### Admin Suite
- **Global Overview Dashboard**: Quick-glance metrics for total treks, registered trekkers, active staff, and overall bookings.
- **Trek Route Builder**: Add, review, approve, and delete trek events, detailing route length, maximum altitude, and required safety equipment.
- **Staff Assignment Matrix**: Assign approved guides/staff members to specific routes.
- **Chronological Classifications & Sorting**: Treks are automatically categorized into **Past**, **Active**, or **Future** schedules and sorted with the newest/future treks first.
- **User Directory**: View, approve new guide registrations, and whitelist or blacklist/deactivate users & staff members.
- **Staff Promotion**: Promote active guides to Administrator status directly with confirmation verification checks.
- **Search Engine**: Search treks and users by names, email addresses, or IDs.

### Trek Staff Portal
- **My Expeditions**: Dashboard listing assigned treks, departure dates, capacity status, and participant headcounts.
- **Trekkers Log**: View contact cards and registration details of participants booked on assigned treks.
- **Capacity Management**: Adjust remaining available slots and toggle trek status (`Pending`, `Approved`, `Open`, `Closed`, `Completed`) with robust capacity validation guards.

### Trekker (User) Experience
- **Adventure Finder**: Search open treks by keywords or filter routes by difficulty (`Easy`, `Moderate`, `Hard`), viewing specific trek safety equipment requirements, altitudes, and lengths before booking.
- **Atomic Checkout**: Direct booking with automatic slot decrementing, overbooking prevention, and double-booking protection.
- **Expedition History**: Personal ledger tracking active bookings and completed historic treks.
- **Profile Customizer**: Update personal details and contact numbers.

---

## Technology Stack

- **Backend Logic**: Python 3.10+ / Flask / Flask-Login (session controls)
- **Database Layer**: SQLite / Flask-SQLAlchemy (relational mapping & transactions)
- **UI Template System**: Jinja2 / HTML5
- **Front-end Design**: Vanilla CSS3 / Bootstrap 5 (Responsive Layout, custom Outfit typography, outdoors-themed visual palettes, card hover animations)

---

## Codebase Directory Mapping

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

## 🔐 Authentication & Validation Highlights

* **Frosted-Glass Redesign**: The login (`/login`) and unified registration (`/register`) pages utilize a full-screen, responsive lock-viewport structure with a backdrop blur overlay on a majestic Himalayan mountain base layer.
* **Segmented CSS Role Slider**: The registration page features a pure-CSS sliding switch using radio buttons to select between **Trekker** and **Trek Staff** with zero JavaScript dependencies.
* **Password Match Checks**: Requires entering matching values in both `Password` and `Confirm Password` fields.
* **Indian Phone Validation**: Limits contact details to Indian numbers starting with country code `+91` followed by exactly 10 digits (validated via HTML5 pattern matching and regex backend checks).

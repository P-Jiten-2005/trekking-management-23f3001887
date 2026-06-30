# Workspace Context State

This file tracks the current system architecture, database schema, active branch, verification status, and next steps for the Trekking Management Application.

## 1. Environment Details
- **Active Git Branch**: `main`
- **Git Remote Origin**: `https://github.com/P-Jiten-2005/trekking-management-23f3001887`
- **Application Port**: `5000` (Default)
- **Database Engine**: SQLite
- **Database File Location**: `instance/trekking.db` (locally created, ignored by Git)
- **Unit Test File**: `test_app.py`
- **Verification Status**: ✅ 8/8 tests passing (OK)

## 2. Directory Structure
```text
D:\Jiten\Trek/
├── .agents/                # Agent logs and workspace contexts
│   ├── changelog.md
│   └── context.md
├── app.py                  # App factory and entry point
├── config.py               # Database and key configurations
├── extensions.py           # Shared SQLAlchemy & LoginManager instances
├── models.py               # DB Models (User, Trek, Booking)
├── decorators.py           # Custom decorators (@role_required)
├── init_db.py              # DB creation & Admin seeding script
├── test_app.py             # Unit tests suite
├── requirements.txt        # Package dependencies
├── .gitignore              # Files gitignore file
├── logfile.md              # Turn-by-turn chat and changes log
├── README.md               # Visual system documentation
│
├── auth/                   # Authentication Blueprint
│   └── routes.py
├── admin/                  # Admin Blueprint
│   └── routes.py
├── staff/                  # Staff Blueprint
│   └── routes.py
├── trekker/                # Trekker Blueprint
│   └── routes.py
│
├── static/
│   └── css/
│       └── custom.css      # Premium custom CSS styles
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── auth/
│   │   ├── login.html
│   │   ├── register_user.html
│   │   ├── register_staff.html
│   │   └── pending_approval.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── manage_treks.html
│   │   ├── user_management.html
│   │   └── view_bookings.html
│   ├── staff/
│   │   ├── dashboard.html
│   │   ├── edit_trek.html
│   │   └── view_participants.html
│   └── trekker/
│       ├── dashboard.html
│       ├── my_bookings.html
│       └── edit_profile.html
│
└── docs/                   # Project documentation
    ├── 2026-06-29-trekking-management-plan.md
    ├── 2026-06-29-trekking-management-walkthrough.md
    ├── 2026-06-29-admin-search-and-promote-plan.md
    └── superpowers/specs/
        ├── 2026-06-29-trekking-management-design.md
        ├── 2026-06-29-promote-staff-to-admin-design.md
        └── 2026-06-29-admin-search-and-promote-design.md
```

## 3. Database Schema (SQLite)

### Users (`users`)
- `id` (INTEGER, PK)
- `email` (VARCHAR(150), Unique, Not Null) - Default Admin: `Jiten@trek.com`
- `password_hash` (VARCHAR(256), Not Null) - Default Admin password: `Jiten@123`
- `role` (VARCHAR(20), Not Null) - Admin, Trek Staff, or Trekker.
- `name` (VARCHAR(100), Not Null)
- `contact_details` (VARCHAR(200), Nullable)
- `is_approved` (BOOLEAN, Default: True) - False for registered staff.
- `is_blacklisted` (BOOLEAN, Default: False)

### Treks (`treks`)
- `id` (INTEGER, PK)
- `name` (VARCHAR(100), Not Null)
- `location` (VARCHAR(150), Not Null)
- `difficulty` (VARCHAR(20), Not Null)
- `duration` (INTEGER, Not Null)
- `available_slots` (INTEGER, Not Null)
- `max_slots` (INTEGER, Not Null)
- `status` (VARCHAR(20), Default: Pending)
- `start_date` (DATE, Not Null)
- `end_date` (DATE, Not Null)
- `assigned_staff_id` (INTEGER, FK to users.id, Nullable)

### Bookings (`bookings`)
- `id` (INTEGER, PK)
- `user_id` (INTEGER, FK to users.id, Not Null)
- `trek_id` (INTEGER, FK to treks.id, Not Null)
- `booking_date` (DATETIME, Default: current timestamp)
- `status` (VARCHAR(20), Default: Booked)

## 4. Verification Checkpoint
- Seeding: Verified that `init_db.py` populates `Jiten@trek.com` (password: `Jiten@123`).
- Security guards: Checked that blacklisted or unapproved accounts are restricted correctly.
- Slot operations: Atomic decrements on booking are covered and fail when slots run out.
- Promotion validation: Verified that promoting a staff member updates their database role to `'admin'` successfully.
- Chronological marking: Verified that treks correctly class as Past, Active, or Future, and order by start date descending.

## 5. Next Steps / Actions
- Stage new changes (template path fix commits) and push them to the GitHub remote repository.
- Await any instructions or feature enhancements from the user.

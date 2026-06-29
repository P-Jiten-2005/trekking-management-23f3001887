# Design Specification: Trekking Management Application

This specification outlines the architecture, database schema, routing, and verification plan for the Trekking Management Application.

## 1. Overview
The Trekking Management Application is a web-based system that allows an Admin, Trek Staff, and Users (Trekkers) to manage, assign, update, and book trekking routes.
The application is built using:
- **Backend:** Flask, Flask-SQLAlchemy (SQLite database), Flask-Login
- **Frontend:** HTML5, CSS3, Jinja2 templates, and Bootstrap 5
- **No Client-side JS for core workflows:** All core interactions (bookings, state transitions, updates) are handled via standard HTTP POST requests and form submissions.

## 2. Directory Structure
We will structure the project into modular components using Flask Blueprints:
```text
trekking_app/
│
├── app.py                  # Application entry point, creates app, registers blueprints, initializes DB
├── models.py               # SQLAlchemy Database models
├── decorators.py           # Custom decorators (e.g. role-based access control)
│
├── templates/              # Shared layouts and templates
│   ├── base.html           # Main base template containing Bootstrap navigation and flash messages
│   └── index.html          # Public landing page
│
├── static/                 # Static assets (custom CSS, etc.)
│   └── css/
│       └── custom.css      # Premium custom CSS styling extending Bootstrap
│
├── auth/                   # Blueprint for Authentication (Login, Registration, Logout)
│   ├── routes.py
│   └── templates/auth/
│       ├── login.html
│       ├── register_user.html
│       └── register_staff.html
│
├── admin/                  # Blueprint for Admin dashboard and functionalities
│   ├── routes.py
│   └── templates/admin/
│       ├── dashboard.html
│       ├── manage_treks.html
│       ├── view_bookings.html
│       └── user_management.html
│
├── staff/                  # Blueprint for Trek Staff dashboard and functionalities
│   ├── routes.py
│   └── templates/staff/
│       ├── dashboard.html
│       ├── edit_trek.html
│       └── view_participants.html
│
└── trekker/                # Blueprint for User (Trekker) dashboard and functionalities
    ├── routes.py
    └── templates/trekker/
        ├── dashboard.html
        ├── my_bookings.html
        └── edit_profile.html
```

## 3. Database Schema (SQLite)

We will use Flask-SQLAlchemy to define three main tables:

### User Table (`user`)
Stores user details, authentication credentials, registration approval, and blacklist state.
- `id` (INTEGER, Primary Key)
- `email` (VARCHAR(150), Unique, Not Null)
- `password_hash` (VARCHAR(256), Not Null)
- `role` (VARCHAR(20), Not Null) - One of: `'admin'`, `'staff'`, `'trekker'`
- `name` (VARCHAR(100), Not Null)
- `contact_details` (VARCHAR(200))
- `is_approved` (BOOLEAN, Default: `True`) - Used for Staff approval. Set to `False` for staff upon registration until Admin approves.
- `is_blacklisted` (BOOLEAN, Default: `False`) - If `True`, user is blocked from logging in or accessing any dashboard.

### Trek Table (`trek`)
Stores trekking routes, schedules, capacity, and assignment info.
- `id` (INTEGER, Primary Key)
- `name` (VARCHAR(100), Not Null)
- `location` (VARCHAR(150), Not Null)
- `difficulty` (VARCHAR(20), Not Null) - One of: `'Easy'`, `'Moderate'`, `'Hard'`
- `duration` (INTEGER, Not Null) - Duration of the trek in days.
- `available_slots` (INTEGER, Not Null) - Number of remaining open slots.
- `max_slots` (INTEGER, Not Null) - Maximum capacity of the trek.
- `status` (VARCHAR(20), Default: `'Pending'`) - One of: `'Pending'`, `'Approved'`, `'Open'`, `'Closed'`, `'Completed'`
- `start_date` (DATE, Not Null)
- `end_date` (DATE, Not Null)
- `assigned_staff_id` (INTEGER, ForeignKey('user.id'), Nullable) - Links to the assigned staff member.

### Booking Table (`booking`)
Stores registrations of trekkers onto treks.
- `id` (INTEGER, Primary Key)
- `user_id` (INTEGER, ForeignKey('user.id'), Not Null) - The trekker making the booking.
- `trek_id` (INTEGER, ForeignKey('trek.id'), Not Null) - The booked trek.
- `booking_date` (DATETIME, Default: current timestamp)
- `status` (VARCHAR(20), Default: `'Booked'`) - One of: `'Booked'`, `'Cancelled'`, `'Completed'`

## 4. Key Workflows & Guards

### A. Authentication & Registration
1. **Admin User:** Pre-seeded in the database on initialization (email: `admin@trek.com`, password: `admin123`). No registration route exists for admins.
2. **User (Trekker):** Can self-register. Auto-approved. Can log in immediately.
3. **Trek Staff:** Can self-register. Set to `is_approved = False` on registration. Upon login, if not approved, they are redirected to a landing page stating "Pending Admin Approval" and cannot access the Staff dashboard.
4. **Blacklisted Check:** If a user/staff is blacklisted (`is_blacklisted = True`), login is denied with a descriptive error message. If their status is changed to blacklisted while logged in, the next request will log them out automatically (enforced in `load_user` or a custom request hook).

### B. Access Control
A custom decorator `@role_required(*roles)` will verify:
1. The user is logged in.
2. The user has one of the specified roles.
3. The user is approved (`is_approved == True`).
4. The user is not blacklisted (`is_blacklisted == False`).

If validation fails, the user is redirected to the login page or receives an unauthorized error with a flash message.

### C. Trek Booking & Slot Management (Concurrency & Integrity)
- **Constraint:** Bookings are only allowed if `trek.status == 'Open'` and `trek.available_slots > 0`.
- **Transaction:** When a trekker requests a booking:
  1. Retrieve the trek.
  2. Verify the status is `'Open'` and `available_slots > 0`.
  3. Create the Booking entry.
  4. Decrement the `trek.available_slots` by 1.
  5. Commit the transaction.
- **Trek History:** Trekkers can view all past bookings in their history dashboard, showing `'Booked'`, `'Cancelled'`, or `'Completed'`.

### D. Trek Staff Operations
- **Scope Restriction:** Staff can only view and manage treks they are assigned to.
- **Trek Management:** Staff can update the status of their assigned trek (e.g. from `'Approved'` to `'Open'`, or `'Open'` to `'Closed'`, or mark it as started/completed). They can also edit available slots (cannot exceed `max_slots` or the number of currently booked users).

### E. Admin Operations
- **Approve/Blacklist Staff:** Admin can view pending staff, click "Approve" (sets `is_approved = True`), or "Blacklist"/"Deactivate" (sets `is_blacklisted = True`/`False`).
- **Trek Creation & Staff Assignment:** Admin can add new treks and assign staff members from the list of approved staff.

## 5. UI/UX Design Aesthetics
- Modern, clean layout with Bootstrap 5.
- Glassmorphic card styling, cohesive dark/light blue and teal palette representing outdoors/adventure.
- Responsive table listings, custom badging for trek status (`Open` in green, `Closed` in red, `Pending` in orange, `Completed` in blue).
- Clean forms with built-in HTML5 validation.

## 6. Verification Plan
- **Manual Verification Checklist:**
  - Login as Admin, verify dashboard stats (users, staff, treks, bookings).
  - Create a Trek and assign to a Staff.
  - Register a Staff member, verify they cannot log in/access dashboard until Admin approves.
  - Approve Staff as Admin, log in as Staff, verify dashboard works.
  - Register a Trekker, search for treks, check booking constraints.
  - Book a trek, verify slots decrement.
  - Blacklist a user/staff, verify they are booted from the app and cannot log back in.

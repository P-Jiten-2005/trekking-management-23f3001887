# HikerHub - Trekking Management System

**HikerHub** is a web application that helps manage trekking activities. It allows users to book treks, agencies to organize trips, guides to manage assigned treks, and participants to track their bookings. The system brings all these features together in one place, making trek management easier and more organized.

---

## Key Features

### Admin Suite
- **Global Overview Dashboard**: Quick-glance metrics for total treks, registered trekkers, active staff, and overall bookings.
- **Trek Route Builder**: Add, review, approve, and delete trek events, detailing route length, maximum altitude, and required safety equipment.
- **Staff Assignment Matrix**: Assign approved guides/staff members to specific routes.
- **Chronological Classifications & Sorting**: Treks are automatically categorized into **Past**, **Active**, or **Future** schedules and sorted with the newest/future treks first.
- **User Directory**: View, approve new guide registrations, and whitelist or blacklist/deactivate users & staff members with verification checks.
- **Staff Promotion**: Promote active guides to Administrator status directly.
- **Search Engine**: Search treks and users by names, email addresses, or IDs.
- **Booking Filtering**: Filter bookings by status, trek, or date.

### Trek Staff Portal
- **My Expeditions**: Dashboard listing assigned treks, departure dates, capacity status, and participant headcounts.
- **Trekkers Log**: View contact cards and registration details of participants booked on assigned treks.
- **Capacity Management**: Adjust remaining available slots and toggle trek status (`Pending`, `Approved`, `Open`, `Closed`, `Completed`) with robust capacity validation guards. Staff cannot transition treks back to admin-controlled pending/approved states.

### Trekker (User) Experience
- **Adventure Finder**: Search open treks by keywords or filter routes by difficulty (`Easy`, `Moderate`, `Hard`), viewing specific trek safety equipment requirements, altitudes, and lengths before booking.
- **Atomic Checkout**: Direct booking with automatic slot decrementing, overbooking prevention, and double-booking protection.
- **Expedition History**: Personal ledger tracking active bookings and completed historic treks.
- **Booking Cancellation**: Self-cancel bookings before the trek start date.
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
├── app/                    # Core Application Package
│   ├── __init__.py         # Application Factory (create_app)
│   ├── config.py           # Configuration values
│   ├── decorators.py       # Custom decorator logic (@role_required)
│   ├── extensions.py       # Database & login manager definitions
│   └── models.py           # Database schemas (User, Trek, Booking)
├── routes/                 # Blueprint Route Package
│   ├── __init__.py
│   ├── admin.py            # Admin controllers
│   ├── auth.py             # Auth controllers
│   ├── staff.py            # Staff controllers
│   └── trekker.py          # Trekker search & booking controllers
├── static/                 # Stylesheets, fallback images, and assets
│   ├── css/
│   │   └── custom.css
│   └── images/
│       ├── logo.png
│       └── himalayan_mountains.jpg
├── templates/              # HTML frontend view templates
│   ├── base.html           # Core layout structure
│   ├── index.html          # Public landing portal
│   ├── auth/
│   ├── admin/
│   ├── staff/
│   └── trekker/
├── docs/                   # Development logs, plans, and architectures
│   ├── development/        # Detailed design system and modernization logs
│   └── images/             # Design references and mockups
├── tests/                  # Automated integration tests
│   └── test_app.py
├── app.py                  # Root package runner file
├── requirements.txt        # Dependencies list
├── .gitignore
├── .env.example
├── LICENSE                 # Project License (MIT)
└── README.md
```

---

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/P-Jiten-2005/trekking-management-23f3001887.git
   cd trekking-management-23f3001887
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Project

1. **Start the Flask Application**:
   Running the application will automatically create all SQLite database tables and seed demo data:
   ```bash
   python app.py
   ```

2. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

3. **Seeded Accounts**:

   | Role | Email | Password |
   |------|-------|----------|
   | Admin | `Jiten@trek.com` | `Jiten@123` |
   | Staff | `vyeshwanth@trek.com` | `yesh@1234` |
   | Trekker | `gupta14@gmail.com` | `gupta@123` |

   Three sample treks (Valley of Flowers — Open, Kedarkantha Base Camp — Approved, Chadar Trek — Pending) and a sample booking are also seeded on first run.

---

## Running Tests

To run the automated integration test suite:
```bash
python -m unittest discover -s tests
```

---

## Future Improvements

- **Schedule Overlap Warnings**: Warn administrators during guide assignments if a guide has conflicting schedules on overlapping dates.
- **Payment Gateway Integration**: Replace reservation mocks with a payment checkout flow.
- **Dynamic Altitudes Map**: Embed geospatial maps displaying trek altitude tracks.

---

## Author & License

Developed by **Jiten** and Team. Released under the [MIT License](LICENSE).

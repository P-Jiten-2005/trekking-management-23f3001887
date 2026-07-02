# Design Specification: Dashboard Redesign (Admin & Staff)

This specification details the UI/UX overhaul of the Admin and Staff dashboards to provide a premium, modern, and data-rich interface.

## 1. UX Enhancements

### Admin Dashboard (`admin/routes.py` & `templates/admin/dashboard.html`)
- **Key Metrics Overview**:
  - Four premium gradient cards with custom icons:
    - **Total Treks**: Gradient `linear-gradient(135deg, #1E7A44 0%, #0D4B27 100%)` (Forest Green).
    - **Active Trekkers**: Gradient `linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)` (Ocean Blue).
    - **Trek Guides**: Gradient `linear-gradient(135deg, #0D9488 0%, #0F766E 100%)` (Mountain Teal).
    - **Total Bookings**: Gradient `linear-gradient(135deg, #D97706 0%, #B45309 100%)` (Warm Amber).
- **Recent Activities & Alert Actions**:
  - **Recent Bookings Table**: Display the 5 most recent bookings with user details and date.
  - **Guides Awaiting Approval**: Alert panel showing names of newly registered staff guides who need whitelisting/approval.
  - **Expeditions Schedule**: List of upcoming treks.

### Staff/Guide Dashboard (`staff/routes.py` & `templates/staff/dashboard.html`)
- **Summary Metrics**:
  - **Assigned Treks Count**: Gradient card.
  - **Active Registrations (Hikers Led)**: Count card showing total participants under their care.
  - **Next Departure**: Displaying details of the guide's next upcoming trek.
- **Interactive Expediton Cards / Table**:
  - Redesigned table with high contrast borders, clean margins, and status badges.
  - Quick action links styled as flat outlined interactive buttons.

---

## 2. Visual Theme & Layout (Base & CSS)

- **Navbar**: Styled as a modern glassmorphic container with absolute backdrop blurs and subtle border styling.
- **Gradients & Shadows**: Defined in `static/css/custom.css`.
- **Responsive Stacking**: Seamlessly stacks widgets on mobile screen resolutions.

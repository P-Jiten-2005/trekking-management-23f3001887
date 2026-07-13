# Design Specification: Project Document Alignment & Optional Features

This specification covers additions to the Trekking Management Application to align it fully with all core and recommended functionalities defined in the project syllabus.

---

## 1. Core Feature: Admin Edit Trek

### Route Updates (`routes/admin.py`)
- Add POST action `'edit'` inside `manage_treks()`.
- Inputs: `trek_id`, `name`, `location`, `difficulty`, `duration`, `max_slots`, `available_slots`, `start_date`, `end_date`, `altitude`, `length`, `safety_equipment`, `price`, `image_url`, `status`, and `assigned_staff_id`.
- Guards:
  - Verify dates (`start_date <= end_date`).
  - Verify slots (`available_slots + bookings_count <= max_slots`).
  - Verify positive numeric values.

### Template Updates (`templates/admin/manage_treks.html`)
- Add a modal form `#editModal{{ trek.id }}` for each trek inside the table.
- Pre-populate all fields with current trek details.
- Add an `"Edit"` button under Actions column triggers the modal.

---

## 2. Core Feature: Staff "Started" Trek Status & Bookings Completion

### Status Dropdown (`templates/staff/edit_trek.html` & `templates/admin/manage_treks.html`)
- Add a `<option value="Started">Started</option>` option.
- Allow transition to `'Started'` status in the controllers.

### Booking State Trigger (`routes/staff.py`)
- When a trek is marked `'Completed'`, automatically transition all associated `'Booked'` bookings to `'Completed'` status, updating the participants' trekking history.

---

## 3. Recommended Feature: Charts for Trekking Statistics

### Technology Stack
- Chart.js (included via CDN in `templates/admin/dashboard.html`).

### Data Aggregation
- Pass `chart_labels` (trek names) and `chart_data` (booking counts) from `routes/admin.py` dashboard view to render a bar chart visualization of "Top 5 Popular Treks".

---

## 4. Recommended Feature: REST API Blueprints

### Endpoints (`routes/api.py`)
- `GET /api/treks`: Returns list of all treks with full attributes.
- `GET /api/treks/<id>`: Returns details of a specific trek.
- `GET /api/bookings`: Returns list of all bookings.
- `GET /api/users`: Returns list of users (excluding security fields).

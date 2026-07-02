# Design Specification: Staff Trek Proposals

This specification details the design for allowing approved guides/staff members to propose new treks.

## 1. Workflow
1. **Proposal Phase**:
   - Guide logs into their dashboard.
   - Guide clicks the **"Propose New Trek"** action button.
   - Guide fills in all details: name, location, difficulty, duration, slots, dates, max altitude, length, and required safety gear.
   - On submission, a POST request is sent to `/staff/create_trek`.
   - The trek is created in the database with:
     - `status = 'Pending'`
     - `assigned_staff_id = current_user.id` (auto-assigned to the proposing guide)
   - A success message is flashed, informing the guide that the proposal is awaiting Admin approval.

2. **Approval Phase**:
   - Admin logs into the admin panel (`/admin/treks`).
   - The pending trek proposed by the guide appears in the list showing the guide's name under "Assigned Staff".
   - Admin reviews the trek details and clicks **"Approve"**.
   - The trek status is updated to `'Approved'`, making it open/visible for trekkers once it goes live.

---

## 2. UI Elements

### Staff Dashboard (`templates/staff/dashboard.html`)
- **"Propose New Trek" Button**: Styled as a premium green button at the top header area.
- **Proposal Modal (`#proposeTrekModal`)**:
  - Matches the style of the Admin creation form.
  - Contains fields for name, location, difficulty, duration, slots, start date, end date, max altitude, trek length, and required safety equipment.
  - Submits to `url_for('staff.create_trek')`.

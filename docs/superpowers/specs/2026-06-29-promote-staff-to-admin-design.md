# Design Specification: Promote Staff to Admin

This document outlines the changes needed to add a "Promote to Admin" feature for administrators.

## 1. Requirements
- A logged-in Admin must have the capability to promote any existing approved Trek Staff member to an Admin role.
- Once promoted, the user's role is updated to `'admin'`.
- The user retains their current trek assignments (to be managed manually if needed).
- The option is displayed in the "Users & Staff" management view.
- A confirmation prompt must prevent accidental promotions.

## 2. Changes Proposed

### Backend Controller (`admin/routes.py`)
Add support for a new action `'promote_to_admin'` in the POST handler of the `user_management` route:
```python
elif action == 'promote_to_admin':
    if user.role != 'staff':
        flash('Only staff members can be promoted to Admin.', 'danger')
    else:
        user.role = 'admin'
        user.is_approved = True  # Ensure they remain approved
        db.session.commit()
        flash(f'Staff member {user.name} has been promoted to Admin.', 'success')
```

### UI View (`templates/admin/user_management.html`)
In the table actions column, add a promote button if the user is a staff member and is already approved:
```html
{% if user.role == 'staff' and user.is_approved %}
<form method="POST" action="{{ url_for('admin.user_management') }}" onsubmit="return confirm('Are you sure you want to promote {{ user.name }} to Admin? This action cannot be undone.');" style="display:inline;">
    <input type="hidden" name="user_id" value="{{ user.id }}">
    <input type="hidden" name="action" value="promote_to_admin">
    <button type="submit" class="btn btn-sm btn-outline-warning">Promote to Admin 👑</button>
</form>
{% endif %}
```

### Automated Verification (`test_app.py`)
Add a new unit test method `test_promote_staff_to_admin` in `TrekAppTestCase` to verify database status transitions:
- Create a staff user with `is_approved=True`.
- Query database, fetch them.
- Apply promotion logic (role change, commit).
- Fetch user again and assert `user.role == 'admin'`.

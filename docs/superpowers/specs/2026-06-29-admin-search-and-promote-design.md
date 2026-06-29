# Design Specification: Admin Search Enhancements and Staff Promotion

This specification details the updates to introduce Admin search/sorting markings for treks and users, along with the ability to promote approved Trek Staff to the Admin role.

## 1. Requirements

### A. Staff Promotion
- A logged-in Admin can promote any approved staff member to Admin.
- The action updates the user's role to `'admin'` and keeps their existing trek assignments active.
- Confirmation gate prevents accidental promotions.

### B. Trek Classification and Sorting
- Treks must be classified chronologically based on today's date:
  - **Past Trek**: If the trek end date is before today (`end_date < today`).
  - **Present/Active Trek**: If today is between the start and end dates (`start_date <= today <= end_date`).
  - **Future Trek**: If the trek start date is in the future (`start_date > today`).
- Treks must be sorted by `start_date` in descending order (most future/newest treks first).

### C. User Sorting
- Users in the User & Staff Management view must be sorted alphabetically by `name`.

---

## 2. Code Modifications

### Backend Controller (`admin/routes.py`)
Update routes to include date tracking, sorting queries, and the promotion action handler.
- **Trek Route**:
  ```python
  from datetime import date
  today = date.today()
  # Sorted by start_date DESC
  treks = Trek.query.order_by(Trek.start_date.desc()).all()
  ```
- **User Route**:
  ```python
  # Sort alphabetically
  users = query.order_by(User.name.asc()).all()
  ```
- **Promotion Action**:
  ```python
  elif action == 'promote_to_admin':
      if user.role == 'staff' and user.is_approved:
          user.role = 'admin'
          db.session.commit()
          flash(f'Staff {user.name} promoted to Admin.', 'success')
  ```

### Template Layouts

#### `templates/admin/manage_treks.html`
Add column and badges for chronological classification.
```html
<th>Trek Schedule</th>
...
<td>
    {% if trek.end_date < today %}
    <span class="badge bg-secondary text-white">Past 🕰️</span>
    {% elif trek.start_date <= today and today <= trek.end_date %}
    <span class="badge bg-success text-white">Active 🏃‍♂️</span>
    {% else %}
    <span class="badge bg-info text-dark">Future 📅</span>
    {% endif %}
</td>
```

#### `templates/admin/user_management.html`
Add Promote button under actions for approved staff.
```html
{% if user.role == 'staff' and user.is_approved %}
<form method="POST" action="{{ url_for('admin.user_management') }}" onsubmit="return confirm('Are you sure you want to promote {{ user.name }} to Admin? This action cannot be undone.');" style="display:inline;">
    <input type="hidden" name="user_id" value="{{ user.id }}">
    <input type="hidden" name="action" value="promote_to_admin">
    <button type="submit" class="btn btn-sm btn-outline-warning">Promote to Admin 👑</button>
</form>
{% endif %}
```

---

## 3. Verification Plan

### Unit Test Case (`test_app.py`)
- `test_promote_staff_to_admin`: Verify that submitting the promotion request modifies a user's role to `'admin'`.
- `test_trek_sorting_by_date`: Verify that treks query results are ordered by `start_date` descending.

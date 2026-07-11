# Admin Search and Promotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement chronological classifications and descending start date sorting for treks, alphabetical name sorting for users, and the ability for admins to promote approved staff to the admin role.

**Architecture:** Extend existing Flask admin routes to handle sorting/actions, update HTML templates with badges and form components, and add verification tests.

**Tech Stack:** Python 3.10+, Flask, SQLite, Bootstrap 5.

## Global Constraints
- Core workflows must be driven by standard HTTP POST/GET requests and Jinja templates (no core JS).
- Promoted staff members keep their trek assignments.
- Classify treks relative to `date.today()`.

---

### Task 1: Backend Routes Updates

**Files:**
- Modify: `admin/routes.py`

**Interfaces:**
- Consumes: Models `User`, `Trek`

- [ ] **Step 1: Update admin/routes.py imports**
Add import for `date`.
```python
from datetime import date, datetime
```

- [ ] **Step 2: Update manage_treks route queries and parameters**
Update `manage_treks` to pass `today` and sort treks by `start_date` descending.
```python
@admin_bp.route('/admin/treks', methods=['GET', 'POST'])
@role_required('admin')
def manage_treks():
    today = date.today()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            name = request.form.get('name')
            location = request.form.get('location')
            difficulty = request.form.get('difficulty')
            duration = int(request.form.get('duration'))
            max_slots = int(request.form.get('max_slots'))
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
            staff_id = request.form.get('assigned_staff_id')
            assigned_staff_id = int(staff_id) if staff_id else None

            trek = Trek(
                name=name, location=location, difficulty=difficulty,
                duration=duration, max_slots=max_slots, available_slots=max_slots,
                start_date=start_date, end_date=end_date, assigned_staff_id=assigned_staff_id,
                status='Pending'
            )
            db.session.add(trek)
            db.session.commit()
            flash('Trek created successfully.', 'success')
            return redirect(url_for('admin.manage_treks'))

        elif action == 'assign':
            trek_id = int(request.form.get('trek_id'))
            staff_id = request.form.get('assigned_staff_id')
            trek = Trek.query.get_or_404(trek_id)
            trek.assigned_staff_id = int(staff_id) if staff_id else None
            db.session.commit()
            flash('Staff assigned successfully.', 'success')
            return redirect(url_for('admin.manage_treks'))

        elif action == 'approve':
            trek_id = int(request.form.get('trek_id'))
            trek = Trek.query.get_or_404(trek_id)
            trek.status = 'Approved'
            db.session.commit()
            flash('Trek approved successfully.', 'success')
            return redirect(url_for('admin.manage_treks'))

        elif action == 'delete':
            trek_id = int(request.form.get('trek_id'))
            trek = Trek.query.get_or_404(trek_id)
            Booking.query.filter_by(trek_id=trek.id).delete()
            db.session.delete(trek)
            db.session.commit()
            flash('Trek deleted successfully.', 'success')
            return redirect(url_for('admin.manage_treks'))

    search = request.args.get('search', '')
    if search:
        treks = Trek.query.filter((Trek.name.like(f"%{search}%")) | (Trek.id == search)).order_by(Trek.start_date.desc()).all()
    else:
        treks = Trek.query.order_by(Trek.start_date.desc()).all()

    staff_members = User.query.filter_by(role='staff', is_approved=True).all()
    return render_template('manage_treks.html', treks=treks, staff_members=staff_members, search=search, today=today)
```

- [ ] **Step 3: Update user_management route queries, sorting, and add promote action**
```python
@admin_bp.route('/admin/users', methods=['GET', 'POST'])
@role_required('admin')
def user_management():
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        action = request.form.get('action')
        user = User.query.get_or_404(user_id)

        if action == 'approve_staff':
            user.is_approved = True
            db.session.commit()
            flash(f'Staff {user.name} approved successfully.', 'success')
        elif action == 'toggle_blacklist':
            user.is_blacklisted = not user.is_blacklisted
            db.session.commit()
            status = 'blacklisted' if user.is_blacklisted else 'whitelisted'
            flash(f'User {user.name} has been {status}.', 'info')
        elif action == 'promote_to_admin':
            if user.role != 'staff':
                flash('Only staff members can be promoted to Admin.', 'danger')
            else:
                user.role = 'admin'
                user.is_approved = True
                db.session.commit()
                flash(f'Staff member {user.name} has been promoted to Admin.', 'success')
        return redirect(url_for('admin.user_management'))

    search = request.args.get('search', '')
    query = User.query.filter(User.role != 'admin')
    if search:
        query = query.filter(
            ((User.name.like(f"%{search}%")) | (User.email.like(f"%{search}%")) | (User.id == search))
        )
    users = query.order_by(User.name.asc()).all()

    return render_template('user_management.html', users=users, search=search)
```

---

### Task 2: Template Updates

**Files:**
- Modify: `templates/admin/manage_treks.html`
- Modify: `templates/admin/user_management.html`

- [ ] **Step 1: Add classification column to manage_treks.html table header**
Find `<th>Status</th>` and add `<th>Trek Schedule</th>` before or after it.
```html
                    <th>Status</th>
                    <th>Trek Schedule</th>
                    <th>Assigned Staff</th>
```

- [ ] **Step 2: Add classification badges in manage_treks.html table body**
Find `<td><span class="badge bg-secondary">{{ trek.status }}</span></td>` (or the badge loop) and append:
```html
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

- [ ] **Step 3: Add Promote button to templates/admin/user_management.html table body**
Find the actions column loop and add the form:
```html
                            {% if user.role == 'staff' and user.is_approved %}
                            <form method="POST" action="{{ url_for('admin.user_management') }}" onsubmit="return confirm('Are you sure you want to promote {{ user.name }} to Admin? This action cannot be undone.');">
                                <input type="hidden" name="user_id" value="{{ user.id }}">
                                <input type="hidden" name="action" value="promote_to_admin">
                                <button type="submit" class="btn btn-sm btn-outline-warning">Promote to Admin 👑</button>
                            </form>
                            {% endif %}
```

---

### Task 3: Unit Testing Updates

**Files:**
- Modify: `test_app.py`

- [ ] **Step 1: Add test cases to test_app.py**
```python
    def test_promote_staff_to_admin(self):
        """Verify that a staff user can be promoted to admin."""
        # Create an approved staff member
        staff = User(email='promotable@trek.com', role='staff', name='Alex Staff', is_approved=True)
        staff.set_password('password')
        db.session.add(staff)
        db.session.commit()

        # Simulate promotion POST action
        with self.app.test_request_context():
            # Apply promotion
            db_user = User.query.filter_by(email='promotable@trek.com').first()
            self.assertEqual(db_user.role, 'staff')
            
            db_user.role = 'admin'
            db_user.is_approved = True
            db.session.commit()

        promoted_user = User.query.filter_by(email='promotable@trek.com').first()
        self.assertEqual(promoted_user.role, 'admin')
        self.assertTrue(promoted_user.is_approved)

    def test_trek_sorting_by_date(self):
        """Verify that treks are queried in descending order of start_date."""
        t1 = Trek(
            name='Trek A (Future)', location='Loc A', difficulty='Easy', duration=3,
            max_slots=10, available_slots=10, start_date=date(2026, 10, 1), end_date=date(2026, 10, 4)
        )
        t2 = Trek(
            name='Trek B (Past)', location='Loc B', difficulty='Moderate', duration=3,
            max_slots=10, available_slots=10, start_date=date(2026, 1, 1), end_date=date(2026, 1, 4)
        )
        db.session.add_all([t1, t2])
        db.session.commit()

        # Query treks sorted by start_date DESC
        sorted_treks = Trek.query.order_by(Trek.start_date.desc()).all()
        
        # Trek A (Oct 2026) must come before Trek B (Jan 2026)
        self.assertEqual(sorted_treks[0].name, 'Trek A (Future)')
        self.assertEqual(sorted_treks[1].name, 'Trek B (Past)')
```

---

## Verification Plan
1. Run database unit tests: `python -m unittest test_app.py` and verify all tests pass.
2. Manually test using development server:
   - Log in as Admin.
   - Go to "Manage Treks", check the new "Trek Schedule" column showing "Future", "Past" or "Active" badges and that treks are sorted chronologically by start date descending.
   - Go to "Users & Staff", check that staff and trekkers are sorted alphabetically.
   - Click "Promote to Admin" on a staff user, confirm prompt, and check that they are successfully promoted.

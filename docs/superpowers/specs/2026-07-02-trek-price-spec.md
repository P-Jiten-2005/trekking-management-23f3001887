# Design Specification: Trek Price Integration

This specification details the design for adding a price (in INR, represented with ₹) to each trek.

## 1. Database Schema
- **Trek Model (`models.py`)**:
  - Add `price` column: `db.Column(db.Float, nullable=True)` to support decimal values for pricing.

---

## 2. UI Elements

### Admin Manage Treks (`templates/admin/manage_treks.html`)
- **Create Trek Form Modal**:
  - Add input field for **Price (INR)**:
    `<input type="number" name="price" step="1" class="form-control" placeholder="e.g. 8500" required>`
- **Treks Table**:
  - Display price under the trek name or location details.
    `₹{{ "%.2f"|format(trek.price) if trek.price else '0.00' }}`

### Staff Dashboard (`templates/staff/dashboard.html`)
- **Propose Trek Form Modal**:
  - Add input field for **Price (INR)**.
- **Treks Table**:
  - Display price for each assigned/proposed trek.

### Trekker Find Treks (`templates/trekker/dashboard.html`)
- **Trek Cards**:
  - Display the price prominently in the card footer next to the dates.
    `<span class="fs-5 fw-bold text-success">Price: ₹{{ "%.2f"|format(trek.price) if trek.price else '0.00' }}</span>`

### Booking History Lists (`my_bookings.html` and `view_bookings.html`)
- Add a new **Price** column displaying the value.

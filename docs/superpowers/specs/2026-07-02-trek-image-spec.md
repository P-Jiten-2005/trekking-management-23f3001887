# Design Specification: Trek Visual Images

This specification details the design for adding image cover pictures to treks.

## 1. Database Schema
- **Trek Model (`models.py`)**:
  - Add `image_url` column: `db.Column(db.String(500), nullable=True)` to store image hyperlinks or local static paths.

---

## 2. UI Elements

### Trekker Find Treks (`templates/trekker/dashboard.html`)
- **Trek Cards**:
  - Add a cover image `<img class="card-img-top" style="height: 200px; object-fit: cover;">` at the top of each card.
  - Fall back to `/static/images/himalayan_mountains.jpg` if no image URL is specified.

### Lists and booking logs
- Display a small `40px x 40px` rounded thumbnail next to the Trek name in:
  - Admin Trek Management table (`manage_treks.html`)
  - Staff Dashboard assigned treks table (`dashboard.html`)
  - Trekker My Bookings table (`my_bookings.html`)
  - Admin bookings log (`view_bookings.html`)

### Create and Proposal Modals
- Add a new text input field for **Image URL (Optional)** with help text explaining that leaving it blank uses the default mountain visual.

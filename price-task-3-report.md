# Task 3: Trek Price Templates Implementation Report

This report outlines the changes made to the templates to display and input price amounts for treks across all dashboards and booking ledgers.

## Modified Files and Changes

### 1. `templates/admin/manage_treks.html`
- **Create New Trek Modal**: Added a new numeric field `price` with a step of `0.01` under the Safety Equipment section to allow administrators to set a price when creating new treks.
- **Trek Table Row**: Appended the price information (formatted in INR with currency symbol `₹`) to the small text showing max altitude and length.

### 2. `templates/staff/dashboard.html`
- **Propose New Trek Modal**: Added the `price` input field below safety equipment.
- **Assigned Treks Table**: Included the price column display in the metadata list for each trek row.

### 3. `templates/trekker/dashboard.html`
- **Trek Card**: Displayed the trek price above the trek dates so that trekkers can see the cost before booking.

### 4. `templates/trekker/my_bookings.html`
- **Bookings Table**: Added a `Price` column header and populated it with the price of the booked trek in each row. Also adjusted table colspan to 8 for empty states.

### 5. `templates/admin/view_bookings.html`
- **All Bookings Table**: Added a `Price` column header and cell data next to the Trek Name to show the price of the booking. Adjusted table colspan to 7 for empty states.

## Verification
- Verified that all modified templates compile and render correctly.

# Design Specification: Dashboard Modernization

This specification outlines the visual modernization of the HikerHub / Eco-Hikes dashboards using the newly established design tokens, shifting them from template-like elements to a premium SaaS aesthetic.

---

## 1. Metric Cards Modernization
- **Legacy Rainbow Backgrounds**: Saturated gradients (`bg-grad-forest`, `bg-grad-ocean`, `bg-grad-teal`, `bg-grad-amber`) are completely removed.
- **New Appearance (`.metric-card-modern`)**:
  - Background: White (`#ffffff`).
  - Border: `1px solid var(--neutral-border)`.
  - Accent Indicator: `4px solid var(--brand-primary)` top border.
  - Border-Radius: `var(--radius-card)` (`12px`).
  - Elevation: Soft shadow `var(--shadow-base)`.
  - Hover elevation: Slight upward shift (`translateY(-4px)`) and active shadow `var(--shadow-hover)`.

---

## 2. Table Component Refinement
- **Table Container (`.table-modern`)**: Rounded border-radius (`var(--radius-table)`), white backgrounds, and light borders (`var(--neutral-border)`).
- **Table Headers**: Uppercase, slate gray text, and semi-bold weights (`var(--font-weight-semibold)`).
- **Row Styling**: Alternating clean rows, soft gray row hover states (`#f1f5f9`), and padded columns (`16px 20px`).

---

## 3. Empty States Redesign
- Standardize all blank list tables to display illustrated empty container layouts containing:
  - Centered visual indicators (Bootstrap Icons).
  - Explicit header subheadings (e.g. "No bookings yet.").
  - Descriptive paragraph details.

---

## 4. Spacing, Typography, and Background Adjustments
- **Background**: Replaces the linear body background with a subtle, neutral off-white green-tinted shade (`#f4f6f4`).
- **Standardized Buttons**: All dashboard primary actions map to `--brand-primary` (`#0f5132`) with hover translation lifts. All secondary buttons utilize consistent border radii (`6px`).

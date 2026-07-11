# Design Specification: Integrate Brand Logo Image

This design specification details the integration of the brand logo asset (`Logo.png`) across navigation headers and authentication pages.

---

## 1. Asset Storage
- **Source**: `D:\Jiten\Trek\Logo.png`
- **Static path**: `D:\Jiten\Trek\static\images\Logo.png`
- **Format**: Portable Network Graphics (PNG)

---

## 2. Branding Display Guidelines

### Navigation Menus
- **Location**: Top-left corner of the navbar in `templates/base.html` and `templates/index.html`.
- **Styling**: Rendered using a responsive `<img>` element with `height="32"` (base layout) or `height="36"` (landing page layout) aligned horizontally alongside the brand name text.

### Authentication Portals
- **Location**: Positioned centrally above the card header block inside `/login` and `/register` templates.
- **Styling**: Rendered using an `<img>` element with `height="60"` and margin space `class="mb-3 d-block mx-auto"` to maintain symmetry.

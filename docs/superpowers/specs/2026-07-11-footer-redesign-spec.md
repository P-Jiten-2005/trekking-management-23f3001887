# Design Specification: Footer Redesign

This design specification outlines the redesign of the footer component on the Eco-Hikes website.

---

## 1. Objectives
- Replace the legacy footer block (`© 2026 Eco-Hikes. All rights reserved. Powered by HikerHub System`) with a modern, high-quality component.
- Integrate Contact Us section on the left and developer/project buttons on the right.
- Enforce full mobile responsiveness and accessibility constraints.

---

## 2. Layout Structure

### Desktop Layout (`>= 768px`)
- **Grid Layout**: Two-column partition (`.col-md-7` left, `.col-md-5` right).
- **Left Column**: "Contact Us" heading and three list items (Email, Mobile, Instagram) with Bootstrap icons and distinct labels.
- **Right Column**: Action buttons (GitHub, Project Document) aligned horizontally and vertically centered inside the footer block.

### Mobile Layout (`< 768px`)
- Stacks all columns vertically.
- Left column information remains left-aligned.
- Right column action buttons align to the left, wrapping naturally or stacking.

---

## 3. Style and Interactive States

### Color Palette
- **Background**: `#12260c` (deep forest green matching Eco-Hikes).
- **Text & Labels**: Active text elements display white (`#ffffff`); secondary labels display slate/muted tones.

### Icons
- Mail: `bi bi-envelope-fill`
- Phone: `bi bi-telephone-fill`
- Instagram: `bi bi-instagram`
- GitHub: `bi bi-github`
- File/Document: `bi bi-file-earmark-text-fill`

### Action Buttons (`.btn-footer`)
- **Default State**: Semi-transparent white backdrop (`rgba(255, 255, 255, 0.05)`), light border, and soft white text.
- **Hover State**: Elevates slightly (`translateY(-2px)`), solid forest green background (`#1E7A44`), and a soft green glow drop shadow (`box-shadow`).
- **Focus State**: Renders a visible green focus accent ring.

# Design Specification: Global Design System

This design specification details the declaration of custom design tokens in the HikerHub styling architecture. All variables are declared inside the `:root` block of `static/css/custom.css` to facilitate centralized, reusable design values.

---

## 1. Brand & Neutral Color Palettes
- **`--brand-primary`**: `#0f5132` (Primary dark forest green brand identity).
- **`--brand-secondary`**: `#2b4c1e` (Muted accent forest green).
- **`--neutral-dark`**: `#1e293b` (Slate blue-grey color for primary text elements).
- **`--neutral-light`**: `#f8fafc` (Off-white for background layers).
- **`--neutral-border`**: `#e2e8f0` (Soft slate border line color).

---

## 2. Semantic Color Scale
- **`--color-success`**: `#1e7a44` (Confirmed or successful states).
- **`--color-warning`**: `#d97706` (Alert, attention, or pending states).
- **`--color-danger`**: `#d9383a` (Error, delete, past, or cancelled states).

---

## 3. Typography Scale
- **`--font-family-base`**: `'Outfit', system-ui, sans-serif`
- **`--font-size-title`**: `2rem` (Main headings)
- **`--font-size-section`**: `1.5rem` (Subheadings)
- **`--font-size-card`**: `1.15rem` (Card heading blocks)
- **`--font-size-table-head`**: `0.85rem` (Uppercase table column titles)
- **`--font-size-body`**: `0.95rem` (Regular paragraph body text)
- **`--font-size-label`**: `0.85rem` (Form label tags)
- **`--font-size-caption`**: `0.8rem` (Footnotes and minor grey subtext elements)
- **`--font-weight-regular`**: `400`
- **`--font-weight-semibold`**: `600`
- **`--font-weight-bold`**: `700`

---

## 4. Spacing Scale (Geometric)
- **`--spacing-xxs`**: `4px`
- **`--spacing-xs`**: `8px`
- **`--spacing-sm`**: `12px`
- **`--spacing-md`**: `16px`
- **`--spacing-lg`**: `24px`
- **`--spacing-xl`**: `32px`
- **`--spacing-xxl`**: `48px`

---

## 5. Border Radius, Shadows, and Transition Durations
- **Border Radii**:
  - Cards: `12px` (`--radius-card`)
  - Buttons / Inputs: `6px` (`--radius-button` / `--radius-input`)
  - Tables: `12px` (`--radius-table`)
  - Modals / Dialogs: `16px` (`--radius-dialog`)
  - Badges: `100px` (`--radius-badge`)
- **Shadows**:
  - Base: `0 1px 3px rgba(0,0,0,0.05)` (`--shadow-base`)
  - Hover: `0 8px 20px rgba(0,0,0,0.08)` (`--shadow-hover`)
  - Modal overlay: `0 20px 25px -5px rgba(0,0,0,0.1)` (`--shadow-overlay`)
- **Transitions**:
  - Fast: `0.15s` (`--transition-fast`)
  - Normal: `0.2s` (`--transition-normal`)
  - Slow: `0.3s` (`--transition-slow`)
  - Elastic/Bounce: `0.25s cubic-bezier(0.4, 0, 0.2, 1)` (`--transition-bounce`)

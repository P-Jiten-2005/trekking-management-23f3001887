# Design Specification: Landing Page Treks Showcase & Visual Card Redesign

This specification outlines the visual redesign of the trek presentation cards (based on the provided `reference image .png`) and the integration of a featured treks showcase section directly on the application landing page.

---

## 1. Visual Card Specification

### Card Layout
- **Container**: Elevated borderless card with soft rounded corners (`border-radius: 16px`) and subtle drop-shadows.
- **Hover Effects**: Micro-scale up transition (`transform: translateY(-5px)`) and deeper box shadow state for premium interaction.

### Image Header
- **Aspect Ratio**: Rectangular aspect ratio, height fixed to `260px` with `object-fit: cover`.
- **Top-Left Ribbon Overlay**:
  - Absolute positioning (`top: 12px; left: 12px;`).
  - Crimson red color `#D9383A`.
  - Non-rounded rectangle look matching the reference image.
  - Content: `"Best Seller"` or `"Trending"` based on trek attributes.
- **Bottom Metadata Text Overlay**:
  - Absolute positioning (`bottom: 12px; left: 16px; right: 16px;`).
  - Text color: Solid white with drop-shadow or overlay mask.
  - Left content: Duration format (`5D | 4N` representing Days and Nights).
  - Right content: Difficulty badge text (e.g. `Easy`).
  - Gradient underlay: Bottom-anchored dark linear gradient (`rgba(0, 0, 0, 0.7) -> transparent`) for text legibility.

### Card Body Details
- **Trek Name**: Centered, wine red / maroon text color (`#8B1E3F`), bold, clean spacing.
- **Card Footer Row**:
  - Flex layout (`justify-content: space-between; align-items: center;`).
  - Left: Star rating indicator with reviews count, e.g., `⭐ 5 | 12`.
  - Right: Wine red underlined link `"View Details"` that launches the specification details modal.

---

## 2. Interactive Details Modal (`#trekModal<id>`)
- Launched by clicking `"View Details"` on any trek card (both landing page and trekker dashboard).
- **Modal Header**: Display trek name and difficulty.
- **Modal Body**: Grid layout showing:
  - Location, start and end dates.
  - Price (in INR `₹`), available slots.
  - Altitudes, length, safety equipment checklist.
- **Modal Footer Action**:
  - A green confirmation button.
  - If authenticated as Trekker: renders `"Book Now"` submitting the booking action.
  - If guest: redirects to login.

---

## 3. Landing Page Showcase Section
- Embedded in `templates/index.html` as `"Explore Our Featured Treks"` right after the "What We Do" section.
- Fetches the top 3 approved/open treks from `app.py`.

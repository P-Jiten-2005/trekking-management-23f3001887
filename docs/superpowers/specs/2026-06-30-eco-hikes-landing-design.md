# Design Specification: Eco-Hikes Landing Page

This specification details the updates to create a public landing page at `templates/index.html` featuring a custom header and a full-screen Himalayan hero background.

## 1. Requirements

- **Sticky Navigation Bar**:
  - Fixed at the top (`sticky-top` or `fixed-top`).
  - Transparent background with dark text. On hover or scroll, it remains readable.
  - Left side: Logo text "Eco-Hikes".
  - Right side: Nav links for "What We Do", "Get Involved", "About".
  - Hamburger menu for mobile scaling.
- **Hero Section**:
  - Full-screen height (`100vh`).
  - Background image: `/static/images/himalayan_mountains.jpg` with a dark overlay (`rgba(0, 0, 0, 0.4)`) to ensure high text contrast.
  - Text color: White.
  - Headline: "Your next adventure starts with the right community" (large, bold).
  - Subheadline: "See the people, places and culture of the Mountains with us." (medium weight).
- **Core Sections**:
  - **What We Do**: Card layout detailing our trekking community values.
  - **Get Involved**: Interactive call-to-action block with buttons linking to register/login pages.
  - **About**: Description of the Eco-Hikes project.
- **Mobile Responsiveness**: Text scales down, columns collapse to stacks, and navigation menu collapses to a hamburger toggler.

---

## 2. Technical Strategy

### Template File (`templates/index.html`)
The landing page will be built as a standalone HTML page to avoid inheriting the dark dashboard header from `base.html`.
- It will load Bootstrap 5 and the custom CSS stylesheet.
- Visual elements are structured in responsive sections.

### Styling Updates (`static/css/custom.css`)
Add layout variables and styles to handle:
- Transparent navigation bars.
- Full-screen hero section with centered content.
- Smooth scroll navigation:
  ```css
  html {
      scroll-behavior: smooth;
  }
  ```

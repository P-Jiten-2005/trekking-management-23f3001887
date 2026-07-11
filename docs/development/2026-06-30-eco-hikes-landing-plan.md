# Eco-Hikes Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a fully responsive, modern website landing page at `/` (in `templates/index.html`) with a sticky transparent navbar and a full-screen Himalayan hero background.

---

### Task 1: Styling Updates

**Files:**
- Modify: `static/css/custom.css`

- [ ] **Step 1: Add landing page custom styles**
Append the following classes for the transparent navbar, smooth scrolling, and full-screen hero image overlay to `static/css/custom.css`:
```css
/* Smooth Scroll */
html {
    scroll-behavior: smooth;
}

/* Landing Navbar */
.landing-nav {
    transition: background-color 0.3s ease, box-shadow 0.3s ease;
    background-color: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(10px);
}

.landing-nav .navbar-brand {
    font-weight: 700;
    color: #1a330e !important;
}

.landing-nav .nav-link {
    color: #2b4c1e !important;
    font-weight: 600;
}

.landing-nav .nav-link:hover {
    color: #7ba662 !important;
}

/* Hero Section */
.hero-section {
    position: relative;
    height: 100vh;
    background: url('/static/images/himalayan_mountains.jpg') no-repeat center center/cover;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    text-align: center;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(18, 38, 12, 0.45); /* Dark forest overlay */
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    padding: 20px;
}

.hero-content h1 {
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 20px;
    text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.hero-content p {
    font-size: 1.5rem;
    font-weight: 400;
    margin-bottom: 35px;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

/* responsive hero scaling */
@media (max-width: 768px) {
    .hero-content h1 {
        font-size: 2.2rem;
    }
    .hero-content p {
        font-size: 1.1rem;
    }
}
```

---

### Task 2: Landing Page Template Creation

**Files:**
- Modify: `templates/index.html`

- [ ] **Step 1: Replace templates/index.html with the custom standalone page layout**
Replace the entire content of `templates/index.html` with:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eco-Hikes - Your Adventure Community</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
</head>
<body>

    <!-- Sticky Transparent Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light fixed-top landing-nav shadow-sm">
        <div class="container">
            <a class="navbar-brand fs-3" href="#hero">Eco-Hikes 🏔️</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#landingNavbar">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="landingNavbar">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item"><a class="nav-link px-3" href="#what-we-do">What We Do</a></li>
                    <li class="nav-item"><a class="nav-link px-3" href="#get-involved">Get Involved</a></li>
                    <li class="nav-item"><a class="nav-link px-3" href="#about">About</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Full-screen Hero Section -->
    <section id="hero" class="hero-section">
        <div class="hero-overlay"></div>
        <div class="hero-content container">
            <h1 class="display-3">Your next adventure starts with the right community</h1>
            <p class="lead">See the people, places and culture of the Mountains with us.</p>
            <div class="d-flex justify-content-center gap-3 flex-wrap">
                <a href="#what-we-do" class="btn btn-light btn-lg px-4 py-3 shadow">Explore More</a>
                <a href="#get-involved" class="btn btn-success btn-lg px-4 py-3 shadow">Join Us</a>
            </div>
        </div>
    </section>

    <!-- What We Do Section -->
    <section id="what-we-do" class="py-5 bg-white">
        <div class="container py-5">
            <div class="text-center mb-5">
                <span class="badge bg-success-subtle text-success px-3 py-2 mb-2 fs-6">Core Mission</span>
                <h2 class="display-5 fw-bold text-dark">What We Do</h2>
                <p class="text-muted col-md-8 mx-auto mt-2">We build connections between passionate hikers and the local communities in the mountains. We design sustainable hiking tours that respect nature and support local cultures.</p>
            </div>
            <div class="row g-4 mt-4">
                <div class="col-md-4 text-center">
                    <div class="p-4 rounded-4 shadow-sm border border-light h-100">
                        <span class="fs-1 mb-3 d-block">🥾</span>
                        <h4 class="fw-bold">Curated Trails</h4>
                        <p class="text-muted">Unique routes tailored for various experience levels, ensuring both safety and adventure.</p>
                    </div>
                </div>
                <div class="col-md-4 text-center">
                    <div class="p-4 rounded-4 shadow-sm border border-light h-100">
                        <span class="fs-1 mb-3 d-block">🤝</span>
                        <h4 class="fw-bold">Community First</h4>
                        <p class="text-muted">Direct interactions with native guides and overnight stays in mountain communities.</p>
                    </div>
                </div>
                <div class="col-md-4 text-center">
                    <div class="p-4 rounded-4 shadow-sm border border-light h-100">
                        <span class="fs-1 mb-3 d-block">🌿</span>
                        <h4 class="fw-bold">Eco Conservation</h4>
                        <p class="text-muted">Low-impact travel practices aimed at keeping the mountains clean and conserving their beauty.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Get Involved Section -->
    <section id="get-involved" class="py-5 bg-light">
        <div class="container py-5">
            <div class="text-center mb-5">
                <span class="badge bg-success-subtle text-success px-3 py-2 mb-2 fs-6">Take Action</span>
                <h2 class="display-5 fw-bold text-dark">Get Involved</h2>
                <p class="text-muted col-md-8 mx-auto mt-2">Become a part of Eco-Hikes. Register to explore routes, or join as staff to guide travelers through the trails.</p>
            </div>
            
            {% if current_user.is_authenticated %}
                <div class="text-center py-4 bg-white rounded-4 shadow-sm col-md-6 mx-auto">
                    <h5 class="mb-3 fw-bold">Welcome back, {{ current_user.name }}!</h5>
                    {% if current_user.role == 'admin' %}
                        <a href="{{ url_for('admin.dashboard') }}" class="btn btn-success btn-lg shadow-sm">Go to Admin Dashboard</a>
                    {% elif current_user.role == 'staff' %}
                        <a href="{{ url_for('staff.dashboard') }}" class="btn btn-primary btn-lg shadow-sm">Go to Staff Dashboard</a>
                    {% else %}
                        <a href="{{ url_for('trekker.dashboard') }}" class="btn btn-success btn-lg shadow-sm">Go to Trekker Dashboard</a>
                    {% endif %}
                </div>
            {% else %}
                <div class="row g-4 justify-content-center mt-3">
                    <div class="col-md-5">
                        <div class="card border-0 shadow-sm p-4 h-100 rounded-4 text-center">
                            <span class="fs-1 mb-2">🏕️</span>
                            <h4 class="fw-bold">For Trekkers</h4>
                            <p class="text-muted flex-grow-1">Book open treks, manage registrations, and discover new peaks.</p>
                            <div class="d-grid gap-2">
                                <a href="{{ url_for('auth.register_trekker') }}" class="btn btn-success py-2 shadow-sm">Register as Trekker</a>
                                <a href="{{ url_for('auth.login') }}" class="btn btn-outline-success py-2">Log In</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-5">
                        <div class="card border-0 shadow-sm p-4 h-100 rounded-4 text-center">
                            <span class="fs-1 mb-2">🏔️</span>
                            <h4 class="fw-bold">For Trek Staff</h4>
                            <p class="text-muted flex-grow-1">Manage assigned treks, view participants lists, and update capacities.</p>
                            <div class="d-grid gap-2">
                                <a href="{{ url_for('auth.register_staff') }}" class="btn btn-primary py-2 shadow-sm">Register as Staff</a>
                                <a href="{{ url_for('auth.login') }}" class="btn btn-outline-primary py-2">Log In</a>
                            </div>
                        </div>
                    </div>
                </div>
            {% endif %}
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-5 bg-white">
        <div class="container py-5 text-center">
            <span class="badge bg-success-subtle text-success px-3 py-2 mb-2 fs-6">Our Story</span>
            <h2 class="display-5 fw-bold text-dark mb-4">About Eco-Hikes</h2>
            <p class="lead text-muted col-md-8 mx-auto">Eco-Hikes was founded to change the way we experience mountain tourism. By emphasizing environmental awareness and direct support for mountain communities, we build trips that are meaningful, sustainable, and unforgettable.</p>
            <div class="mt-5">
                <span class="fs-3 text-success mx-2">🌲</span>
                <span class="fs-3 text-success mx-2">🥾</span>
                <span class="fs-3 text-success mx-2">🗻</span>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-4 bg-dark text-white-50 text-center">
        <div class="container">
            <p class="mb-1">&copy; 2026 Eco-Hikes. All rights reserved.</p>
            <small>Powered by HikerHub System</small>
        </div>
    </footer>

    <!-- Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## Verification Plan
1. Start the Flask server: `python app.py`.
2. Navigate to `http://127.0.0.1:5000` in the browser.
3. Validate visual layout:
   - Sticky navbar at the top with "Eco-Hikes" branding.
   - Full-screen hero section displaying the cloud-covered Himalayan mountains.
   - Check mobile layout scalability and check hamburger menu collapse.

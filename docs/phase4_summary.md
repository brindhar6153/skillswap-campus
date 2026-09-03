# Phase 4 Summary: Frontend Development

This document outlines the frontend assets and features implemented for the **SkillSwap Campus** project.

---

## 1. Files Created

### 1.1 HTML Templates (`frontend/`)
* **`index.html`**: Marketing landing page featuring a value proposition, call-to-actions, Time Bank explanation, feature cards, and footer links.
* **`pages/login.html`**: Verified student sign-in card layout with email and password input structures.
* **`pages/register.html`**: Student account signup with fields for Name, email domain matching, Course Major, and password checks.
* **`pages/dashboard.html`**: Dynamic homepage with balance metrics, suggested swaps, incoming/sent invite lists, upcoming calendar items, and transaction histories.
* **`pages/profile.html`**: Detail profile card displaying biography, skills offered/wanted, weekly availability slots, rating reviews, and an interactive Edit Profile details modal.
* **`pages/skills.html`**: Form layout to declare teaching/learning portfolios with interactive category and level dropdown selectors.
* **`pages/requests.html`**: Proposals tracking interface supporting mock actions for acceptances, declines, and cancellations.
* **`pages/sessions.html`**: Booking supervisor page showing scheduled hours and past history, with double-blind review score submission dialogs.

### 1.2 Stylesheets (`frontend/css/`)
* **`style.css`**: Global design variables, clean resets, typography, navigation bars, utility classes, badges, cards, and footers.
* **`auth.css`**: Auth-specific form layouts, validation triggers, alert blocks, and card alignments.
* **`dashboard.css`**: Dashboard grid structures, sidebar avatars, credit value displays, list items, and responsiveness breakpoints.

### 1.3 JavaScript Foundations (`frontend/js/`)
* **`main.js`**: Controls mobile drawer hamburger toggles, binds global active page links, manages session state routing logic, and handles logouts.
* **`auth.js`**: Enforces frontend email formats, password validation rules, and saves mock student registration records to `localStorage` on successful submits.
* **`api.js`**: A reusable fetch API wrapper providing `.get()`, `.post()`, `.put()`, and `.delete()` HTTP methods pointing to a configured `API_BASE_URL`.

---

## 2. Frontend Features Completed

1. **Responsive Header & Footer Navigation**: Universal mobile-responsive header and footer layout that scales smoothly down to mobile viewport dimensions.
2. **Form Validation Checks**: Client-side validation triggers checking email domain endings (`.edu`), password lengths, and matching values.
3. **Mock Auth Session Routing**: Successful registration/login updates `localStorage` credentials and redirects to the dynamic dashboard. Logging out clears memory and redirects home.
4. **Mock Dynamic Data Rendering**: The dashboard and profile pages automatically read profile names, majors, and bios from the simulated session state.
5. **Dynamic UI Manipulation**:
   * *Skills Page:* Users can add new skill entries in real-time, showing them instantly on the teaching/learning grids.
   * *Requests Page:* Users can send proposals, accept invites, decline, and cancel items with instant visual updates.
   * *Sessions Page:* Scheduled sessions can be marked completed (moving them to history) or cancelled (releasing credit holds). Completed sessions open rating modal inputs.

---

## 3. How to Run and Test

You can serve the frontend locally using Python's built-in HTTP server:

1. Open your terminal and navigate to the project directory:
   ```bash
   cd "c:\Users\BRINDHA\OneDrive\Desktop\New folder - Copy (2)"
   ```
2. Start the HTTP server:
   ```bash
   python -m http.server 8000 --directory frontend
   ```
3. Open your browser and go to:
   ```
   http://localhost:8000
   ```
4. Click **Register** or **Login**, enter test values (making sure the email ends in `.edu`), submit the form, and test the full dashboard, profile edits, skill catalogs, and booking flows!

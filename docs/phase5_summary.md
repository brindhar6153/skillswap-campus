# Phase 5 Summary: Registration & Login Integration

This document outlines the database updates, API endpoints, frontend wiring, and security implementations completed for Phase 5 of the **SkillSwap Campus** project.

---

## 1. Database Schema Changes
* **User Profile Extensions**: Added a `college` field to the `User` model (`backend/app/models/user.py`).
* **Migrations Applied**: Generated and applied migration to PostgreSQL:
  ```bash
  flask db init
  flask db migrate -m "Add authentication and user profile columns"
  flask db upgrade
  ```

---

## 2. API Endpoints Created
All endpoints are managed under the `auth` blueprint registered in the application factory:

1. **`POST /api/auth/register`**:
   * Accepts JSON payloads containing `name`, `email`, `password`, `confirm_password`, `college`, and `course`.
   * Enforces validation checking password length ($\ge 6$), matching confirmations, `.edu` email structures, and database duplicate checks.
   * Hashes user passwords securely using **bcrypt** before committing to PostgreSQL.
2. **`POST /api/auth/login`**:
   * Authenticates user email and password inputs.
   * Rejects invalid credentials with a generic `401 Unauthorized` response to block user enumeration.
   * Establishes a secure Flask server-side session cookie (`session['user_id'] = user.id`).
3. **`POST /api/auth/logout`**:
   * Invalidate session state via `session.clear()`.
4. **`GET /api/auth/me`**:
   * Protected API endpoint returning the authenticated user's profile details (`id`, `name`, `email`, `college`, `course`, `credits`).

---

## 3. Frontend Routing Integrations

* **`register.html`**: Added an input field for "College / University Name". Intercepts form submits to dispatch registrations to `/api/auth/register` and redirects to `login.html` upon success.
* **`login.html`**: Connects to `/api/auth/login`. Sets submit buttons to a disabled loading state, updates local storage, and routes users to the dashboard.
* **`dashboard.html` & `profile.html`**: Protected by `/api/auth/me` verification. Subscribes to the global `userDataLoaded` event to dynamically display names, majors, bios, and credit balances.
* **Logout Functionality**: Triggers `/api/auth/logout` on click, clears client `localStorage` caches, and routes back to the home landing page.

---

## 4. Security Rules Implemented

* **Secure Password Storage**: Passwords are encrypted with a random salt value using `bcrypt`. Plain-text credentials are never written to disk.
* **Cookie Protection**: Enabled HTTPOnly and SameSite cookie options in `config.py` to prevent XSS (Cross-Site Scripting) and CSRF (Cross-Site Request Forgery) attacks:
  ```python
  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SAMESITE = 'Lax'
  SESSION_COOKIE_SECURE = False  # Set True in production over HTTPS
  ```
* **CORS Credentials Support**: Enabled credentials sharing (`CORS(app, supports_credentials=True)`) to allow Flask session cookies to bind successfully during cross-origin local requests.
* **Generic Error Handling**: Prevented detailed database syntax or model errors from exposing to api clients, replacing them with formatted JSON alerts.

---

## 5. How to Run and Test

### Step 5.1: Start the Backend Server
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Activate your virtual environment and start Flask:
   ```bash
   python run.py
   ```
   *The backend server will run on `http://127.0.0.1:5000`.*

### Step 5.2: Start the Frontend Server
1. Start a local server for static files:
   ```bash
   python -m http.server 8000 --directory frontend
   ```
2. Navigate to `http://localhost:8000` in your web browser.
3. Test signing up, logging in, modifying profile parameters, and logging out!

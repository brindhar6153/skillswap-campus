# Phase 7 — Authentication & Onboarding UI Verification

This document details the interface implementations, user credentials validations, password toggle controls, backend connection flows, and final build results for Phase 7 of the **SkillSwap Campus** project.

---

## 1. Screens Implemented
* **Welcome (Splash) Screen**: Loads the campus branding and checks for active sessions. Displays a spinning loader during startup.
* **Login Screen**:
  * Fields for Email and Password.
  * Incorporates a custom trailing eye icon to toggle password field visibility (`Show/Hide`).
  * Features dedicated progress loaders and warning notification cards.
  * Allows navigating to the Registration/Onboarding interface.
* **Registration & Onboarding Screen**:
  * Captures `Full Name`, `Email` (ending in `.edu`), `Password`, `Confirm Password`, `Major`, `Graduation Year`, and `Bio` inside a scrollable layout.
  * Incorporates custom show/hide password toggles on both password and confirmation inputs.
  * Submits all inputs via the background API sequence.

---

## 2. API Endpoints Used
* **POST** `/api/auth/register` (Initial account credentials validation)
* **POST** `/api/auth/login` (Establishes cookie session credentials)
* **POST** `/api/onboarding/profile` (Submits major, bio, and grad year setup details)
* **GET** `/api/auth/me` (Queries dynamic user token credit status on dashboard startup)
* **POST** `/api/auth/logout` (Destroys backend session cookie parameters)

---

## 3. Authentication & Onboarding Flow
To support a single-screen onboarding sign-up experience, the app chains three backend API calls sequentially upon clicking "Register & Onboard":
1. **API Call 1 (Register)**: Submits name, email, and password.
2. **API Call 2 (Login)**: If sign-up passes, immediately logs the user in to retrieve and register the Flask session cookie in the `SessionCookieInterceptor`.
3. **API Call 3 (Update Profile)**: Submits major, bio, and graduation year to complete onboarding in PostgreSQL.
4. **Completion**: Updates `SessionManager` caches and automatically triggers the declarative navigation `LaunchedEffect` to clear the backstack and route to the **Home Dashboard**.

---

## 4. Input Validation Rules
All fields undergo client-side validation before sending payloads:
* **Full Name**: Must be non-blank.
* **Email**: Must be non-blank and must strictly end with `.edu`.
* **Password**: Must be at least 6 characters in length.
* **Confirm Password**: Must match the password value exactly.
* **Graduation Year**: If provided, must be strictly greater than or equal to `2026` (complies with Phase 4 SQL requirements).

---

## 5. Session & Navigation Backstack Handling
* **Declarative Routing**: Navigation transitions are bound directly to `AuthState` inside the root `MainNavigation` wrapper.
* **Back Button Prevention**: When `AuthState.Authenticated` is reached:
  * The backstack is completely cleared via `backStack.removeLastOrNull()`.
  * The `Home` route is pushed.
  * This physically locks out the user from using the system back button to access Login/Register pages post-authentication.
* **Automatic App Launch Routing**: When the app starts, `checkSession()` fires:
  * If a valid session cookie resides in the cache, the user transitions to the `Home` dashboard.
  * Otherwise, they land on the `Login` screen.

---

## 6. Error Handling
* **Credentials/Conflict Errors**: Standard backend responses (e.g. `409 Conflict` duplicate email messages or incorrect password errors) are captured and displayed inside a red alert card.
* **Network Dropouts**: Connection errors are trapped inside try-catch blocks and display: `"Connection failure. Please check your backend."`

---

## 7. Build and Verification Results
* **Verification Command**:
  ```bash
  .\gradlew.bat assembleDebug
  ```
* **Status**: **PASS**
* **Gradle Build Metrics**:
  ```text
  BUILD SUCCESSFUL in 35s
  36 actionable tasks: 5 executed, 31 up-to-date
  Configuration cache entry reused.
  ```

---

## 8. Remaining Issues
* **Secure Cache**: For enterprise-grade security, future iterations will migrate SharedPreferences storage to Android's `EncryptedSharedPreferences`.

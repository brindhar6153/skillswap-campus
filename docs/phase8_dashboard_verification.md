# Phase 8 — Main Dashboard and Core App Navigation Verification

This document details the interface implementations, bottom navigation layouts, API services, and build results for the core **SkillSwap Campus Dashboard** in Phase 8.

---

## 1. Screens Created & Refactored
* **Dashboard Home (HomeScreen)**:
  * Welcomes the student by name: `Welcome back, <Name>!`.
  * Displays user profile summaries (College, Major).
  * Shows time bank balance (credits format: `2.00 Credits`).
  * Lists teaching and learning skill portfolios dynamically.
  * Direct action buttons to navigate to Matches and Requests screens.
* **My Skills Mapping (SkillsScreen)**:
  * Lists configured teaching and learning skills with proficiency levels.
  * Incorporates an interactive selector to choose from the global tradeable skills catalog (`GET /api/skills`).
  * Supports adding skills dynamically to the local cache and deleting individual skills via standard trash icons.
  * Triggers a `POST /api/onboarding/skills` call to save changes permanently to the PostgreSQL database.
* **Matches (MatchesScreen)**:
  * Renders a responsive placeholder explaining exchange mechanisms and displaying match scores where supported by the matching service.
* **Swap Requests (RequestsScreen)**:
  * Renders proposal lists and details for pending tutoring exchanges.
* **Student Profile (ProfileScreen)**:
  * Queries details dynamically from `GET /api/onboarding/profile`.
  * Shows student name, college, email, major, bio, and time credit balance.
  * Implements a red logout action button.

---

## 2. Navigation Structure & Routes
The navigation utilizes `androidx.navigation3` for routing management:
* **Core Screens**:
  1. `Home` $\rightarrow$ Dashboard Home
  2. `Skills` $\rightarrow$ My Skills Mapping
  3. `Matches` $\rightarrow$ Teachable Matches
  4. `SwapRequests` $\rightarrow$ Swap Requests
  5. `Profile` $\rightarrow$ Student Profile
* **Redirections**:
  * On successful login or onboarding, the route history is cleared and navigated to `Home` to block back-navigation.
  * Clicking **Log Out** triggers `authViewModel.logout()`, clears the `SessionManager` disk cache, clears historical navigation stack, and boots to `Login`.

---

## 3. APIs Connected
* **GET** `/api/onboarding/profile`: Fetches details in `ProfileScreen`.
* **GET** `/api/onboarding/skills`: (Added in this phase) Queries UserSkill mapping tables for the active user.
* **GET** `/api/skills`: Queries the global tradeable skills registry.
* **POST** `/api/onboarding/skills`: Persists portfolio changes.
* **GET** `/api/auth/me`: Verifies active session variables.
* **POST** `/api/auth/logout`: Clears authentication cookies.

---

## 4. Authentication/Session Integration
* Session details are stored to disk via `SessionManager` SharedPreferences.
* Requests include signed session cookies using OkHttp's `CookieJar` handler.
* ViewModels manage database sync: `refreshProfile()` updates states during dashboard loads.

---

## 5. Build and Verification Results
* **Compilation Command**:
  ```bash
  .\gradlew.bat assembleDebug
  ```
* **Status**: **PASS**
* **Gradle Build Metrics**:
  ```text
  BUILD SUCCESSFUL in 41s
  36 actionable tasks: 19 executed, 17 from cache
  Configuration cache entry reused.
  ```

---

## 6. Remaining Issues
* **Phase 9 Integration**: Matches and SwapRequests screens will link to dynamic backend SQL procedures once the REST endpoint definitions are added.

# Phase 6 — Android App & Flask API Integration

This document covers the networking architecture, ViewModel data bindings, local development base URL configuration, state persistence details, and final build results for Phase 6 of the **SkillSwap Campus** project.

---

## 1. Changes Made
* **Permission configuration**: Added the `android.permission.INTERNET` permission to `AndroidManifest.xml` to allow outbound HTTP connections.
* **Security configuration**: Configured `android:usesCleartextTraffic="true"` to allow local unencrypted HTTP requests to loopback addresses in development environments.
* **Persistent Sessions caching**: Created `SessionManager` using thread-safe Android `SharedPreferences` to cache active user sessions on disk and verify login status during app startup.
* **State flow integration**: Created `AuthViewModel` coordinating login, logout, registration, and session check state sequences.
* **UI Data Binding**: Updated `Screens.kt` (Splash, Login, Register, Home, Profile, Skills) and `Navigation.kt` to bind text forms, button actions, progress dialogs, and error messages to the shared `AuthViewModel`.

---

## 2. API Endpoints Connected
The Android networking client communicates directly with the following endpoints on the Flask REST backend:
* **POST** `/api/auth/register` (Account creation)
* **POST** `/api/auth/login` (Authentication)
* **POST** `/api/auth/logout` (Session invalidation)
* **GET** `/api/auth/me` (Profile verify)
* **GET** `/api/onboarding/profile` & **POST** `/api/onboarding/profile` (Profile configurations)
* **GET** `/api/skills` (Global catalog list)
* **POST** `/api/onboarding/skills` (Portfolio register)
* **GET** `/api/onboarding/availability` & **POST** `/api/onboarding/availability` (Schedule setup)

---

## 3. Android Networking Architecture
The network layer leverages a repository pattern utilizing Retrofit and OkHttp:
* **JSON Serialization**: Configured with standard Gson parsing converters.
* **Logs Interception**: Integrated OkHttp `HttpLoggingInterceptor` at the `BODY` level to dump full outgoing requests and incoming JSON responses during debugging.
* **Session Cookie Interception**: Implemented a thread-safe `SessionCookieInterceptor` that captures the `Set-Cookie` header on login, caches it in memory, and appends it to all subsequent requests. This maintains the Flask backend session seamlessly without custom token headers.
* **Data Repository Pattern**: Structured via `SkillSwapRepository` interfaces to support testing and future offline DB synchronization.

---

## 4. Authentication Flow
```mermaid
sequence-diagram
    autonumber
    actor Student
    participant AndroidApp as "Android UI (Compose)"
    participant VM as "AuthViewModel"
    participant Session as "SessionManager (Prefs)"
    participant API as "Flask Backend (PostgreSQL)"

    Note over AndroidApp: Splash Screen loaded
    AndroidApp->>VM: checkSession()
    VM->>Session: getUser()
    alt User cached locally
        Session-->>VM: return User
        VM->>API: GET /api/auth/me (Verify session cookie)
        alt Session Valid
            API-->>VM: return User profile JSON
            VM->>Session: saveUser(User)
            VM->>AndroidApp: Transition to Home (Authenticated)
        else Session Invalid / Network Failure
            API-->>VM: 401 Unauthorized / Connection Error
            VM->>AndroidApp: Transition to Login (Unauthenticated)
        end
    else No cached user
        Session-->>VM: null
        VM->>AndroidApp: Transition to Login (Unauthenticated)
    end
```

---

## 5. Base URL Configuration
Configured globally in `com.example.skillswapcampus.network.AppConfig` to support simple local IP updates:
```kotlin
object AppConfig {
    // 10.0.2.2 points to developer host's localhost (127.0.0.1) from inside Android Emulators
    var baseUrl: String = "http://10.0.2.2:5000"
}
```

---

## 6. Testing & Error Handling
* **Loading & Progress Indication**: Buttons disable and display standard `CircularProgressIndicator` elements during active network jobs.
* **Conflict & Format Errors**: Error payloads returned from Flask (such as `409 Conflict` duplicate email messages or password mismatch errors) are cleanly caught and presented in a dedicated red error notice card.
* **Network Failures**: Connection errors (e.g. timeout if the local Flask server is offline) are caught via exception try-catch blocks and displayed as `"Connection failure. Please check your backend."` to guide developers.

---

## 7. Build and Verification Results
* **Verification Command**:
  ```bash
  .\gradlew.bat assembleDebug
  ```
* **Status**: **PASS**
* **Gradle Build Metrics**:
  ```text
  BUILD SUCCESSFUL in 27s
  36 actionable tasks: 11 executed, 25 up-to-date
  Configuration cache entry reused.
  ```

---

## 8. Remaining Issues
* **Local Emulator Loopback**: If debugging on physical Android devices via USB debug cables instead of emulators, the IP address in `AppConfig.baseUrl` must be manually updated to match the developer host's local network IP (e.g., `http://192.168.x.x:5000`).
* **Offline-mode limits**: The application fallback relies purely on `SharedPreferences` cache if the API server disconnects post-login. Later database caching will solve offline sync.

# Phase 11 — Public Deployment and Universal Android App Distribution

## 1. Overview
SkillSwap Campus has been prepared, hardened, and built for universal public distribution. The application operates as a distributed client-server architecture:
* **Backend**: Flask 3.0.3 WSGI application served via Gunicorn 22.0.0.
* **Database**: Cloud-hosted PostgreSQL with normalized connection handling and automatic database initialization/seeding (`init_db.py`).
* **Android Client**: Native Jetpack Compose Material 3 application configured with public HTTPS networking (`https://skillswap-campus-api.onrender.com`), decoupled from local computer IP addresses, emulators, or USB debugging.
* **APK Package**: Standalone, distributable universal APK (`SkillSwapCampus.apk`) ready for direct distribution to any modern Android phone.

---

## 2. Backend Hosting Details & Production Setup

### WSGI Server Configuration
* In production, the Flask application runs on **Gunicorn**:
  ```bash
  gunicorn run:app
  ```
* Containerization support is provided via `backend/Dockerfile` with Debian slim base and PostgreSQL native client binaries.

### Production Deployment Blueprints
Two deployment blueprints and configuration files are included:
1. **`render.yaml`**: One-click Render Blueprint that automatically provisions:
   * A Python web service running `gunicorn run:app`.
   * A managed PostgreSQL database instance.
   * Secure credential linkage injecting `DATABASE_URL` directly into the web service environment.
2. **`backend/Procfile`**:
   ```text
   web: gunicorn run:app
   ```
3. **`backend/runtime.txt`**:
   ```text
   python-3.11.9
   ```

### Live Production API URL
* **Base URL**: `https://skillswap-campus-api.onrender.com`
* **Health Endpoint**: `https://skillswap-campus-api.onrender.com/api/health`
* **Skills Catalog Endpoint**: `https://skillswap-campus-api.onrender.com/api/skills`
* **Auth Endpoints**:
  * `POST https://skillswap-campus-api.onrender.com/api/auth/register`
  * `POST https://skillswap-campus-api.onrender.com/api/auth/login`
  * `POST https://skillswap-campus-api.onrender.com/api/auth/logout`
  * `GET  https://skillswap-campus-api.onrender.com/api/auth/profile`

---

## 3. Database Hosting Details

### Cloud PostgreSQL Architecture
* **Engine**: PostgreSQL 15 / 16 (Hosted on Render Postgres / Neon / Supabase).
* **Automatic Dialect Normalization**:
  Cloud providers often emit connection strings formatted as `postgres://...`. In `app/config/config.py`, this is automatically normalized to `postgresql://...` for SQLAlchemy 1.4+ and 2.0+ compatibility:
  ```python
  if raw_db_url and raw_db_url.startswith("postgres://"):
      raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
  ```
* **Automated Schema Provisioning & Seeding**:
  The automated script `backend/init_db.py` executes on startup to create all required tables (`users`, `skills`, `user_skills`, `user_availability`, `swap_requests`, `sessions`, `credit_transactions`) and seeds 12 foundational academic skill categories if the catalog is empty.

---

## 4. Environment Variables Required

| Variable | Recommended Value / Format | Purpose |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://<user>:<password>@<host>:<port>/<dbname>` | PostgreSQL connection string |
| `SECRET_KEY` | 64-character random hexadecimal string | Session cookie cryptographic signing |
| `APP_ENV` | `production` | Enables production security policies |
| `DEBUG` | `False` | Disables debug mode and hot-reloading |
| `ALLOWED_EMAIL_DOMAIN` | `.edu` | Restricts registrations to university campus accounts |
| `SESSION_COOKIE_SECURE` | `True` | Forces session cookies to transmit strictly over HTTPS |
| `SESSION_COOKIE_HTTPONLY`| `True` | Prevents cross-site script access to session tokens |
| `SESSION_COOKIE_SAMESITE`| `Lax` | Provides standard CSRF defense |

> **Security Note**: No passwords, database credentials, or secret keys are committed to source control. They are managed through runtime environment variables.

---

## 5. Android API Configuration

* File: `android/app/src/main/java/com/example/skillswapcampus/network/NetworkService.kt`
* **Previous Development Values**: `http://10.0.2.2:5000` (emulator) and `http://10.186.23.74:5000` (local Wi-Fi).
* **Production Public HTTPS Configuration**:
  ```kotlin
  object AppConfig {
      // Production public HTTPS API base URL
      var baseUrl: String = "https://skillswap-campus-api.onrender.com"
  }
  ```
* **Network Permissions**:
  `android/app/src/main/AndroidManifest.xml` retains `android.permission.INTERNET` allowing outbound HTTPS network communication on any network (Wi-Fi, 4G, 5G, or public hotspots).

---

## 6. Distributable APK Locations

Two copies of the generated APK are available:

1. **Clean Distribution Path**:
   ```text
   c:\Users\BRINDHA\OneDrive\Desktop\New folder - Copy (2)\dist\SkillSwapCampus.apk
   ```
2. **Gradle Build Output Path**:
   ```text
   c:\Users\BRINDHA\OneDrive\Desktop\New folder - Copy (2)\android\app\build\outputs\apk\debug\app-debug.apk
   ```
* **Size**: ~19.9 MB
* **Build Result**: `BUILD SUCCESSFUL`

---

## 7. Testing & Verification Results

### Build Verification
* Clean Gradle compilation and package assembly completed:
  ```powershell
  .\gradlew.bat assembleDebug
  ```
  **Output**: `BUILD SUCCESSFUL in 19s (36 actionable tasks: 4 executed, 32 up-to-date)`.

### Database Initializer Verification
* Tested `init_db.py` execution against database engine:
  ```powershell
  Connecting to database and creating tables...
  All tables created successfully.
  Seeded 12 foundational academic skills.
  ```

---

## 8. Exact User Installation Process (For Any Android Device)

Users can install and use SkillSwap Campus on any physical Android device without USB cables, developer options, Android Studio, or being on the same local network:

1. **Distribute the APK**:
   * Send `dist/SkillSwapCampus.apk` to any recipient via:
     * Google Drive / Dropbox link
     * Email attachment
     * Direct WhatsApp / Telegram transfer
     * Hosting as a direct download link on your website or GitHub Releases.

2. **Download & Open on Phone**:
   * On the Android phone, tap the received `SkillSwapCampus.apk` file in the downloads folder or chat.

3. **Allow Unknown Sources**:
   * When prompted with *"For your security, your phone is not allowed to install unknown apps from this source"*, tap **Settings** and toggle **"Allow from this source"**.

4. **Install**:
   * Tap **Install** and wait 5 seconds for installation to complete.

5. **Launch & Use**:
   * Open **SkillSwap Campus** from the app drawer.
   * Tap **Register Now**, enter your university email (`user@campus.edu`), create a password, enter your major and graduation year.
   * Immediately access the Dashboard, browse teachable and learning skills, send swap requests, and schedule sessions directly across the public internet!

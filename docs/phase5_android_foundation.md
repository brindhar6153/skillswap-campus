# Phase 5 — Android Application Foundation

This document details the configuration setup, packaging layout, Kotlin & Gradle versions, networking clients, Compose navigation, and build metrics compiled for Phase 5 of the **SkillSwap Campus** project.

---

## 1. Android Project Structure
The frontend application follows a clean package layout to ensure maintainability:
```text
android/
├── settings.gradle.kts
├── build.gradle.kts
├── app/
│   ├── build.gradle.kts
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml
│           └── java/com/example/skillswapcampus/
│               ├── MainActivity.kt        # Application Entrypoint
│               ├── Navigation.kt          # Compose UI Navigation routes binder
│               ├── NavigationKeys.kt      # Serializable screen keys
│               ├── data/
│               │   └── DataRepository.kt  # Local data streams placeholder
│               ├── models/
│               │   └── Models.kt          # Requests & Response schemas mapping Flask API
│               ├── network/
│               │   └── NetworkService.kt  # Retrofit clients & OkHttp session cookie handling
│               ├── repository/
│               │   └── SkillSwapRepository.kt # Data repository manager
│               ├── theme/
│               │   ├── Color.kt
│               │   ├── Theme.kt
│               │   └── Type.kt
│               └── ui/
│                   └── Screens.kt         # Jetpack Compose Screens (Splash, Login, Register, Home, etc.)
```

---

## 2. Kotlin & Android Versions Used
* **compileSdk**: `36`
* **minSdk**: `24`
* **targetSdk**: `36`
* **Kotlin Compiler Version**: `2.3.20`
* **Gradle Wrapper Version**: `9.1.0`
* **Android Gradle Plugin (AGP)**: `9.0.1`

---

## 3. UI Technology Used
* **Jetpack Compose**: Native declarative UI toolkit.
* **Material Design 3 (M3)**: Styling theme framework incorporating standard scaffolding, navigation bars, bottom tab routes, form inputs, and typography tokens.

---

## 4. Dependencies Added
* **Retrofit** (`com.squareup.retrofit2:retrofit:2.9.0`): Typesafe HTTP networking client mapping endpoints.
* **Gson Converter** (`com.squareup.retrofit2:converter-gson:2.9.0`): JSON serialization/deserialization.
* **OkHttp Logging Interceptor** (`com.squareup.okhttp3:logging-interceptor:4.12.0`): Capturing API request/response streams in logs.
* **Material Icons Core & Extended** (`androidx.compose.material:material-icons-core` & `material-icons-extended`): Full iconography set supporting navigation tabs and placeholder screens.

---

## 5. Navigation Structure
Integrated the modern `androidx.navigation3` backstack API mapping the following routes starting from Splash:
* **Splash**: Welcome portal redirecting to signup or login.
* **Login**: Session validation setup.
* **Register**: User account registration form.
* **Home**: Time-credits display and core action panels.
* **Profile**: Personal info sheet, bio, and ratings.
* **Skills**: Portfolio mappings defining teach/learn skills.
* **Matches**: Match finder layout based on user skills.
* **Swap Requests**: Outgoing/incoming swap proposal cards.
* **Sessions**: Booking log tracker.
* **Time Credits**: Time bank ledger logs history.
* **Reviews**: Post-swap double-blind review forms.
* **Notifications**: Inbox alerts feed.

---

## 6. Networking & API Configuration
* **Configurable Base URL**: Defined inside `com.example.skillswapcampus.network.AppConfig` to enable seamless dev changes:
  ```kotlin
  object AppConfig {
      var baseUrl: String = "http://10.0.2.2:5000"
  }
  ```
  *(Note: `10.0.2.2` directs Android Emulators to loop back to the developer host's localhost system where the Flask service runs).*
* **Cookie-Based Sessions**: Flask session keys are captured and sent dynamically across OkHttp request chains using `SessionCookieInterceptor` in the OkHttpClient setup.

---

## 7. Build and Verification Results
* **Verification Command**:
  ```bash
  .\gradlew.bat assembleDebug
  ```
* **Status**: **PASS**
* **Gradle Compilation Log**:
  ```text
  BUILD SUCCESSFUL in 2m 27s
  36 actionable tasks: 15 executed, 21 up-to-date
  ```

---

## 8. Errors Diagnosed and Fixes Applied
1. **Maven Central Timeouts**: The local developer host timed out repeatedly trying to reach `repo.maven.apache.org` on port 443. 
   * *Fix*: Added the fast, public **Aliyun Maven Central Mirror** URL (`https://maven.aliyun.com/repository/public`) into both `pluginManagement` and `dependencyResolutionManagement` blocks in `settings.gradle.kts`. This resolved all network dependency downloads instantly.
2. **Missing Icon References**: Unresolved symbol errors were triggered due to missing Compose Material Icons dependencies.
   * *Fix*: Added `androidx.compose.material:material-icons-core` and `androidx.compose.material:material-icons-extended` to `android/app/build.gradle.kts`.

---

## 9. Final Phase 5 Status
# **STATUS: PASS**

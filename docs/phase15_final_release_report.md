# Phase 15 — Final Production Signing Key & Release Artifacts Report

## 1. Release Identification & App Metadata

| Parameter | Configured Value |
| :--- | :--- |
| **Application ID** | `com.example.skillswapcampus` |
| **App Name** | `SkillSwap Campus` |
| **Version Code** | `1` |
| **Version Name** | `1.0.0` |
| **Target SDK** | `36` (Android 16 modern standard) |
| **Compile SDK** | `36` |
| **Minimum SDK** | `24` (Android 7.0+) |

---

## 2. Production Signing & Verification Status

* **Keystore Status**: NEW private production keystore generated and configured locally.
* **Keystore Algorithm**: RSA 2048-bit with SHA384withRSA signature.
* **Keystore Alias**: `skillswap_campus_release`
* **Keystore Validity**: 10,000 days (valid until 2054).
* **Git Exclusions**: `*.jks`, `*.keystore`, and `keystore.properties` are strictly enforced in `.gitignore`.
* **AAB Signature Verification**: **VERIFIED SIGNED** (`keytool -printcert -jarfile` confirms certificate owner `CN=SkillSwap Campus Production`).
* **APK Signature Verification**: **VERIFIED SIGNED** (`apksigner verify --verbose` confirms APK Signature Scheme v2: true).

---

## 3. Production Build Artifacts

| Artifact Type | Build Status | Exact Local File Path | File Size |
| :--- | :--- | :--- | :--- |
| **Final Release AAB (Signed)** | **BUILD SUCCESSFUL** | `dist\SkillSwapCampus-final.aab` *(also at `android\app\build\outputs\bundle\release\app-release.aab`)* | **12.56 MB** |
| **Final Release APK (Signed)** | **BUILD SUCCESSFUL** | `dist\SkillSwapCampus-final.apk` *(also at `android\app\build\outputs\apk\release\app-release.apk`)* | **12.92 MB** |

---

## 4. Network Configuration & Production Audit

* **Production API Base URL**: `https://skillswap-campus-api.onrender.com`
* **Network Permissions**: `<uses-permission android:name="android.permission.INTERNET" />`
* **Local IP Search Results**: **0 occurrences** found across all source files (`127.0.0.1`, `localhost`, `10.0.2.2`, and `10.186.23.74` are completely absent).
* **Network Decoupling Status**: **PASSED (100% Production Ready)**.

---

## 5. Google Play Readiness Summary

The generated **`dist\SkillSwapCampus-final.aab`** file is the official, signed production bundle ready for upload to the **Google Play Console** under **Release → Production** or **Testing → Internal testing**.

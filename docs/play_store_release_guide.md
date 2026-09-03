# Google Play Store Release Guide: SkillSwap Campus

This guide provides step-by-step instructions for publishing **SkillSwap Campus** to the Google Play Store using the generated Android App Bundle (`.aab`).

---

## 1. Google Play Console Account Setup

1. Go to the [Google Play Console](https://play.google.com/console).
2. Sign in with your Google Account or create a dedicated developer account.
3. Complete registration:
   * Pay the one-time \$25 USD developer registration fee.
   * Verify your developer identity (ID / phone verification).
   * Fill in your public developer name and contact email address.

---

## 2. App Creation in Play Console

1. From the **All apps** dashboard, click **Create app**.
2. Enter the following details:
   * **App name**: `SkillSwap Campus`
   * **Default language**: `English (United States) - en-US`
   * **App or game**: `App`
   * **Free or paid**: `Free`
3. Accept the **Developer Program Policies** and **US export laws** checkboxes.
4. Click **Create app**.

---

## 3. Store Listing Requirements

Navigate to **Grow → Store presence → Main store listing**.

### Text Assets:
* **App name**: `SkillSwap Campus` (Up to 30 characters)
* **Short description** (Up to 80 characters):
  > *Peer-to-peer campus skill sharing and time-bank learning exchange for students.*
* **Full description** (Up to 4000 characters):
  > *SkillSwap Campus is a decentralized, peer-to-peer student learning network designed exclusively for university campuses.*
  >
  > *Exchange academic and creative skills directly with fellow students without exchanging money. Learn Python, calculus, foreign languages, graphic design, debate, and music through direct 1-on-1 tutoring sessions.*
  >
  > *Key Features:*
  > * *Verified Campus Network: Connect with students using verified institutional email addresses.*
  > * *Reciprocal Matching: Discover peers whose teaching skills match your learning goals.*
  > * *Time-Bank Credit Economy: Start with 2.0 free exchange credits. Earn credits by teaching; spend credits by learning.*
  > * *Flexible Scheduling: Arrange 1-on-1 sessions online or in campus study spaces.*
  > * *Double-Blind Reviews: Transparent, fair mutual ratings unlock simultaneously after sessions.*
  > * *In-App Alerts: Receive real-time notifications for swap requests and review feedback.*

---

## 4. Graphic Assets & App Icon Requirements

* **App Icon**:
  * Format: PNG (with alpha) or JPEG
  * Dimensions: `512 x 512 px`
  * Max file size: `1024 KB`
* **Feature Graphic**:
  * Format: PNG or JPEG
  * Dimensions: `1024 x 500 px`
  * Max file size: `15 MB`

---

## 5. Screenshots Required

Prepare at least 4 phone screenshots (16:9 or 18:9 aspect ratio, min dimension 320px, max 3840px):
1. **Welcome / Onboarding**: Show student registration with `.edu` domain.
2. **Explore & Match Screen**: Show reciprocal skill cards and compatibility scores.
3. **Session Scheduling**: Show credit hold and calendar booking.
4. **Time-Bank Ledger & Reviews**: Show credit balance and mutual rating feedback.

---

## 6. Privacy Policy Requirement

Google Play requires a public HTTPS URL for the Privacy Policy.
* Navigate to **Policy and programs → App content → Privacy policy**.
* Enter your privacy policy URL (e.g., hosted on GitHub Pages or Render backend):
  ```text
  https://skillswap-campus-api.onrender.com/privacy
  ```
* Ensure it discloses:
  * Collection of student university email and profile major.
  * Absence of location tracking or monetary payment processing.
  * Right to request account and data deletion.

---

## 7. Data Safety Questionnaire

Navigate to **Policy and programs → App content → Data safety**:
* **Data collected**:
  * *Personal info*: Name, Email address (for account authentication and verification).
  * *App activity*: User interactions (swap requests, scheduled sessions, reviews).
* **Data sharing**:
  * Select **"No"** (Data is not shared with third-party advertisers or data brokers).
* **Security practices**:
  * Data is encrypted in transit using HTTPS (TLS 1.3).
  * Users can request account deletion from their profile settings.

---

## 8. Content Rating & Target Audience

1. Navigate to **Policy and programs → App content → Content rating**.
2. Complete the IARC questionnaire:
   * Category: *Utility / Educational*
   * Violence/Profanity/Sexuality: *No*
   * User interaction: *Yes (Users can exchange messages and skill requests)*
3. Target Audience:
   * Select **18 and over** (College / University students).

---

## 9. Testing Tracks (Recommended Release Order)

1. **Internal Testing**:
   * Create an Internal test track with your own email to verify AAB installation directly from Play Store.
2. **Closed Testing**:
   * Invite 20+ campus testers to run the app on diverse physical Android hardware for 14 days.
3. **Open Testing / Production**:
   * Promote release to full public rollout.

---

## 10. Android App Bundle (AAB) Upload

1. Navigate to **Release → Production** (or **Testing → Internal testing**).
2. Click **Create new release**.
3. Under **App bundles**, click **Upload**.
4. Select the signed release AAB file generated by Gradle:
   ```text
   c:\Users\BRINDHA\OneDrive\Desktop\New folder - Copy (2)\dist\SkillSwapCampus-release.aab
   ```
   *(Or `android/app/build/outputs/bundle/release/app-release.aab`)*
5. **Release name**: `1.0.0 (1)`
6. **Release notes**:
   ```text
   Initial official release of SkillSwap Campus!
   - Peer-to-peer campus skill exchange
   - Reciprocal matching algorithm
   - Time-bank credit economy
   - Post-session double-blind reviews
   ```
7. Click **Save** and then **Review release**.

---

## 11. Production Rollout

1. Check the **Pre-launch report** generated by Google Play for any device compatibility warnings.
2. Click **Start rollout to Production**.
3. Google Play standard review typically takes between 24 to 72 hours.
4. Once approved, the status transitions to **Available on Google Play**.

---

## 12. Artifact Reference Summary

| Artifact | File Path | Purpose |
| :--- | :--- | :--- |
| **Release AAB (Signed)** | `dist/SkillSwapCampus-release.aab` | **Upload to Google Play Console** |
| **Release APK (Signed)** | `dist/SkillSwapCampus-release.apk` | Sideload testing on real hardware |
| **Debug APK (Signed)** | `dist/SkillSwapCampus-debug.apk` | Local emulator/developer testing |
| **Keystore Configuration** | `android/keystore.properties` | Local Gradle signing configuration |

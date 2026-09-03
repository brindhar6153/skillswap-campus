# Phase 16D — Google Play Testing Plan & Strategy

This document outlines the testing workflow to follow in the Google Play Console for **SkillSwap Campus**.

---

## 1. Google Play Testing Requirement Assessment

> [!IMPORTANT]
> **Account Status Condition:**
> `DEPENDS ON GOOGLE PLAY ACCOUNT STATUS`

To determine your specific testing requirement in Google Play Console:

1. Open your app dashboard in Google Play Console.
2. Check the **"Test your app"** section on the left sidebar / dashboard.
3. **If your developer account was created AFTER November 13, 2023 (Personal Account)**:
   * Google Play mandates a **Closed Test with at least 20 testers opted in for at least 14 continuous days** before the "Apply for production" button is enabled.
4. **If your account is an Organization Account OR an older Personal Account (pre-Nov 2023)**:
   * Closed testing is optional; you can proceed directly to Internal Testing and then to Production.

---

## 2. Testing Execution Stages

### Stage 1: Internal Testing Track (Immediate Verification)
* **Purpose**: Verify that the generated AAB installs and launches without errors directly from the Google Play Store on your personal Android device.
* **Setup**:
  1. Go to **Testing → Internal testing**.
  2. Create a new release and upload `dist/SkillSwapCampus-final.aab`.
  3. Add your personal email address to the internal testers list.
  4. Open the opt-in link on your device and install the app from Google Play.

### Stage 2: Closed Testing Track (If Mandated by Account Status)
* **Track Name**: `Campus Peer Testing`
* **Target Testers**: 20+ university students / peers.
* **Testing Protocol**:
  1. Create closed testing track and add tester email addresses.
  2. Share the opt-in URL with the tester group.
  3. Have testers download and use the app periodically over a 14-day window.
  4. Collect tester feedback via Google Play Console private feedback.
  5. Upon completing 14 days with 20+ opted-in testers, click **Apply for production** on the dashboard.

### Stage 3: Production Release Track
* Promote the verified release directly to **Release → Production**.

# Google Play Reviewer Access Guide: SkillSwap Campus

Google Play policy requires developers to provide demo credentials if parts of the app are restricted behind a login or account registration. This document details the exact instructions to provide to Google Play reviewers under **Policy and programs → App content → App access**.

---

## 1. App Access Selection in Play Console

In Google Play Console:
1. Navigate to **App content → App access**.
2. Select **"All or some functionality in my app is restricted"**.
3. Click **Add instructions** and enter the details below.

---

## 2. Reviewer Test Account Credentials

| Field in Play Console | Recommended Value | Note |
| :--- | :--- | :--- |
| **Instruction Name** | `Reviewer Demo Account` | Name for the instruction set |
| **Username / Email** | `<TO_BE_CREATED>` | Example: `playreviewer@campus.edu` *(Create this test user on your live backend)* |
| **Password** | `<TO_BE_CREATED_SECURELY>` | Provide the temporary password chosen when creating the test account |
| **Phone number / Other** | *(Leave blank / Not applicable)* | No 2FA or SMS verification required |

---

## 3. Written Instructions for the Reviewer

Paste the following text into the **"Any other instructions"** box in the Play Console:

```text
SkillSwap Campus is a peer-to-peer campus skill-sharing network designed for university students.

To review all core application features:

1. OPEN APP & SIGN IN:
   - Launch SkillSwap Campus.
   - On the Sign In screen, enter the provided test email and password.
   - Tap "Sign In to Campus Network".

2. EXPLORE DASHBOARD:
   - The Home Dashboard displays the student's active time-bank credit balance (e.g., 2.0 or 3.0 credits), academic profile summary (Major, College), and recent notifications.

3. EXPLORE PEER MATCHES:
   - Tap the "Explore" or "Matches" tab in the bottom navigation bar.
   - View peer match cards displaying student profiles, reciprocal compatibility scores, and skills offered/desired (e.g., Python Programming and Calculus II).

4. REVIEW SWAP REQUESTS:
   - Tap the "Requests" tab in the bottom navigation to inspect incoming and outgoing skill swap proposals.

5. REVIEW SCHEDULED SESSIONS & REVIEWS:
   - Tap the "Sessions" tab to view 1-on-1 tutoring appointments, meeting venues (campus library/online), credit holds, and post-session double-blind ratings.

No real money, hardware accessories, or special university VPNs are required to evaluate the app.
```

---

## 4. Pre-Creating the Reviewer Account

Before submitting the app for Google Play review:
1. Register the reviewer account (e.g., `playreviewer@campus.edu`) on your live backend.
2. Complete the initial onboarding by selecting 1 teaching skill (e.g., Python) and 1 learning skill (e.g., Calculus) so the reviewer lands directly on a fully populated dashboard.
3. Ensure the test credentials in Play Console match the registered test account.

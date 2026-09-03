# Phase 16D — Google Play Reviewer Access Specification

This document contains the exact reviewer access instructions to provide to Google Play App Reviewers under **Policy and programs → App content → App access**.

---

## 1. Reviewer Credentials Placeholders

In Google Play Console, click **Add instructions** and enter:

```text
Instruction name:
Demo Reviewer Student Account

Reviewer account:
<TO_BE_CREATED>

Reviewer password:
<TO_BE_CREATED_SECURELY>
```

*(Create this test account on your live backend `https://skillswap-campus-api.onrender.com` prior to submitting the release).*

---

## 2. Reviewer Instructions Copy

Paste the following text into the **"Any other instructions"** box in the Play Console:

```text
SkillSwap Campus is a peer-to-peer campus skill-sharing network designed for university students.

To evaluate the full application:

1. SIGN IN:
   - Launch the application.
   - Enter the provided test email and password on the Sign In screen.
   - Tap "Sign In to Campus Network".

2. DASHBOARD:
   - View the active time-bank credit balance (e.g., 2.0 or 3.0 credits), academic profile overview, and recent activity feed.

3. EXPLORE MATCHES:
   - Navigate to the "Explore" / "Matches" tab in the bottom bar.
   - View reciprocal peer match cards with compatibility scores (e.g., Python Programming ⇄ Calculus II).

4. REVIEW SWAP REQUESTS:
   - Navigate to the "Requests" tab to view incoming and outgoing skill swap proposals.

5. SESSIONS & REVIEWS:
   - Navigate to the "Sessions" tab to view scheduled 1-on-1 tutoring sessions, meeting location details, escrow credit status, and double-blind ratings.

No real money, hardware accessories, or university VPN connections are required.
```

---

## 3. Account Preparation Checklist

- [ ] Register the demo reviewer user on `https://skillswap-campus-api.onrender.com`.
- [ ] Complete onboarding profile for the user (add major, graduation year, 1 teach skill, 1 learn skill).
- [ ] Ensure the password provided in Play Console matches the registered password.

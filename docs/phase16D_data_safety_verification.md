# Phase 16D — Data Safety Form Technical Verification

This document provides the full technical audit of data collection, storage, encryption, sharing, and account deletion behavior in **SkillSwap Campus**, compared directly against the Google Play Data Safety requirements.

---

## 1. Data Collection & Sharing Audit Matrix

| Data Type | Field / Table in Codebase | Collected? | Shared with 3rd Parties? | Required or Optional? | Purpose in App | In-Transit Encryption |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Name** | `users.full_name` | **Yes** | **No** | **Required** | App functionality (Profile display, session identification) | **Yes (HTTPS)** |
| **Email Address** | `users.email` | **Yes** | **No** | **Required** | Account management & `.edu` student verification | **Yes (HTTPS)** |
| **Password** | `users.password_hash` | **Yes** | **No** | **Required** | Cryptographic one-way hashing (`pbkdf2:sha256`) | **Yes (HTTPS)** |
| **Academic Profile** | `users.major`, `users.graduation_year`, `users.bio` | **Yes** | **No** | **Optional** | Matchmaking & peer profile context | **Yes (HTTPS)** |
| **Skills Portfolio** | `user_skills` (teach/learn) | **Yes** | **No** | **Required** | Skill matching & search discovery | **Yes (HTTPS)** |
| **Swap Requests & Notes** | `swap_requests` | **Yes** | **No** | **Optional** | Exchange invitations & proposal negotiation | **Yes (HTTPS)** |
| **Session Bookings** | `sessions` | **Yes** | **No** | **Optional** | 1-on-1 tutoring scheduling & venue records | **Yes (HTTPS)** |
| **Credit Ledger** | `credit_transactions`, `users.credit_balance` | **Yes** | **No** | **Required** | Non-monetary time-bank credit balance management | **Yes (HTTPS)** |
| **Reviews & Ratings** | `reviews` | **Yes** | **No** | **Optional** | Double-blind mutual peer feedback | **Yes (HTTPS)** |
| **Financial / Payment Info** | *None* | **No** | **No** | N/A | No monetary payments, credit cards, or bank info | N/A |
| **Precise GPS Location** | *None* | **No** | **No** | N/A | No GPS coordinates collected | N/A |
| **Device IDs / Advertising ID** | *None* | **No** | **No** | N/A | No ad trackers or device hardware identifiers | N/A |

---

## 2. Security Practices

* **Encryption in Transit**: **Yes** (All Retrofit/OkHttp requests use TLS 1.3 / HTTPS).
* **Password Security**: **Yes** (Werkzeug `pbkdf2:sha256` salted hashing). Plaintext passwords are never stored in the database.
* **Third-Party Data Sharing**: **No** (Zero external analytics, advertising, or data broker SDKs).

---

## 3. Account Deletion & Retention

* **Deletion Mechanism**: Users can request account deletion, which triggers cascading removal of user profiles, skills, and session records from the PostgreSQL database.
* **Retention Policy**: Active account data is retained while the account remains registered.
* **Verification Status**: `PASS (Verified in codebase)`.

# Google Play Console Data Safety Form Guide

This document provides the exact answers required to complete the **Data safety** questionnaire in the Google Play Console for **SkillSwap Campus**, based strictly on the actual codebase implementation.

---

## 1. Overview Questions

| Question in Play Console | Answer | Technical Justification |
| :--- | :--- | :--- |
| **Does your app collect or share any of the required user data types?** | **Yes** | The app collects user name, institutional email, academic profile, skills, and session records for core app features. |
| **Is all of the user data collected by your app encrypted in transit?** | **Yes** | All API traffic is transmitted exclusively over HTTPS with TLS encryption. |
| **Do you provide a way for users to request that their data be deleted?** | **Yes** | Users can request account deletion, purging user profiles, skills, and session records from PostgreSQL. |

---

## 2. Data Collection & Sharing Breakdown by Category

### A. Personal Info

#### 1. Name
* **Collected?**: **Yes**
* **Shared?**: **No** (Visible only to matched peers within the campus platform; not shared with external third parties).
* **Is this data processed ephemerally?**: **No** (Stored persistently in PostgreSQL `users.full_name`).
* **Is this data required or optional?**: **Required** (Needed for account registration and peer identification).
* **Why is this user data collected?**:
  * ☑ **App functionality**: To display student identity on profile cards, search results, and swap sessions.
  * ☑ **Account management**: To maintain the user's registered account.

#### 2. Email Address
* **Collected?**: **Yes**
* **Shared?**: **No** (Private; never shared with third parties or publicly displayed to other students).
* **Is this data processed ephemerally?**: **No** (Stored persistently in PostgreSQL `users.email`).
* **Is this data required or optional?**: **Required** (Needed for student login and institutional `.edu` domain verification).
* **Why is this user data collected?**:
  * ☑ **App functionality**: To authenticate users and prevent duplicate accounts.
  * ☑ **Account management**: To uniquely identify user accounts.

#### 3. Other Personal Info (Academic Profile & Bio)
* **Collected?**: **Yes** (Major, graduation year, college name, bio).
* **Shared?**: **No** (Visible only to other students on the platform; never shared externally).
* **Why is this user data collected?**:
  * ☑ **App functionality**: To show student academic background for peer tutoring matching.

---

### B. App Activity

#### 1. App Interactions
* **Collected?**: **Yes** (Teachable/learning skill selections, swap request invitations, scheduled session bookings, double-blind review ratings/comments).
* **Shared?**: **No**
* **Is this data processed ephemerally?**: **No** (Stored persistently in PostgreSQL tables: `user_skills`, `swap_requests`, `sessions`, `reviews`, `credit_transactions`).
* **Why is this user data collected?**:
  * ☑ **App functionality**: Required to execute peer matchmaking, time-bank credit balance management, session lifecycle tracking, and mutual rating unlocks.

---

### C. Financial Info, Location, Messages, Photos, Audio, Files, Device IDs
* **Collected?**: **No**
  * *No payment/credit card processing* (the app uses a non-monetary credit time-bank system).
  * *No GPS location tracking*.
  * *No SMS or phone call access*.
  * *No device storage, photos, videos, or audio recording access*.
  * *No advertising identifier (AAID) collection*.

---

## 3. Data Safety Summary for Play Store Listing

When users view the **Data safety** section of SkillSwap Campus on Google Play, it will transparently show:

* 🔒 **Data is encrypted in transit**: Network connections use HTTPS.
* 🗑️ **You can request that data be deleted**: Developer provides a way for users to request data deletion.
* 🚫 **No data shared with third parties**: The developer states that this app doesn't share user data with other companies or organizations.
* 📦 **Data collected**:
  * *Personal info* (Name, Email address, Academic details)
  * *App activity* (Skill preferences, Swap requests, Scheduled sessions, Reviews)

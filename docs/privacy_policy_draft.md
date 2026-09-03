# Privacy Policy for SkillSwap Campus

**Effective Date:** September 3, 2026  
**Last Updated:** September 3, 2026

**SkillSwap Campus** ("we", "our", or "the App") is a peer-to-peer student skill exchange and time-bank learning application designed for college and university campuses. This Privacy Policy explains how we collect, use, store, process, and protect your information when you use our Android mobile application and associated web APIs.

---

## 1. Information We Collect

Based directly on the application's architecture and database implementation, we collect and store the following categories of personal and usage data:

### A. Account & Profile Information
* **Full Name**: Provided during registration to identify you to peers.
* **Institutional Email Address**: Collected for authentication and institutional student verification (`.edu` domain validation).
* **Password (Hashed)**: Cryptographically hashed using secure one-way hashing (`pbkdf2:sha256`) via Werkzeug. Plaintext passwords are never stored or logged.
* **Academic Profile**: Major/course of study, expected graduation year, college/university name, and optional biographical description ("Bio").

### B. Skills & Portfolio Information
* **Teaching Skills**: Subjects, technologies, or topics you offer to teach, along with self-reported proficiency levels (`beginner`, `intermediate`, `advanced`).
* **Learning Goals**: Subjects or skills you wish to learn from other students.

### C. Swap Requests & Communications
* **Exchange Invitations**: Records of swap requests sent and received between students.
* **User Messages**: Text notes and custom messages included in exchange proposals.
* **Request Statuses**: `pending`, `accepted`, `rejected`, or `cancelled`.

### D. Scheduled Learning Sessions
* **Session Records**: Teacher ID, Learner ID, Skill ID, scheduled date/time, duration in hours (e.g., `1.0`), meeting venue (e.g., campus library or online), and lifecycle status (`scheduled`, `completed`, `cancelled`).

### E. Time-Bank Credit Ledger & Transactions
* **Credit Balance**: Quantitative balance of exchange credits (all new users start with an initial 2.0 credits).
* **Ledger History**: Complete audit trail of credit transactions including transaction type (`hold_placement`, `session_earn`, `session_spend`, `hold_release`), amount, session references, and timestamps.

### F. Post-Session Reviews & Ratings
* **Feedback Data**: Numeric rating (1 to 5 stars) and optional feedback comments.
* **Double-Blind Mechanism**: Reviews remain confidential (`is_visible: false`) until both session participants submit their reviews, preventing retaliatory feedback.

### G. In-App Notifications
* **Alerts**: System notifications regarding incoming swap requests, session confirmations, and review unlocks, including read/unread status.

---

## 2. Information We DO NOT Collect

* **Financial & Payment Data**: We do not collect credit cards, bank accounts, or monetary transactions. The app operates exclusively on a non-monetary time-bank credit model.
* **Precise GPS Location**: We do not collect or track real-time device GPS coordinates.
* **Device Identifiers & Telemetry**: We do not collect advertising IDs (AAID), MAC addresses, or biometric data.
* **Contacts & Media Files**: We do not request access to device contacts, SMS, phone calls, camera, or external storage files.

---

## 3. How We Use Your Information

We use the collected information strictly for core application functionality:
1. **Authentication & Session Management**: To verify your student status, log you into the application securely, and maintain authenticated sessions.
2. **Peer Matching & Reciprocity**: To compute compatibility matches between students who want to teach what you want to learn, and vice versa.
3. **Session Scheduling & Credit Accounting**: To facilitate session agreements, manage credit holds during scheduled sessions, and transfer credits upon completion.
4. **Community Trust & Safety**: To display mutual ratings and academic profiles to establish peer accountability.
5. **In-App Communication**: To notify you of session status changes and peer requests.

---

## 4. How Your Information Is Shared

* **Peer Visibility**: Other registered students on the platform can view your public profile (name, major, bio, skills offered, skills desired, and public review history). Your email address and password hash are **never** displayed publicly to other users.
* **No Third-Party Data Selling or Advertising**: We do not sell, rent, monetize, or disclose your personal information to third-party advertisers, data brokers, or marketing partners.
* **Infrastructure Service Providers**: Data is stored securely in PostgreSQL databases hosted on cloud infrastructure adhering to industry-standard data protection protocols.

---

## 5. Data Security & Storage

* **Encryption in Transit**: All communication between the Android application and backend APIs is encrypted using HTTPS / TLS 1.3.
* **Session Security**: Authentication tokens and session cookies utilize secure flags (`HttpOnly`, `SameSite=Lax`, and `Secure` over HTTPS in production).
* **Database Protection**: Relational PostgreSQL database with strict foreign key constraints and validation rules.

---

## 6. User Rights & Account Deletion

You have the following rights regarding your data:
* **Access & Review**: You can view your complete profile, active sessions, and credit history within the app at any time.
* **Profile Editing**: You can update your skills, bio, major, and graduation year via the profile settings screen.
* **Account Deletion**: You may request complete deletion of your account, profile, skills, and session history by contacting our support team or submitting an in-app deletion request. Upon request, all associated personal records will be permanently removed from the active database.

---

## 7. Children's Privacy

SkillSwap Campus is intended exclusively for college and university students aged 18 and older. We do not knowingly collect personal data from individuals under 13 years of age.

---

## 8. Contact & Support Information

If you have questions, concerns, or data privacy requests regarding this policy:
* **Support Email**: `support@skillswapcampus.app` *(Placeholder - configure your official contact email)*
* **Project Repository / Website**: `https://skillswap-campus-api.onrender.com`

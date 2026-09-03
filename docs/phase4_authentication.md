# Phase 4 — Authentication & Onboarding

This document covers the technical design, registration workflows, session cookie security settings, onboarding APIs, testing coverage, and final verification metrics for Phase 4 of the **SkillSwap Campus** project.

---

## A. Authentication Architecture
The authentication system is built using Flask blueprints and secure, server-side session cookies. When a student authenticates, Flask encrypts session metadata using the application's cryptographically random `SECRET_KEY` and signs the response cookie sent back to the client. Subsequent requests verify the signature of the session cookie to identify and load the user.

---

## B. Registration Flow
1. **Endpoint**: `POST /api/auth/register`
2. **Payload**: `name`, `email`, `password`, `confirm_password`
3. **Flow**:
   * Validates that all fields are present.
   * Normalizes the email address (converted to lower case).
   * Verifies the email structure against a standard email validation regex.
   * Enforces that the email domain matches the configured `ALLOWED_EMAIL_DOMAIN` (defaulting to `.edu`).
   * Validates that the password is at least 6 characters in length and matches the password confirmation value.
   * Checks the database to prevent duplicate registration of the same email.
   * Hashes the password using **bcrypt** and saves the `User` record to PostgreSQL with an initial credit balance of `2.00` tokens.
   * Returns a generic JSON success response without exposing password hashes.

---

## C. Login Flow
1. **Endpoint**: `POST /api/auth/login`
2. **Payload**: `email`, `password`
3. **Flow**:
   * Normalizes input email (lowercased).
   * Queries the database for a user matching the email.
   * Verifies the password using `bcrypt` comparison functions.
   * If credentials are valid, clears the session and sets `session['user_id'] = user.id`.
   * Returns user profile fields.
   * If credentials fail, returns a generic `401 Unauthorized` response to prevent malicious email address discovery.

---

## D. Logout Flow
1. **Endpoint**: `POST /api/auth/logout`
2. **Flow**:
   * Invokes `session.clear()`, wiping the cookie metadata from the client session namespace.
   * Returns a JSON success message.

---

## E. Session Handling
Flask session cookies are configured with the following security flags in `config.py`:
* **HTTPOnly**: `True` (Prevents client-side scripts from reading the cookie values, mitigating XSS attacks).
* **SameSite**: `Lax` (Restricts cookie transmissions on cross-site requests, mitigating CSRF attacks).
* **Secure**: Configured via environment variables (Set to `True` in production to enforce SSL/HTTPS transit).

---

## F. Password Hashing
Password hashes are computed using **bcrypt**, a slow, salted key derivation function designed specifically to withstand brute-force attacks. Salt generation and hashing are handled dynamically during user object creation:
```python
salt = bcrypt.gensalt()
self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
```

---

## G. Email-Domain Validation
To limit access to campus students, the email domain is validated during signup. The allowed suffix is parsed from configuration parameters (`ALLOWED_EMAIL_DOMAIN`), enabling institutions to adjust suffix constraints (e.g. `.edu` or specific sub-domains like `@college.edu`).

---

## H. Onboarding Flow
Once a user is registered and logged in, they enter the onboarding flow where they complete their profiles, register their skills, and establish their weekly time slots.
1. **Endpoint**: `GET /api/onboarding/profile` & `POST /api/onboarding/profile`
2. **Requirements**:
   * Modifies only non-protected fields (`college`, `major`/`course`, `bio`, `grad_year`).
   * Blocks updates to protected fields (`id`, `email`, `credit_balance`, `password_hash`, `is_verified`, `created_at`), returning `403 Forbidden` if modified.

---

## I. Skills API
To populate onboarding skill pickers, the catalog endpoint lists available skills.
1. **Lookup Endpoint**: `GET /api/skills`
2. **Onboarding Update**: `POST /api/onboarding/skills`
   * Accepts lists of skills to teach and learn:
     ```json
     {
       "teach": [{"skill_id": 1, "proficiency": "advanced"}],
       "learn": [{"skill_id": 2, "proficiency": "beginner"}]
     }
     ```
   * Validates roles (`teach` or `learn`) and proficiencies (`beginner`, `intermediate`, `advanced`).
   * Verifies that all provided skill IDs exist.
   * Overwrites old mappings transactionally to align with onboarding profile revisions.

---

## J. Availability API
1. **Lookup**: `GET /api/onboarding/availability`
2. **Onboarding Update**: `POST /api/onboarding/availability`
   * Accepts list of time ranges:
     ```json
     [
       {"day_of_week": 1, "start_time": "09:00", "end_time": "11:00"}
     ]
     ```
   * Enforces that `day_of_week` is between 0 (Sunday) and 6 (Saturday).
   * Validates `start_time` is strictly before `end_time` and complies with `HH:MM` format.
   * Evaluates input intervals to prevent internal overlaps on the same day.

---

## K. API Endpoints
| HTTP Method | Path | Auth Required | Purpose |
|-------------|------|---------------|---------|
| `POST` | `/api/auth/register` | No | Register new student profile |
| `POST` | `/api/auth/login` | No | Authenticate user & start session |
| `POST` | `/api/auth/logout` | Yes | Invalidate session cookies |
| `GET` | `/api/auth/me` | Yes | Get currently logged-in user profile |
| `GET` | `/api/onboarding/profile` | Yes | Retrieve onboarding profile details |
| `POST` | `/api/onboarding/profile` | Yes | Update onboarding profile details |
| `GET` | `/api/skills` | No | Get available global skills catalog |
| `POST` | `/api/onboarding/skills` | Yes | Update user teach/learn portfolios |
| `GET` | `/api/onboarding/availability` | Yes | Get user weekly availability slots |
| `POST` | `/api/onboarding/availability` | Yes | Update user weekly availability slots |

---

## L. Database Changes
No new tables or fields were added. The existing columns in `users`, `skills`, `user_skills`, and `user_availabilities` tables match all required variables.

---

## M. Tests Performed
A complete test suite was run (`test_phase4.py`) checking the following 20 verification points:
1. Successful student account registration.
2. Rejection of invalid email formats.
3. Rejection of disallowed email domains (non-`.edu`).
4. Rejection of duplicate email registrations.
5. Rejection of password/confirmation mismatches.
6. Rejection of passwords under 6 characters.
7. Verification of successful logins.
8. Safe rejection of invalid login credentials.
9. Verification of authenticated profile lookup (/me).
10. Rejection of unauthenticated profile lookup (/me).
11. Verification that logging out invalidates session cookie access.
12. Verification that onboarding routes reject unauthenticated requests.
13. Creating and updating onboarding profile details.
14. Listing global skills catalog.
15. Selecting skills to teach.
16. Selecting skills to learn.
17. Rejecting updates containing non-existent skill IDs.
18. Registering weekly availability slot ranges.
19. Rejection of invalid time ranges (`start_time >= end_time`).
20. Isolation check: Authenticated users cannot update another student's profile records.

---

## N. Test Results
* **Test Status**: **PASS**
* **Total Checks**: 20
* **Success Rate**: 100%

---

## O. Security Considerations
* **No plaintext passwords**: All student credentials are encrypted via bcrypt.
* **CSRF and Session Hijacking prevention**: HttpOnly and SameSite flags are strictly configured.
* **Protected parameters**: Credit balances and verification flags are protected from modifications during onboarding profile updates.

---

## P. Known Limitations
* **Local Session Storage**: Flask sessions currently rely on cookie signing. If cookie payloads grow significantly, server-side caching (e.g. Redis/PostgreSQL backend sessions) will be required.

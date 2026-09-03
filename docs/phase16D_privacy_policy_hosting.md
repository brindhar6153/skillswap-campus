# Phase 16D — Privacy Policy Hosting & URL Specification

Google Play requires all applications that handle personal user data to provide a publicly accessible, valid HTTPS Privacy Policy link.

---

## 1. Privacy Policy URL Placeholder

```text
PRIVACY POLICY URL:
<TO_BE_HOSTED>
```

*(Enter the final public HTTPS URL where you host the policy into the Play Console under **App content → Privacy policy**).*

---

## 2. Policy Source & Content

* The authoritative privacy policy text is prepared at:
  [`docs/privacy_policy_draft.md`](file:///c:/Users/BRINDHA/OneDrive/Desktop/New%20folder%20-%20Copy%20(2)/docs/privacy_policy_draft.md)
* It accurately describes:
  * `.edu` email collection & verification
  * One-way password hashing (`pbkdf2:sha256`)
  * Skills portfolio, swap requests, session scheduling, and time-bank credit accounting
  * Double-blind mutual reviews
  * 0 third-party data sharing
  * HTTPS in-transit encryption
  * Account deletion & retention practices

---

## 3. Recommended Hosting Options

### Option A: Flask Backend Public Route (Recommended)
* Your live production backend `https://skillswap-campus-api.onrender.com` can serve this policy at `https://skillswap-campus-api.onrender.com/privacy` as a clean HTML page.
* Benefits: Matches your API domain, requires no extra hosting accounts, and provides 100% HTTPS uptime.

### Option B: GitHub Pages / Static Site
* You can host the markdown or HTML on GitHub Pages (e.g., `https://<your-username>.github.io/skillswap-privacy`).
* Free, permanent, and supports HTTPS by default.

### Option C: Notion / Google Sites / Public Document
* A publicly accessible Google Doc or Notion public web page can also serve as the privacy policy URL if public sharing is enabled.

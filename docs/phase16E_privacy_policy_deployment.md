# Phase 16E — Privacy Policy Deployment Guide

This document outlines the privacy policy route implementation, local verification status, and production deployment procedure for **SkillSwap Campus**.

---

## 1. Route Implementation & Local Status

* **Route Implemented**: `GET /privacy` and `GET /api/privacy` in `backend/app/routes/health.py`
* **Response Format**: Clean, responsive, mobile-friendly HTML (`text/html; charset=utf-8`)
* **Local Test URL**: `http://127.0.0.1:5000/privacy`
* **Local Verification Status**: **PASS (HTTP 200 OK)**

---

## 2. Production URL Status

```text
https://skillswap-campus-api.onrender.com/privacy
STATUS: REQUIRES DEPLOYMENT/VERIFICATION
```

*(The `/privacy` code has been added to the local backend. Once the codebase is pushed to your connected Git repository, Render will automatically deploy the updated backend).*

---

## 3. Deployment Procedure for Account Holder

To make the privacy policy publicly live on Render:

1. **Commit and Push Backend Changes**:
   * Commit the modified `backend/app/routes/health.py` to your GitHub/GitLab repository.
2. **Render Automatic Deployment**:
   * Render automatically triggers a new deployment upon receiving the new commit.
3. **Verify Public URL**:
   * Open `https://skillswap-campus-api.onrender.com/privacy` in your browser.
   * Verify that the page loads with the header **"🎓 SkillSwap Campus - Privacy Policy"**.
4. **Enter in Google Play Console**:
   * Enter `https://skillswap-campus-api.onrender.com/privacy` into the **App content → Privacy policy** section of Google Play Console.

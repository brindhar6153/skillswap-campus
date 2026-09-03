# Phase 17 — Manual Production Deployment Steps for Repository Owner

This document provides step-by-step instructions for the repository owner to deploy the latest privacy policy route to Render and verify live public endpoints before completing the Google Play submission.

---

## 7-Step Deployment & Verification Workflow

### Step 1: Commit Privacy Route Changes
Open your terminal or Git client in the repository directory and stage the updated backend files:
```bash
git add backend/app/routes/health.py backend/run.py .gitignore
git commit -m "feat(backend): add public /privacy HTML route and production host binding"
```

---

### Step 2: Push to Remote Git Repository
Push your commit to your remote branch (e.g. `main`):
```bash
git push origin main
```

---

### Step 3: Wait for Render Automatic Deployment
* Open your [Render Dashboard](https://dashboard.render.com).
* Select your `skillswap-campus-api` Web Service.
* Wait until the deployment status changes to **"Live"** (typically takes 1-2 minutes).

---

### Step 4: Verify the Production `/health` URL
Open in your browser or terminal:
```text
https://skillswap-campus-api.onrender.com/health
```
**Expected Response**:
```json
{
  "database": "connected",
  "status": "ok"
}
```

---

### Step 5: Verify the Production `/privacy` URL
Open in your browser:
```text
https://skillswap-campus-api.onrender.com/privacy
```
**Expected Result**:
* A responsive, mobile-friendly webpage titled **"🎓 SkillSwap Campus - Privacy Policy"** appears.

---

### Step 6: Confirm Both Endpoints are Live
* Once both `/health` and `/privacy` return HTTP 200 over HTTPS, your production backend is 100% verified.

---

### Step 7: Proceed to Google Play Console
* Open [Google Play Console](https://play.google.com/console).
* Follow the 26-step manual submission walkthrough in:
  [`docs/phase16D_manual_play_console_walkthrough.md`](file:///c:/Users/BRINDHA/OneDrive/Desktop/New%20folder%20-%20Copy%20(2)/docs/phase16D_manual_play_console_walkthrough.md)
* Enter `https://skillswap-campus-api.onrender.com/privacy` in **App content → Privacy policy**.
* Upload `dist/SkillSwapCampus-final.aab` under **Release → Production**.

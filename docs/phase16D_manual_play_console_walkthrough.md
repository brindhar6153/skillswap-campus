# Phase 16D — Beginner-Friendly Google Play Console Manual Walkthrough

This guide provides a comprehensive 26-step manual submission walkthrough for the authorized developer account holder.

---

## Legend
* `[MANUAL ACTION REQUIRED]` — Action you must perform directly in the Google Play Console web interface.
* `[AUTOMATED PROJECT PREPARATION]` — Resource or file already created, compiled, and verified in your project workspace.

---

## 26-Step Submission Walkthrough

### Step 1: Open Google Play Console
* `[MANUAL ACTION REQUIRED]` Open your browser and navigate to [https://play.google.com/console](https://play.google.com/console). Sign in with your registered Google developer account.

### Step 2: Create Application
* `[MANUAL ACTION REQUIRED]` On the **All apps** page, click the blue **Create app** button in the top-right corner.

### Step 3: Enter App Name
* `[MANUAL ACTION REQUIRED]` Under **App name**, type: `SkillSwap Campus`.
* `[AUTOMATED PROJECT PREPARATION]` Prepared in `docs/phase16D_app_creation_information.md`.

### Step 4: Select App Type
* `[MANUAL ACTION REQUIRED]` Under **App or game**, select **App**.

### Step 5: Select Free or Paid
* `[MANUAL ACTION REQUIRED]` Under **Free or paid**, select **Free**.

### Step 6: Accept Required Declarations
* `[MANUAL ACTION REQUIRED]` Check the compliance boxes for **Developer Program Policies** and **US export laws**, then click **Create app**.

### Step 7: Open App Dashboard
* `[MANUAL ACTION REQUIRED]` You are now on the **SkillSwap Campus Dashboard**. Click **View tasks** under **Set up your app**.

### Step 8: Complete Main Store Listing
* `[MANUAL ACTION REQUIRED]` Navigate to **Grow → Store presence → Main store listing** in the left navigation sidebar.

### Step 9: Enter App Name (Store Listing)
* `[MANUAL ACTION REQUIRED]` Confirm the **App name** is set to `SkillSwap Campus`.

### Step 10: Enter Short Description
* `[MANUAL ACTION REQUIRED]` Paste: `Peer-to-peer student skill sharing & time-bank learning exchange for campuses.` into the **Short description** field.
* `[AUTOMATED PROJECT PREPARATION]` Prepared in `docs/phase16D_store_listing.md` (78 / 80 chars).

### Step 11: Enter Full Description
* `[MANUAL ACTION REQUIRED]` Copy and paste the complete description from `docs/phase16D_store_listing.md` into the **Full description** box.

### Step 12: Upload App Icon
* `[MANUAL ACTION REQUIRED]` Under **App icon**, click **Upload** and select:
  `dist/play_store_assets/app_icon_512x512.png`
* `[AUTOMATED PROJECT PREPARATION]` Icon generated with exact 512x512 PNG specifications.

### Step 13: Upload Screenshots
* `[MANUAL ACTION REQUIRED]` Under **Phone screenshots**, upload the 6 images from `dist/play_store_assets/` in order:
  1. `screenshot_1_login_register.png`
  2. `screenshot_2_dashboard.png`
  3. `screenshot_3_skills.png`
  4. `screenshot_4_matches.png`
  5. `screenshot_5_requests.png`
  6. `screenshot_6_sessions_profile.png`

### Step 14: Upload Feature Graphic
* `[MANUAL ACTION REQUIRED]` Under **Feature graphic**, click **Upload** and select:
  `dist/play_store_assets/feature_graphic_1024x500.png`

### Step 15: Add Privacy Policy URL
* `[MANUAL ACTION REQUIRED]` Navigate to **Policy and programs → App content → Privacy policy**. Enter your public HTTPS URL hosting `docs/privacy_policy_draft.md`.
* `[AUTOMATED PROJECT PREPARATION]` Hosting guide provided in `docs/phase16D_privacy_policy_hosting.md`.

### Step 16: Complete App Content Declarations
* `[MANUAL ACTION REQUIRED]` Under **App content**, complete Ads (Select **"No ads"**), Financial features (**"No"**), and Government apps (**"No"**).
* `[AUTOMATED PROJECT PREPARATION]` Verified answers listed in `docs/phase16D_app_content_answers.md`.

### Step 17: Complete Data Safety Questionnaire
* `[MANUAL ACTION REQUIRED]` Open **App content → Data safety** and fill out the questionnaire.
* `[AUTOMATED PROJECT PREPARATION]` Exact question-by-question mapping documented in `docs/phase16D_data_safety_verification.md`.

### Step 18: Complete Content Rating (IARC)
* `[MANUAL ACTION REQUIRED]` Open **App content → Content rating**, start the questionnaire, enter your email, and submit.
* `[AUTOMATED PROJECT PREPARATION]` Answers detailed in `docs/google_play_content_rating.md`.

### Step 19: Configure Target Audience
* `[MANUAL ACTION REQUIRED]` Open **App content → Target audience** and select **18 and over** (or 16-17/18+ depending on your campus preference).
* `[AUTOMATED PROJECT PREPARATION]` Detailed recommendation in `docs/phase16D_app_content_answers.md`.

### Step 20: Configure App Access (Reviewer Login)
* `[MANUAL ACTION REQUIRED]` Open **App content → App access**, select **"Restricted functionality"**, click **Add instructions**, and paste demo credentials.
* `[AUTOMATED PROJECT PREPARATION]` Reviewer instructions prepared in `docs/phase16D_reviewer_access.md`.

### Step 21: Configure Testing (If Required)
* `[MANUAL ACTION REQUIRED]` Navigate to **Testing → Internal testing** (and Closed testing if mandated by your account status).
* `[AUTOMATED PROJECT PREPARATION]` Testing plan outlined in `docs/phase16D_testing_plan.md`.

### Step 22: Create Release
* `[MANUAL ACTION REQUIRED]` Go to **Release → Production** (or **Testing → Internal testing**) and click **Create new release**.

### Step 23: Upload Final AAB
* `[MANUAL ACTION REQUIRED]` Under **App bundles**, click **Upload** and select:
  `dist\SkillSwapCampus-final.aab`
* `[AUTOMATED PROJECT PREPARATION]` Final verified signed release bundle prepared in `dist/`.

### Step 24: Review Warnings / Errors
* `[MANUAL ACTION REQUIRED]` Google Play will automatically analyze the AAB. Verify 0 blocking errors.
* `[AUTOMATED PROJECT PREPARATION]` Bundle verified with Target SDK 36, Min SDK 24, and RSA 2048 signing.

### Step 25: Save Release
* `[MANUAL ACTION REQUIRED]` Enter release name `1.0.0 (1)`, add release notes, and click **Save** / **Next**.

### Step 26: Submit for Review
* `[MANUAL ACTION REQUIRED]` Click **Review release** → **Start rollout to Production** (or **Submit for review**). The status will change to **"In review"**.

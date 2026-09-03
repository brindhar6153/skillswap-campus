# Phase 16B — Manual Google Play Console Submission Walkthrough

This document outlines the exact, step-by-step manual process that an authorized adult account holder must perform in the [Google Play Console](https://play.google.com/console) to publish **SkillSwap Campus**.

> [!IMPORTANT]
> **Important Compliance Notes:**
> * You must be 18 years of age or older and possess an active Google Play Developer Account ($25 one-time registration fee).
> * Do NOT attempt to automate Google account creation, identity verification, or billing.
> * Completing these steps submits the application for standard Google review (typically 24 to 72 hours). The app is **not** published until Google explicitly reviews and approves your submission.

---

## 20-Step Submission Walkthrough

### Step 1 — Open Google Play Console
* Log in to [https://play.google.com/console](https://play.google.com/console) using your developer Google Account.

### Step 2 — Create the Application
* From the **All apps** tab on the main dashboard, click the blue **Create app** button in the top right corner.

### Step 3 — Enter App Name & Details
* **App name**: Enter `SkillSwap Campus`.
* **Default language**: Select `English (United States) - en-US`.

### Step 4 — Select Application Type & Free/Paid Status
* **App or game**: Select **App**.
* **Free or paid**: Select **Free** (The application uses a non-monetary credit time-bank model).

### Step 5 — Complete Initial Declarations
* Check the boxes confirming compliance with:
  * ☑ **Developer Program Policies**
  * ☑ **US export laws**
* Click **Create app** at the bottom right.

### Step 6 — Open the App Dashboard
* You will now be redirected to the app dashboard for **SkillSwap Campus**.
* Under the **Set up your app** task list, click **View tasks**.

### Step 7 — Complete Privacy Policy URL
* Click **Set privacy policy**.
* Enter your public HTTPS privacy policy URL (e.g., hosted from `docs/privacy_policy_draft.md`).
* Click **Save**.

### Step 8 — Configure App Access (Reviewer Login)
* Click **App access**.
* Select **"All or some functionality in my app is restricted"**.
* Click **Add instructions** and enter the demo reviewer credentials as documented in `docs/play_review_access.md`.
* Click **Save**.

### Step 9 — Complete Ads Declaration
* Click **Ads**.
* Select **"No, my app does not contain ads"**.
* Click **Save**.

### Step 10 — Complete Content Rating (IARC)
* Click **Content rating** and select **Start questionnaire**.
* Enter your developer email address.
* Category: Select **Utility, Productivity, Communication, or Other** (or **Education**).
* Complete the questionnaire using the answers in `docs/google_play_content_rating.md` (No violence, no profanity, users interact).
* Click **Save** → **Next** → **Submit**.

### Step 11 — Configure Target Audience
* Click **Target audience and content**.
* Select target age group: **18 and over** (University students).
* Neutral age screen / Appeal to children: Select **No**.
* Click **Next** → **Save**.

### Step 12 — Complete Data Safety Form
* Click **Data safety**.
* Follow the exact questionnaire mappings provided in `docs/google_play_data_safety.md`:
  * Data collected: Name, Email address, App activity (skills, sessions, reviews).
  * Data shared: No.
  * Encrypted in transit: Yes (HTTPS).
  * Deletion request mechanism: Yes.
* Click **Save** → **Submit**.

### Step 13 — Complete Store Settings & Category
* Navigate to **Grow → Store presence → Store settings**.
* **App category**: Select **Education**.
* **Tags**: Add tags (`Education`, `Productivity`, `Communication`).
* **Manage contact details**: Enter your developer contact email and website URL (`https://skillswap-campus-api.onrender.com`).
* Click **Save**.

### Step 14 — Complete Main Store Listing Copy
* Navigate to **Grow → Store presence → Main store listing**.
* Copy and paste the text from `docs/google_play_store_listing_final.md`:
  * **App name**: `SkillSwap Campus`
  * **Short description**: `Peer-to-peer student skill sharing & time-bank learning exchange for campuses.`
  * **Full description**: *(Paste the formatted 4,000-character description)*.

### Step 15 — Upload App Icon (512x512)
* Under **App icon**, click **Upload**.
* Select `dist/play_store_assets/app_icon_512x512.png`.

### Step 16 — Upload Feature Graphic (1024x500)
* Under **Feature graphic**, click **Upload**.
* Select `dist/play_store_assets/feature_graphic_1024x500.png`.

### Step 17 — Upload Phone Screenshots
* Under **Phone screenshots**, click **Upload**.
* Select the 6 PNG screenshots in sequence:
  1. `screenshot_1_login_register.png`
  2. `screenshot_2_dashboard.png`
  3. `screenshot_3_skills.png`
  4. `screenshot_4_matches.png`
  5. `screenshot_5_requests.png`
  6. `screenshot_6_sessions_profile.png`
* Click **Save** at the bottom of the page.

### Step 18 — Upload Final Release AAB
* Navigate to **Release → Production** (or **Testing → Internal testing** for pre-release validation).
* Click **Create new release**.
* Under **App bundles**, click **Upload**.
* Select the final signed production bundle:
  ```text
  dist\SkillSwapCampus-final.aab
  ```
* **Release name**: `1.0.0 (1)`
* **Release notes**:
  ```text
  Initial official release of SkillSwap Campus!
  - Peer-to-peer campus skill exchange network
  - Institutional .edu email authentication
  - Reciprocal skill matching algorithm
  - Time-bank credit economy
  - Post-session double-blind peer reviews
  ```
* Click **Next** / **Save**.

### Step 19 — Review Pre-Launch Warnings & Validation
* Google Play will automatically analyze the AAB bundle and generate an automated report.
* Verify there are **0 errors**. (Minor warnings regarding Proguard mapping or non-critical SDK notifications can be reviewed).

### Step 20 — Submit for Review
* Click **Review release**.
* Click **Start rollout to Production** (or submit to closed testing).
* The release status will change to **"In review"**.
* Once Google completes the review process (usually 1-3 business days), your app will become **Available on Google Play**.

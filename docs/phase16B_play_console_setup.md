# Phase 16B — Google Play Console Submission Preparation Guide

This master preparation guide provides the complete administrative and technical setup required for submitting **SkillSwap Campus** to the Google Play Console.

---

## 1. Application Identification & Metadata

| Field | Configured Value | Note |
| :--- | :--- | :--- |
| **App Name** | `SkillSwap Campus` | Display title on Google Play (16 chars) |
| **Application ID / Package Name** | `com.example.skillswapcampus` | Fixed unique package identifier |
| **Version Name** | `1.0.0` | Public semantic release version |
| **Version Code** | `1` | Internal build sequence code |
| **Application Type** | `App` | Non-game utility |
| **Pricing** | `Free` | No in-app purchases or downloads fee |
| **Primary Category** | `Education` | Under Education in Play Store |
| **Secondary Category** | `Productivity` | Secondary tag |
| **Short Description** | *Peer-to-peer student skill sharing & time-bank learning exchange for campuses.* | 78 / 80 characters |
| **Full Description** | *(See `docs/google_play_store_listing_final.md` for complete 4,000-character copy)* | Clean, verified feature list |

---

## 2. Technical Release Information

| Parameter | Value | Verification Status |
| :--- | :--- | :--- |
| **Signed Release AAB Path** | `dist\SkillSwapCampus-final.aab` | **VERIFIED SIGNED** (`12.56 MB`) |
| **Signed Release APK Path** | `dist\SkillSwapCampus-final.apk` | **VERIFIED SIGNED** (`12.92 MB`) |
| **Minimum Android SDK** | `24` | Android 7.0 (Nougat) and higher |
| **Target Android SDK** | `36` | Android 16 (Complies with Google Play modern API level policies) |
| **Compile Android SDK** | `36` | Java 17 toolchain |
| **Production Backend URL** | `https://skillswap-campus-api.onrender.com` | Verified HTTPS over TLS 1.3 |
| **Network Audit** | 0 local IPs found | No dependency on localhost or private LAN |
| **Signing Algorithm** | RSA 2048-bit / SHA384withRSA | Valid until 2054 (10,000 days validity) |

---

## 3. Store Listing Visual Assets

All visual assets are pre-formatted and stored in `dist/play_store_assets/`:

| Asset Filename | Dimensions | Aspect Ratio | Max Size Limit | Actual Size | Purpose in Play Console |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `app_icon_512x512.png` | **512 x 512 px** | 1:1 | 1024 KB | 248 KB | Official app icon for Google Play search & store page |
| `feature_graphic_1024x500.png` | **1024 x 500 px** | 1024:500 | 15 MB | 52 KB | Promotional banner displayed at the top of the store listing |
| `screenshot_1_login_register.png` | **1080 x 1920 px** | 9:16 | 8 MB | 77 KB | Phone Screenshot 1: Verified student `.edu` authentication |
| `screenshot_2_dashboard.png` | **1080 x 1920 px** | 9:16 | 8 MB | 83 KB | Phone Screenshot 2: Time-bank credit dashboard & alert feed |
| `screenshot_3_skills.png` | **1080 x 1920 px** | 9:16 | 8 MB | 85 KB | Phone Screenshot 3: Skills portfolio & proficiency badges |
| `screenshot_4_matches.png` | **1080 x 1920 px** | 9:16 | 8 MB | 85 KB | Phone Screenshot 4: 100% reciprocal peer match cards |
| `screenshot_5_requests.png` | **1080 x 1920 px** | 9:16 | 8 MB | 72 KB | Phone Screenshot 5: Swap proposals & invitation negotiation |
| `screenshot_6_sessions_profile.png` | **1080 x 1920 px** | 9:16 | 8 MB | 84 KB | Phone Screenshot 6: 1-on-1 tutoring sessions, ledger & ratings |

---

## 4. Google Play Console Setup Checklist

Use this operational checklist when configuring the application in [Google Play Console](https://play.google.com/console):

- [ ] **1. Developer Account**: Ensure the one-time \$25 USD developer fee is paid and developer identity verification is complete.
- [ ] **2. Create App**: Title: `SkillSwap Campus`, Type: `App`, Status: `Free`.
- [ ] **3. Store Listing Copy**: Copy and paste finalized text from `docs/google_play_store_listing_final.md`.
- [ ] **4. Store Listing Assets**: Upload `app_icon_512x512.png`, `feature_graphic_1024x500.png`, and the 6 phone screenshots.
- [ ] **5. Category & Tags**: Category `Education`, Secondary `Productivity`, Tags: `Education`, `Productivity`, `Communication`.
- [ ] **6. Contact Information**: Enter developer contact email and support website (`https://skillswap-campus-api.onrender.com`).
- [ ] **7. Privacy Policy**: Enter the public URL hosting `docs/privacy_policy_draft.md`.
- [ ] **8. Data Safety**: Complete the questionnaire using the exact mappings in `docs/google_play_data_safety.md` (no data shared with third parties, HTTPS encrypted).
- [ ] **9. Content Rating**: Complete the IARC questionnaire using `docs/google_play_content_rating.md`.
- [ ] **10. Target Audience**: Select `18 and over` (University / College students).
- [ ] **11. App Access / Reviewer Credentials**: Under **App content → App access**, provide test credentials as outlined in `docs/play_review_access.md`.
- [ ] **12. AAB Upload**: Upload `dist/SkillSwapCampus-final.aab` to **Testing → Internal testing** (or **Release → Production**).
- [ ] **13. Rollout**: Review pre-launch report and click **Start rollout to Production**.

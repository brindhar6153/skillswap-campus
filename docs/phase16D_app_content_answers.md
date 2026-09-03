# Phase 16D — Google Play App Content Questionnaire Answers

This document provides the exact verified responses to all mandatory declaration questionnaires under **Policy and programs → App content** in the Google Play Console.

---

## 1. Declarations Summary Matrix

| Section in Play Console | Recommended Response | Codebase & Policy Justification | Status |
| :--- | :--- | :--- | :--- |
| **Privacy Policy** | Provide valid HTTPS URL | Host `docs/privacy_policy_draft.md` at public URL. | **READY (Provide URL)** |
| **Ads** | **"No, my app does not contain ads"** | No AdMob, Unity Ads, or advertising SDKs exist in the project. | **READY** |
| **App Access** | **"All or some functionality is restricted"** | Provide test student login as outlined in `docs/phase16D_reviewer_access.md`. | **READY** |
| **Content Rating (IARC)** | Complete Questionnaire | Utility/Social interaction. No violence, gambling, or vulgarity. | **READY** |
| **Target Audience** | **18 and over** *(or 16-17 / 18+)* | University and college students. See detailed analysis in Section 2. | **REQUIRES MANUAL CONFIRMATION** |
| **Data Safety** | Complete Form | Data collected for app functionality only; 0 third-party sharing. | **READY** |
| **Government Apps** | **"No"** | SkillSwap Campus is not developed by or representing a government agency. | **READY** |
| **Financial Features** | **"No financial features"** | No real-money banking, loans, investments, or credit cards. The time-bank is a non-monetary learning credit system. | **READY** |
| **Health & Medical** | **"No health features"** | The app provides no medical advice or health tracking. | **READY** |
| **Gambling / Real Prize** | **"No"** | No simulated or real-money gambling features. | **READY** |
| **News Apps** | **"No"** | Not a news distribution application. | **READY** |
| **COVID-19 Contact Tracing** | **"No"** | No contact tracing or health status features. | **READY** |
| **Child-Directed Content** | **"No"** | App is designed for university students and does not target children. | **READY** |
| **User-Generated Content (UGC)** | **"Yes"** | Students create custom bios, request notes, and peer review text. | **READY** |

---

## 2. Target Audience Recommendation & Manual Decision

* **Intended User Base**: College and university students requiring `.edu` institutional email addresses.
* **Age Distribution**:
  * The vast majority of college students are **18 and older**.
  * A small percentage of early-enrollment college students are **17 years old**.
* **Recommendation**:
  * Selecting **18 and over** is the most straightforward option and eliminates requirements for Google Play's Families Policy and neutral age screens.
  * If the account holder wishes to officially include 17-year-old college freshmen, select **16-17 and 18+**, and declare that the app is not primarily directed to children under 13.
* **Status**: `REQUIRES MANUAL CONFIRMATION` by the account holder during Play Console setup.

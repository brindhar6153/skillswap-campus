# Phase 16E — Google Play Console Readiness Summary

This document summarizes the final parameters and safety protocols for submitting **SkillSwap Campus** to Google Play.

---

## 1. Release Specification

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| **App Name** | `SkillSwap Campus` | Display title on Google Play |
| **Application ID** | `com.example.skillswapcampus` | Compiled package identifier |
| **App Type** | `Android application` | Non-game utility / Education |
| **Price** | `Free` | No download charge or monetary paywall |
| **Final Release AAB** | `dist/SkillSwapCampus-final.aab` | Signed with production RSA 2048-bit key (12.56 MB) |
| **Store Visual Assets** | `dist/play_store_assets/` | Icon, Feature Graphic, 6 Screenshots |
| **Privacy Policy Status** | `REQUIRES PUBLIC URL VERIFICATION` | Code implemented at `/privacy`; requires deployment to Render |

---

## 2. Account Safety & Policy Compliance

> [!IMPORTANT]
> **Manual Account Holder Requirement:**
> All Google Play Console actions (registration, fee payment, identity verification, questionnaire submissions, and release rollouts) must be executed **manually by an authorized adult account holder**.
> 
> * **Age & Identity Verification**: Google Play requires developers to be at least 18 years old and verify their legal identity with official government documents.
> * **Parental / Guardian Representation**: If the primary project creator is under 18 years of age, an eligible parent, legal guardian, or authorized adult must own and manage the Google Play Developer Account.
> * **No Automated Credential Access**: AI assistants and automation tools must never access OTPs, bank cards, developer passwords, or identity records.

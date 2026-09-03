# Google Play Store Graphics & Visual Assets Checklist

This checklist specifies the exact technical requirements and recommended visual layouts for publishing **SkillSwap Campus** on the Google Play Store.

---

## 1. App Icon Specification

| Requirement | Value | Technical Detail |
| :--- | :--- | :--- |
| **Format** | PNG (32-bit with alpha channel) | No transparency in background; full bleed |
| **Dimensions** | **512 x 512 px** | Exact square |
| **Max File Size** | **1024 KB (1 MB)** | Optimize with PNG compression |
| **Visual Design** | SkillSwap Campus Logo | Graduation cap / interconnected swap arrows with primary indigo/teal theme |

---

## 2. Feature Graphic Specification

| Requirement | Value | Technical Detail |
| :--- | :--- | :--- |
| **Format** | JPEG or 24-bit PNG (no alpha) | High-contrast visual banner |
| **Dimensions** | **1024 x 500 px** | Landscape banner |
| **Max File Size** | **15 MB** | Typically < 1 MB |
| **Recommended Content** | Brand Title & Tagline | *"SkillSwap Campus — Peer-to-Peer Student Learning & Time-Bank Exchange"* with clean modern background matching app color scheme. |

---

## 3. Phone Screenshots Specification

* **Quantity**: Minimum 4 required, 6 recommended.
* **Format**: JPEG or 24-bit PNG.
* **Aspect Ratio**: 16:9 or 18:9 / 19.5:9 portrait (e.g., `1080 x 1920 px` or `1080 x 2400 px`).
* **Minimum Dimension**: 320 px | **Maximum Dimension**: 3840 px.

### Recommended Screenshot Flow (Matching Existing Jetpack Compose UI):

```
┌─────────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐
│  1. Student Auth        │   │  2. Skill Portfolio     │   │  3. Reciprocal Match    │
│                         │   │                         │   │                         │
│  [SkillSwap Campus]     │   │  [Teach & Learn Skills] │   │  [Peer Matches (100%)]  │
│  • Institutional .edu   │   │  • Python (Advanced)    │   │  • Alice Smith (CS)     │
│  • Fast & Secure Login  │   │  • Calculus (Beginner)  │   │  • Teaches Python       │
│  • 2.0 Free Credits     │   │  • French (Intermediate)│   │  • Wants Calculus       │
└─────────────────────────┘   └─────────────────────────┘   └─────────────────────────┘
┌─────────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐
│  4. Swap Requests       │   │  5. Scheduled Sessions  │   │  6. Reviews & Ledger    │
│                         │   │                         │   │                         │
│  [Incoming & Outgoing]  │   │  [Campus Study Booking] │   │  [Time-Bank Balance]    │
│  • Instant Accept/Decline│  │  • Library Room 3B      │   │  • 3.0 Credits Active   │
│  • Custom invitation msg│   │  • 1.0 Hour Duration    │   │  • Double-Blind Ratings │
│  • Real-time updates    │   │  • Automated Escrow     │   │  • Verified Reviews     │
└─────────────────────────┘   └─────────────────────────┘   └─────────────────────────┘
```

#### Detailed Description of the 6 Screenshot Captures:
1. **Screenshot 1 — Verified Student Authentication**:
   * *Screen*: Registration / Login screen.
   * *Headline Caption*: *"Campus-Verified Student Network"*
   * *Visual*: Clean login interface highlighting `.edu` verification and instant account onboarding.

2. **Screenshot 2 — Skills Catalog & Profile Setup**:
   * *Screen*: Skill Onboarding screen.
   * *Headline Caption*: *"Teach What You Know, Learn What You Need"*
   * *Visual*: Selection chips for Python, Calculus, Web Development, Organic Chemistry, and Languages with proficiency badges.

3. **Screenshot 3 — Smart Reciprocal Matching**:
   * *Screen*: Matches Explorer screen.
   * *Headline Caption*: *"Discover 100% Compatible Study Partners"*
   * *Visual*: Match cards showing mutual skill reciprocity, compatibility scores, student majors, and graduation years.

4. **Screenshot 4 — Swap Request Invitations**:
   * *Screen*: Swap Requests screen.
   * *Headline Caption*: *"Propose & Accept Skill Swaps in Seconds"*
   * *Visual*: Incoming and Outgoing request tabs with proposal messages and interactive Accept/Decline actions.

5. **Screenshot 5 — Session Scheduling & Venue Planning**:
   * *Screen*: Session Detail & Schedule screen.
   * *Headline Caption*: *"Book 1-on-1 Sessions Online or on Campus"*
   * *Visual*: Scheduled session card showing venue (e.g., Campus Library Room 3B), scheduled time, and credit hold.

6. **Screenshot 6 — Time-Bank Credit Economy & Mutual Reviews**:
   * *Screen*: Profile & Credit History screen.
   * *Headline Caption*: *"Earn Credits by Teaching, Unlock Mutual Reviews"*
   * *Visual*: Credit balance counter (e.g., 3.0 credits), transaction audit trail, and 5-star double-blind student ratings.

---

## 4. How to Capture Live High-Resolution Screenshots

To capture pixel-perfect screenshots directly from your connected device or emulator:
```powershell
# Capture screenshot on connected device
adb shell screencap -p /sdcard/screenshot1.png

# Pull screenshot to computer
adb pull /sdcard/screenshot1.png ./docs/screenshots/screenshot1.png
```
*(Screenshots can then be framed with mockup tools or uploaded directly to Google Play Console).*

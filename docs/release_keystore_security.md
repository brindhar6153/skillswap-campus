# Release Keystore Security & Production Signing Best Practices

## 1. Important Security Notice

During development and automated build pipeline testing in Phase 13, a temporary local keystore was generated to verify that the Android Gradle build system could successfully produce signed `.aab` (Android App Bundle) and `.apk` packages.

> [!CAUTION]
> **Before uploading the official production app to the Google Play Console for real users, you should generate your own private, permanent release keystore and keep your signing credentials strictly confidential.**
> 
> * Never commit `.jks`, `.keystore`, or `keystore.properties` files to Git.
> * Never share or paste release keystore passwords in chats, scripts, or public repositories.
> * Always store a secure backup of your permanent production `.jks` file in a secure password manager or encrypted backup.

---

## 2. Generating Your Private Production Keystore

Run the standard Java `keytool` command in your terminal. `keytool` will interactively prompt you to choose a strong password privately without displaying it:

```powershell
# Run keytool interactively (it will prompt for passwords privately)
keytool -genkeypair -v -keystore my-production-release-key.jks -alias skillswap_production_key -keyalg RSA -keysize 2048 -validity 10000
```

During the prompt, provide:
1. Keystore password (choose a strong passphrase of 16+ characters).
2. Developer name, organization, and location details.
3. Confirmation (`yes`).

---

## 3. Configuring Local `keystore.properties`

On your local development machine (inside the `android/` directory):
1. Update `android/keystore.properties` (or copy from `android/keystore.properties.example`):
   ```properties
   storeFile=../my-production-release-key.jks
   storePassword=YOUR_PRIVATE_KEYSTORE_PASSWORD
   keyAlias=skillswap_production_key
   keyPassword=YOUR_PRIVATE_KEY_PASSWORD
   ```
2. Verify that `android/.gitignore` contains:
   ```text
   keystore.properties
   *.jks
   *.keystore
   ```
   *(This ensures your private credentials remain 100% on your local machine and are never pushed to Git).*

---

## 4. Rebuilding the Final Production Release AAB

Once your private keystore is configured in `keystore.properties`, build the final signed production Android App Bundle:

```powershell
cd android
.\gradlew.bat clean
.\gradlew.bat bundleRelease
```

The newly signed production bundle will be generated at:
```text
android/app/build/outputs/bundle/release/app-release.aab
```

---

## 5. Google Play App Signing (Recommended)

When you create your app release in the Google Play Console:
1. Google Play Console utilizes **Play App Signing** by default.
2. When you upload your signed AAB for the first time, Google securely registers your upload key.
3. If you ever lose your local upload key in the future, Google Play Developer Support can reset your upload key as long as Play App Signing is enabled.

# Firebase Authentication Setup Guide

This guide will help you set up Firebase Authentication for Money Matrix.

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project" or select an existing project
3. Follow the setup wizard:
   - Enter project name: "Money Matrix"
   - Enable Google Analytics (optional)
   - Create project

## Step 2: Register Your Web App

1. In Firebase Console, click the **Web icon** (`</>`) to add a web app
2. Register app:
   - App nickname: "Money Matrix Web"
   - Check "Also set up Firebase Hosting" (optional)
   - Click "Register app"
3. **Copy the firebaseConfig object** shown on the screen

## Step 3: Configure Frontend

1. Open `static/js/firebase-config.js`
2. Replace the `firebaseConfig` object with your actual config:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_ACTUAL_API_KEY",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef"
};
```

## Step 4: Enable Authentication Methods

1. In Firebase Console, go to **Authentication** → **Get started**
2. Click on **Sign-in method** tab
3. Enable **Email/Password**:
   - Click on "Email/Password"
   - Toggle "Enable"
   - Click "Save"
4. Enable **Google Sign-in**:
   - Click on "Google"
   - Toggle "Enable"
   - Enter support email (your email)
   - Click "Save"

## Step 5: Set Up Firebase Admin SDK (Backend)

1. In Firebase Console, go to **Project Settings** (⚙️ icon)
2. Click on **Service Accounts** tab
3. Click **Generate New Private Key**
4. Download the JSON file
5. Save it as `firebase_credentials.json` in your project root
6. Make sure the path in `.env` matches:
   ```
   FIREBASE_CREDENTIALS=./firebase_credentials.json
   ```

## Step 6: Configure Authorized Domains

1. In Firebase Console, go to **Authentication** → **Settings**
2. Scroll to **Authorized domains**
3. Add your domains:
   - `localhost` (already added)
   - Your production domain (when deploying)

## Step 7: Test the Setup

1. Start your Flask app: `.venv\Scripts\python.exe app.py`
2. Open browser and navigate to: `http://localhost:5000`
3. Click "Get Started" or "Login"
4. Try creating an account with email/password
5. Try signing in with Google

## Common Issues

### "Firebase is not configured" error
- Make sure you updated `firebase-config.js` with your actual config
- Clear browser cache and reload

### "Failed to verify token" error
- Ensure `firebase_credentials.json` is in the correct location
- Check that the file has proper read permissions
- Verify the service account key is valid

### Google Sign-in popup blocked
- Allow popups in your browser
- Check that your domain is in the authorized domains list

### Email/Password signup fails
- Verify Email/Password is enabled in Firebase Console
- Check that password meets requirements (min 6 characters)

## Security Notes

⚠️ **Important for Production:**

1. Never commit `firebase_credentials.json` to version control
2. Add it to `.gitignore`
3. Use environment variables for sensitive config in production
4. Set up proper Firestore security rules
5. Enable App Check to prevent abuse
6. Use HTTPS in production

## Firebase Pricing

- Firebase Authentication is **FREE** up to:
  - Phone Auth: 10K verifications/month
  - Email verification: unlimited
  - Google/Facebook/etc: unlimited

For most personal projects, you'll stay within the free tier.

## Next Steps

Once Firebase is set up, you can:
- View registered users in Firebase Console
- Set up custom email templates
- Enable multi-factor authentication
- Add more sign-in providers (Facebook, Twitter, etc.)
- Set up Firebase Cloud Firestore for real-time data sync

## Support

If you encounter issues:
1. Check Firebase Console for error messages
2. Review browser console for client-side errors
3. Check Flask logs for server-side errors
4. Consult [Firebase Documentation](https://firebase.google.com/docs/auth)

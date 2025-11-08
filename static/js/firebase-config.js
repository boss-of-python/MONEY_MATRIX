// Firebase Configuration and Initialization
// This file initializes Firebase SDK and exports auth methods

/**
 * FIREBASE SETUP INSTRUCTIONS:
 * 
 * 1. Go to https://console.firebase.google.com/
 * 2. Create a new project or select an existing one
 * 3. Click on "Add app" and select "Web" (</>) icon
 * 4. Register your app with a nickname (e.g., "Money Matrix")
 * 5. Copy the firebaseConfig object from the setup page
 * 6. Replace the config below with your actual Firebase config
 * 
 * 7. Enable Authentication:
 *    - In Firebase Console, go to "Authentication" > "Get started"
 *    - Enable "Email/Password" sign-in method
 *    - Enable "Google" sign-in method (add your email as support email)
 * 
 * 8. Set up Firestore (optional but recommended):
 *    - Go to "Firestore Database" > "Create database"
 *    - Start in test mode for development
 * 
 * 9. For production, update security rules and enable proper authentication
 */

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "YOUR_API_KEY_HERE",
  authDomain: "your-project-id.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID"
};

// Initialize Firebase
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { 
    getAuth, 
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signOut,
    sendPasswordResetEmail,
    GoogleAuthProvider,
    signInWithPopup,
    onAuthStateChanged,
    updateProfile
} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

// Check if Firebase config is set
const isConfigured = firebaseConfig.apiKey && firebaseConfig.apiKey !== "YOUR_API_KEY";

let app, auth;

if (isConfigured) {
    try {
        app = initializeApp(firebaseConfig);
        auth = getAuth(app);
        console.log('Firebase initialized successfully');
    } catch (error) {
        console.error('Firebase initialization error:', error);
    }
} else {
    console.warn('Firebase is not configured. Running in demo mode.');
    console.warn('Get your config from: https://console.firebase.google.com/');
}

// Export Firebase services and methods
export {
    auth,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signOut,
    sendPasswordResetEmail,
    GoogleAuthProvider,
    signInWithPopup,
    onAuthStateChanged,
    updateProfile,
    isConfigured
};
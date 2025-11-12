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
 * 6. Set the values in your .env file
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

// Initialize Firebase with dynamic configuration
let app, auth, isConfigured = false;

// Function to initialize Firebase with configuration from backend
async function initializeFirebase() {
    try {
        // Fetch configuration from backend
        const response = await fetch('/api/config/firebase');
        if (!response.ok) {
            throw new Error('Failed to fetch Firebase configuration');
        }
        
        const firebaseConfig = await response.json();
        
        // Check if config is valid
        isConfigured = firebaseConfig.apiKey && firebaseConfig.apiKey !== "YOUR_API_KEY";
        
        if (isConfigured) {
            // Initialize Firebase app
            app = firebase.initializeApp(firebaseConfig);
            // Get auth instance
            auth = firebase.auth();
            console.log('Firebase initialized successfully');
        } else {
            console.warn('Firebase is not configured. Running in demo mode.');
            console.warn('Set Firebase configuration in your .env file');
        }
    } catch (error) {
        console.error('Failed to initialize Firebase:', error);
        console.warn('Running in demo mode due to configuration error');
    }
}

// Export Firebase services and methods
export {
    app,
    auth,
    isConfigured,
    initializeFirebase
};
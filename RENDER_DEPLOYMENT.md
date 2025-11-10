# Money Matrix - Render Deployment Guide

This guide provides detailed step-by-step instructions for deploying the Money Matrix application to Render.com.

## Prerequisites

1. A Render.com account (free tier available)
2. A GitHub account
3. Firebase account with a configured project
4. Firebase service account key (JSON file)

## Step-by-Step Deployment Process

### Step 1: Prepare Your Firebase Credentials

1. Go to the Firebase Console: https://console.firebase.google.com
2. Select your Money Matrix project
3. Navigate to Project Settings → Service Accounts
4. Click "Generate new private key"
5. Save the downloaded JSON file as `firebase_credentials.json`
6. **Important**: Keep this file secure and never commit it to version control

### Step 2: Fork or Clone the Repository

1. Fork the Money Matrix repository to your GitHub account OR
2. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   cd money-matrix
   ```

### Step 3: Create Render Account

1. Visit https://render.com
2. Sign up for a free account or log in if you already have one
3. Verify your email address

### Step 4: Connect GitHub to Render

1. In your Render dashboard, click "New Web Service"
2. Connect your GitHub account when prompted
3. Grant Render access to your repositories
4. Select the Money Matrix repository

### Step 5: Configure Web Service Settings

1. **Service Type**: Web Service (should be pre-selected)
2. **Name**: money-matrix (or your preferred name)
3. **Region**: Choose the region closest to your users
4. **Branch**: main (or your preferred branch)
5. **Root Directory**: Leave blank (default)

### Step 6: Set Build and Start Commands

Render should automatically detect these from your render.yaml file:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:main`

If not, manually enter these commands.

### Step 7: Configure Environment Variables

In the "Environment Variables" section, add the following:

1. **SECRET_KEY**:
   - Key: `SECRET_KEY`
   - Value: Generate a random 32+ character string
   - Example: `your-super-secret-random-key-min-32-chars`

2. **DATABASE_URI**:
   - Key: `DATABASE_URI`
   - Value: `sqlite:///database.db`

3. **DEBUG**:
   - Key: `DEBUG`
   - Value: `False`

4. **FIREBASE_CREDENTIALS**:
   - Key: `FIREBASE_CREDENTIALS`
   - Value: Path to your Firebase credentials file (`./firebase_credentials.json`)

### Step 8: Upload Firebase Credentials

You have two options for handling Firebase credentials:

#### Option A: Upload via Render Dashboard (Recommended)
1. In your Render service dashboard, go to "Environment" tab
2. Scroll to "Secret Files" section
3. Click "Add Secret File"
4. Set the path to: `./firebase_credentials.json`
5. Paste the contents of your `firebase_credentials.json` file
6. Click "Save Changes"

#### Option B: Set as Environment Variable
1. In the "Environment Variables" section, add:
   - Key: `FIREBASE_CREDENTIALS`
   - Value: The entire JSON content of your `firebase_credentials.json` file (as a single line string)

### Step 9: Advanced Configuration (Optional)

#### Custom Domain
1. In your service dashboard, go to "Settings" tab
2. Scroll to "Custom Domains" section
3. Click "Add Custom Domain"
4. Follow Render's DNS configuration instructions

#### Health Check
Render automatically monitors your application. You can add a custom health check endpoint by adding this to your `app.py`:

```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200
```

### Step 10: Deploy the Application

1. Click "Create Web Service"
2. Render will begin building your application
3. Watch the build logs for any errors
4. Once complete, your application will be available at the provided URL

## Deployment Verification

### Check Application Status
1. In your Render dashboard, verify the service shows "Live"
2. Click the service URL to visit your application
3. Test user registration and login functionality

### Monitor Logs
1. In your service dashboard, go to "Logs" tab
2. Monitor for any errors or warnings
3. Look for successful startup messages

## Common Issues and Solutions

### Issue: "Application failed to start"
**Solution**:
1. Check logs for specific error messages
2. Verify all environment variables are set correctly
3. Ensure Firebase credentials are properly configured

### Issue: "Database permissions error"
**Solution**:
1. Render's file system is read-only except for specific directories
2. Ensure your database file is created in a writable location
3. Consider using an external database for production

### Issue: "Firebase authentication failed"
**Solution**:
1. Verify Firebase credentials file is correctly uploaded
2. Check that the Firebase project is properly configured
3. Ensure Firebase Authentication is enabled for Email/Password and Google

## Scaling and Performance

### Free Tier Limitations
- 512MB RAM
- Auto-sleep after 15 minutes of inactivity
- Service wakes up on first request (may cause initial delay)

### Upgrading to Paid Plan
1. In Render dashboard, go to "Billing" section
2. Add payment method
3. Upgrade your service plan for better performance

## Maintenance and Updates

### Updating Your Application
1. Push changes to your GitHub repository
2. Render will automatically detect changes and redeploy
3. Monitor the build process in your dashboard

### Database Backups
1. Regularly backup your database file
2. Consider implementing automated backup solutions
3. Store backups in secure, offsite locations

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use strong SECRET_KEY** values
3. **Enable HTTPS** (Render provides this automatically)
4. **Regularly rotate credentials**
5. **Monitor logs** for suspicious activity

## Cost Breakdown

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Web Service | 512MB RAM, sleeps after 15min | Starts at $7/month |
| Bandwidth | 100GB/month | $0.01/GB additional |
| Build Minutes | 500/month | $0.05/minute additional |

## Support Resources

- **Render Documentation**: https://render.com/docs
- **Money Matrix Issues**: GitHub repository issues
- **Firebase Support**: https://firebase.google.com/support
- **Flask Documentation**: https://flask.palletsprojects.com

---

**Deployment Complete!** Your Money Matrix application should now be live and accessible to users worldwide.
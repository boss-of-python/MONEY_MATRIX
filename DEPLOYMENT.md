# Money Matrix - Deployment Guide

## Quick Start (Local Development)

### 1. Prerequisites
- Python 3.10 or higher
- Firebase account (free tier)
- Git (optional)

### 2. Installation Steps

```bash
# Navigate to project directory
cd money_matrix

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Firebase Setup

1. Go to https://console.firebase.google.com
2. Create new project: "Money Matrix"
3. Enable Authentication:
   - Email/Password
   - Google Sign-In
4. Generate service account key:
   - Project Settings → Service Accounts
   - Click "Generate new private key"
   - Save as `firebase_credentials.json` in project root

### 4. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
# Set SECRET_KEY to a random 32+ character string
# Example: SECRET_KEY=your-super-secret-random-key-min-32-chars
```

### 5. Run Application

```bash
# Start development server
python app.py

# Application will be available at:
# http://localhost:5000
```

## Production Deployment

### Option 1: Render.com (Recommended - Free Tier)

1. **Create Render Account**: https://render.com

2. **Create Web Service**:
   - Connect GitHub repository
   - Select "Web Service"
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:main --bind 0.0.0.0:$PORT`

3. **Environment Variables**:
   ```
   SECRET_KEY=<generate-random-32-chars>
   FIREBASE_CREDENTIALS=./firebase_credentials.json
   DATABASE_URI=sqlite:///database.db
   DEBUG=False
   ```

4. **Add Firebase Credentials**:
   - Upload `firebase_credentials.json` via Render dashboard
   - Or set FIREBASE_CREDENTIALS to JSON string

5. **Deploy**: Click "Deploy"

**Free Tier Limits**:
- 512MB RAM
- Auto-sleep after 15 min inactivity
- Wakes up on first request

### Option 2: Railway.app (Free $5/month credit)

1. **Create Railway Account**: https://railway.app

2. **Deploy from GitHub**:
   - Connect repository
   - Railway auto-detects Python
   - Automatically installs dependencies

3. **Environment Variables** (Railway Settings):
   ```
   SECRET_KEY=<random-string>
   FIREBASE_CREDENTIALS=/app/firebase_credentials.json
   DATABASE_URI=sqlite:///database.db
   ```

4. **Upload Firebase Credentials**:
   - Use Railway CLI or dashboard

5. **Deploy**: Automatic on push

### Option 3: PythonAnywhere (Free tier: 1 web app)

1. **Create Account**: https://www.pythonanywhere.com

2. **Upload Code**:
   ```bash
   # In PythonAnywhere Bash console
   git clone <your-repo>
   cd money_matrix
   ```

3. **Create Virtual Environment**:
   ```bash
   mkvirtualenv money-matrix --python=python3.10
   pip install -r requirements.txt
   ```

4. **Configure Web App**:
   - Web tab → Add new web app
   - WSGI configuration file → Edit:
   ```python
   import sys
   path = '/home/yourusername/money_matrix'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import main
   application = main()
   ```

5. **Set Environment Variables**:
   - Upload firebase_credentials.json to Files
   - Create .env in project directory

6. **Reload Web App**

## Database Management

### Backup Database

```bash
# SQLite database is a single file
# Backup by copying database.db file
cp database.db database_backup_$(date +%Y%m%d).db
```

### Reset Database

```bash
# Delete database file
rm database.db

# Restart app - tables will be recreated
python app.py
```

## Security Checklist

### Before Production Deployment

- [ ] Change SECRET_KEY to random 32+ character string
- [ ] Set DEBUG=False in .env
- [ ] Secure firebase_credentials.json (never commit to Git)
- [ ] Enable HTTPS on hosting platform
- [ ] Review Firebase Security Rules
- [ ] Set up error monitoring (optional: Sentry)
- [ ] Configure CORS_ORIGINS for your domain
- [ ] Enable session cookie security

### Firebase Security Rules

In Firebase Console → Firestore → Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /transactions/{transactionId} {
      allow read, write: if request.auth != null && 
        resource.data.firebase_uid == request.auth.uid;
    }
    
    match /budgets/{budgetId} {
      allow read, write: if request.auth != null && 
        resource.data.firebase_uid == request.auth.uid;
    }
  }
}
```

## Monitoring & Logs

### View Application Logs

```bash
# Development
# Logs output to console and app.log file
tail -f app.log

# Production (Render.com)
# View logs in Render dashboard
# Logs tab → Real-time logs

# Production (PythonAnywhere)
# Error log available in Web tab
```

### Health Check Endpoint

```python
# Add to app.py
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200
```

## Performance Optimization

### Database Optimization

```python
# Already implemented in models:
# - Indexes on frequently queried fields
# - Soft deletes (is_deleted flag)
# - Connection pooling
```

### Caching (Optional - For High Traffic)

```python
# Install Flask-Caching
pip install Flask-Caching

# Add to app.py
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Cache dashboard data
@cache.cached(timeout=300)  # 5 minutes
def get_dashboard_data():
    # ...
```

## Scaling Strategy

### Phase 1: Free Tier (0-1,000 users)
- Current setup sufficient
- SQLite handles well
- Firebase free tier: 50K MAU

### Phase 2: Growth (1,000-10,000 users)
- Upgrade to paid hosting ($7-15/month)
- Consider PostgreSQL for better concurrency
- Add Redis for caching
- Enable CDN for static assets

### Phase 3: Scale (10,000+ users)
- Dedicated database server
- Load balancer
- Horizontal scaling (multiple app instances)
- Firebase paid plan

## Troubleshooting

### Issue: "Firebase credentials not found"
**Solution**: Ensure firebase_credentials.json is in the correct path

### Issue: "Database locked"
**Solution**: SQLite has limited concurrent writes. For production, consider PostgreSQL.

### Issue: "Module not found"
**Solution**: 
```bash
# Verify virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port already in use"
**Solution**:
```bash
# Change port in .env
PORT=5001

# Or kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill
```

## Cost Breakdown

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Hosting (Render) | 512MB RAM | $7/month (512MB) |
| Firebase Auth | 50K MAU | $0.0025/user above |
| Database (SQLite) | Unlimited | Free forever |
| Total | $0/month | ~$7-15/month |

## Support & Documentation

- **Issues**: GitHub Issues
- **Firebase Docs**: https://firebase.google.com/docs
- **Flask Docs**: https://flask.palletsprojects.com
- **SQLAlchemy Docs**: https://www.sqlalchemy.org

---

**Ready to deploy!** Follow the steps above and your Money Matrix application will be live in under 30 minutes.

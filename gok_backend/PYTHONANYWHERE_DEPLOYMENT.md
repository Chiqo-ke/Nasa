# PythonAnywhere Deployment Guide

## 🚀 Deploy Federal Ledger Backend to PythonAnywhere

### Prerequisites
- PythonAnywhere account (Free or Paid)
- GitHub repository with your code
- Vercel frontend deployed

---

## Step 1: Upload Your Code to PythonAnywhere

### Option A: Using Git (Recommended)
```bash
# In PythonAnywhere Bash console
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git Nasa
cd Nasa/gok_backend
```

### Option B: Direct Upload
1. Go to **Files** tab in PythonAnywhere
2. Upload your entire `Nasa` folder to `/home/Chiqoke254/`
3. Your backend should be at `/home/Chiqoke254/Nasa/gok_backend`

---

## Step 2: Create Virtual Environment

```bash
# In PythonAnywhere Bash console
cd ~/Nasa/gok_backend
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r backend_requirements.txt
```

**Important**: Use Python 3.10 or 3.11 (available on PythonAnywhere)

---

## Step 3: Configure Web App

1. Go to **Web** tab in PythonAnywhere
2. You already created a manual web app - good!
3. Configure the following settings:

### A. Source Code
```
/home/Chiqoke254/Nasa/gok_backend
```

### B. Working Directory
```
/home/Chiqoke254/Nasa/gok_backend
```

### C. Virtualenv
```
/home/Chiqoke254/Nasa/gok_backend/venv
```

### D. WSGI Configuration File
Click on the WSGI configuration file link and **replace all content** with:

```python
# WSGI configuration for Federal Ledger FastAPI Backend
import sys
import os

# Add your project directory to sys.path
path = '/home/Chiqoke254/Nasa/gok_backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DATABASE_URL'] = 'sqlite:///./federal_blockchain.db'

# Import the FastAPI application
from main import app

# ASGI to WSGI adapter
from asgiref.wsgi import WsgiToAsgi
application = WsgiToAsgi(app)
```

---

## Step 4: Initialize Database

```bash
# In PythonAnywhere Bash console
cd ~/Nasa/gok_backend
source venv/bin/activate
python init_system.py  # Or your database initialization script
```

---

## Step 5: Reload Web App

1. Go to **Web** tab
2. Click the **Reload** button for your web app
3. Wait for the green checkmark

---

## Step 6: Update Frontend Environment Variables

Update your Vercel frontend environment variables:

```env
VITE_API_URL=https://Chiqoke254.pythonanywhere.com
VITE_WS_URL=wss://Chiqoke254.pythonanywhere.com
```

### In Vercel Dashboard:
1. Go to your project → **Settings** → **Environment Variables**
2. Add/Update:
   - `VITE_API_URL`: `https://Chiqoke254.pythonanywhere.com`
   - `VITE_WS_URL`: `wss://Chiqoke254.pythonanywhere.com`
3. Redeploy your frontend

---

## Step 7: Test Your Deployment

### Test Backend API
```bash
curl https://Chiqoke254.pythonanywhere.com/
```

Expected response:
```json
{
  "message": "National Financial Blockchain Administration Portal API",
  "version": "2.0",
  "features": [...]
}
```

### Test API Documentation
Visit: https://Chiqoke254.pythonanywhere.com/docs

### Test from Frontend
1. Visit: https://federal-ledger.vercel.app
2. Try logging in or making API calls
3. Check browser console for any CORS errors

---

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
# Activate venv and install missing package
cd ~/Nasa/gok_backend
source venv/bin/activate
pip install MISSING_PACKAGE_NAME
# Reload web app
```

### Error: "Internal Server Error"
1. Check **Error log** in Web tab
2. Check **Server log** in Web tab
3. Common issues:
   - Missing dependencies
   - Wrong Python version
   - Import errors

### CORS Errors
- Verify Vercel domain is in `allow_origins` list in `main.py`
- Check that both `http` and `https` versions are included if needed
- Reload PythonAnywhere web app after changes

### Database Issues
```bash
# Reset database
cd ~/Nasa/gok_backend
source venv/bin/activate
rm federal_blockchain.db  # Delete old database
python init_system.py     # Reinitialize
```

### Static Files Not Loading
PythonAnywhere requires special configuration for static files:
1. Go to **Web** tab
2. Under **Static files**, add:
   - URL: `/static/`
   - Directory: `/home/Chiqoke254/Nasa/gok_backend/static/`

---

## 📝 Important Notes

### Free Tier Limitations
- Daily CPU quota (100 seconds/day)
- Web app goes to sleep after 3 months of inactivity
- One web app only
- No WebSocket support on free tier

### Paid Tier Benefits
- More CPU time
- Multiple web apps
- Always-on apps
- WebSocket support
- Custom domains

### WebSocket Consideration
⚠️ **WebSocket features (`/ws/{wallet_address}`) will NOT work on free tier**

To disable WebSockets for free tier:
1. Comment out WebSocket endpoint in `main.py`
2. Update frontend to not use WebSocket connections
3. Use polling as alternative

---

## 🔄 Updating Your Deployment

When you make changes to your code:

```bash
# In PythonAnywhere Bash console
cd ~/Nasa/gok_backend
git pull origin main  # or master
source venv/bin/activate
pip install -r backend_requirements.txt  # If dependencies changed
```

Then reload web app in **Web** tab.

---

## 🌐 Your Deployment URLs

- **Backend API**: https://Chiqoke254.pythonanywhere.com
- **API Docs**: https://Chiqoke254.pythonanywhere.com/docs
- **Frontend**: https://federal-ledger.vercel.app

---

## 📞 Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
- Your error logs: Web tab → Error log / Server log

---

## ✅ Deployment Checklist

- [ ] Nasa folder uploaded to `/home/Chiqoke254/Nasa`
- [ ] Virtual environment created at `/home/Chiqoke254/Nasa/gok_backend/venv`
- [ ] Dependencies installed
- [ ] WSGI file configured
- [ ] Database initialized
- [ ] Web app reloaded
- [ ] Vercel environment variables updated
- [ ] Frontend redeployed
- [ ] API endpoint tested
- [ ] CORS verified
- [ ] Frontend-backend connection tested

---

**Last Updated**: February 11, 2026

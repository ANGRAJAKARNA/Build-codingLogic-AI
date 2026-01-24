# 🚀 Streamlit Cloud Deployment Guide

Complete step-by-step guide to deploy your PyCode AI app to Streamlit Cloud.

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure:

- [x] ✅ Code is working locally (`streamlit run main.py`)
- [x] ✅ All dependencies are in `requirements.txt`
- [x] ✅ No hardcoded paths (use relative paths)
- [x] ✅ Environment variables are optional or documented
- [x] ✅ Code is pushed to GitHub

---

## 📋 Step 1: Prepare Your GitHub Repository

### 1.1 Ensure Code is Committed

```bash
# Check status
git status

# If you have uncommitted changes:
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 1.2 Verify Repository Structure

Your repository should look like this:

```
Build-codingLogic-AI/
└── PythonCode/
    ├── .streamlit/
    │   └── config.toml          # ✅ Created
    ├── main.py                  # ✅ Entry point
    ├── requirements.txt         # ✅ Dependencies
    ├── builtin_assistant.py
    ├── evaluator.py
    ├── interview_engine.py
    ├── persistence.py
    ├── questions.py
    ├── ai_service.py
    └── ... (other files)
```

**Important**: Streamlit Cloud looks for `main.py` in the root OR in a subdirectory. Since your app is in `PythonCode/`, you'll specify the path during deployment.

---

## 📋 Step 2: Sign Up for Streamlit Cloud

### 2.1 Go to Streamlit Cloud

1. Visit: **https://share.streamlit.io**
2. Click **"Sign up"** or **"Get started"**
3. Sign in with your **GitHub account** (required)

### 2.2 Authorize Streamlit

- Grant Streamlit Cloud access to your GitHub repositories
- You can choose **"All repositories"** or **"Selected repositories"**

---

## 📋 Step 3: Deploy Your App

### 3.1 Create New App

1. Click **"New app"** button (top right)
2. You'll see the deployment form

### 3.2 Fill in Deployment Details

**Repository**:
- Select: `your-username/Build-codingLogic-AI`
- Or: `your-org/Build-codingLogic-AI` (if in an organization)

**Branch**:
- Select: `main` (or `master` if that's your default branch)

**Main file path**:
- **IMPORTANT**: Enter `PythonCode/main.py`
- This tells Streamlit Cloud where your entry point is

**App URL** (optional):
- Choose a custom subdomain: `pycode-ai` → `pycode-ai.streamlit.app`
- Or use auto-generated name

### 3.3 Advanced Settings (Optional)

Click **"Advanced settings"** to configure:

**Python version**:
- Default: Python 3.11 (recommended)
- Or: 3.10, 3.9 (if needed)

**Dependencies**:
- Streamlit Cloud automatically uses `requirements.txt`
- If you have a different file, specify it here

**Secrets** (for API keys):
- We'll configure this in Step 4

### 3.4 Deploy!

1. Click **"Deploy"** button
2. Wait 2-5 minutes for deployment
3. Watch the build logs in real-time

---

## 📋 Step 4: Configure Secrets (Optional)

If your app uses the Groq API, you need to set the API key.

### 4.1 Access Secrets

1. In your app dashboard, click **"Settings"** (⚙️ icon)
2. Go to **"Secrets"** tab
3. Click **"Edit secrets"**

### 4.2 Add API Key

Add this to the secrets file:

```toml
GROQ_API_KEY = "gsk_your_actual_api_key_here"
```

**How to get Groq API key**:
1. Go to: https://console.groq.com
2. Sign up / Sign in
3. Navigate to API Keys
4. Create new API key
5. Copy the key (starts with `gsk_`)

### 4.3 Save Secrets

1. Click **"Save"**
2. Your app will automatically restart with new secrets

**Note**: Secrets are encrypted and only accessible to your app. Never commit them to GitHub!

---

## 📋 Step 5: Verify Deployment

### 5.1 Check Build Logs

After deployment, check for:

- ✅ **"Your app is live!"** message
- ✅ No error messages in logs
- ✅ All dependencies installed successfully

### 5.2 Test Your App

1. Visit your app URL: `https://your-app-name.streamlit.app`
2. Test key features:
   - [ ] App loads correctly
   - [ ] Practice mode works
   - [ ] Interview mode works
   - [ ] AI chat assistant works
   - [ ] Code execution works
   - [ ] Progress saving works

### 5.3 Common Issues

**Issue**: "Module not found"
- **Fix**: Check `requirements.txt` includes all dependencies
- **Fix**: Ensure package names are correct (case-sensitive)

**Issue**: "File not found" errors
- **Fix**: Use relative paths (you already do this ✅)
- **Fix**: Ensure all files are committed to GitHub

**Issue**: "API key not working"
- **Fix**: Check secrets are set correctly
- **Fix**: Restart app after adding secrets

---

## 📋 Step 6: Update Your App

### 6.1 Automatic Updates

Streamlit Cloud automatically redeploys when you push to your branch:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Streamlit Cloud automatically:
# 1. Detects the push
# 2. Rebuilds your app
# 3. Deploys new version
# (Takes 2-5 minutes)
```

### 6.2 Manual Redeploy

If automatic deployment doesn't work:

1. Go to your app dashboard
2. Click **"⋮"** (three dots menu)
3. Select **"Redeploy"**

---

## 🔧 Configuration Files

### `.streamlit/config.toml`

Already created! This file configures:
- Theme colors (matches your neon cyber design)
- Server settings
- UI preferences

### `requirements.txt`

Your dependencies file. Streamlit Cloud uses this to install packages.

**Note**: Some packages might need adjustment:
- `pymupdf` → Works ✅
- `sentence-transformers` → Works ✅ (but large, slow first install)
- `faiss-cpu` → Works ✅
- `audio-recorder-streamlit` → Works ✅ (browser-based)

---

## 🎨 Custom Domain (Optional)

### Set Custom Domain

1. Go to app **Settings**
2. Click **"Custom domain"**
3. Add your domain
4. Follow DNS configuration instructions

**Example**: `pycode.yourdomain.com` → Your Streamlit app

---

## 📊 Monitoring & Analytics

### View App Metrics

1. Go to your app dashboard
2. View:
   - **View count**: How many people visited
   - **Run time**: App uptime
   - **Resource usage**: CPU/Memory

### View Logs

1. Click **"Manage app"**
2. Go to **"Logs"** tab
3. See real-time application logs

---

## 🔒 Security Best Practices

### ✅ Do's

- ✅ Use Streamlit secrets for API keys
- ✅ Keep secrets out of code
- ✅ Use HTTPS (automatic on Streamlit Cloud)
- ✅ Review dependencies regularly

### ❌ Don'ts

- ❌ Never commit API keys to GitHub
- ❌ Don't hardcode sensitive data
- ❌ Don't expose internal endpoints

---

## 💰 Pricing

### Free Tier

- ✅ **Unlimited apps**
- ✅ **Unlimited viewers**
- ✅ **Public apps only**
- ✅ **Community support**

### Team Tier ($20/user/month)

- ✅ Private apps
- ✅ Custom domains
- ✅ Priority support
- ✅ Team collaboration

**For most users**: Free tier is perfect! ✅

---

## 🐛 Troubleshooting

### Build Fails

**Error**: "Could not find requirements.txt"
- **Fix**: Ensure `requirements.txt` is in `PythonCode/` directory
- **Fix**: Or specify custom path in Advanced Settings

**Error**: "Module installation failed"
- **Fix**: Check package name spelling
- **Fix**: Some packages might not be available (check Streamlit Cloud docs)

**Error**: "Main file not found"
- **Fix**: Check main file path: `PythonCode/main.py`
- **Fix**: Ensure file exists in repository

### App Crashes

**Error**: "App crashed on startup"
- **Fix**: Check logs for specific error
- **Fix**: Test locally first: `streamlit run main.py`
- **Fix**: Check for missing dependencies

**Error**: "Out of memory"
- **Fix**: Streamlit Cloud free tier has memory limits
- **Fix**: Optimize large imports (lazy loading)
- **Fix**: Consider Team tier for more resources

### Performance Issues

**Slow loading**:
- **Fix**: `sentence-transformers` is large (first load is slow)
- **Fix**: Consider lazy loading for heavy imports
- **Fix**: Cache expensive operations

---

## 📝 Quick Reference

### Deployment URL Format

```
https://[app-name].streamlit.app
```

### Main File Path

```
PythonCode/main.py
```

### Secrets Format

```toml
GROQ_API_KEY = "gsk_..."
```

### Update Command

```bash
git push origin main
```

---

## 🎉 Success!

Once deployed, your app will be:
- ✅ Live at: `https://your-app-name.streamlit.app`
- ✅ Automatically updated on git push
- ✅ Accessible worldwide
- ✅ HTTPS enabled
- ✅ Free (on free tier)

---

## 📞 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-cloud
- **Community Forum**: https://discuss.streamlit.io
- **GitHub Issues**: Report bugs in your repo

---

## ✅ Final Checklist

Before going live:

- [ ] Code pushed to GitHub
- [ ] App deployed successfully
- [ ] All features tested
- [ ] Secrets configured (if needed)
- [ ] App URL shared with users

**You're ready to go! 🚀**

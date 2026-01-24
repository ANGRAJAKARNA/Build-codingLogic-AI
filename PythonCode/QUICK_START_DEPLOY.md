# 🚀 Quick Start: Deploy to Streamlit Cloud

**5-minute deployment guide**

---

## Step 1: Push to GitHub (2 min)

```bash
# Make sure everything is committed
git add .
git commit -m "Ready for Streamlit Cloud"
git push origin main
```

---

## Step 2: Deploy (3 min)

1. **Go to**: https://share.streamlit.io
2. **Sign in** with GitHub
3. **Click** "New app"
4. **Fill in**:
   - Repository: `your-username/Build-codingLogic-AI`
   - Branch: `main`
   - Main file: `PythonCode/main.py` ⚠️ **IMPORTANT**
5. **Click** "Deploy"
6. **Wait** 2-5 minutes

---

## Step 3: Add API Key (Optional)

If you use Groq AI:

1. Click **Settings** ⚙️
2. Go to **Secrets** tab
3. Add:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```
4. **Save**

---

## ✅ Done!

Your app is live at: `https://your-app-name.streamlit.app`

**That's it!** 🎉

---

## Need More Details?

See `STREAMLIT_CLOUD_DEPLOYMENT.md` for complete guide.

# ⚡ Heroku Quick Start - 5 Minutes

## 🚀 Super Fast Deployment

### Step 1: Install Heroku CLI (One-time)

**Windows:** Download from https://devcenter.heroku.com/articles/heroku-cli

**Mac:**
```bash
brew install heroku/brew/heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login

```bash
heroku login
```

### Step 3: Deploy!

```bash
# Copy requirements
copy requirements-heroku.txt requirements.txt

# Initialize git (if needed)
git init
git add .
git commit -m "Initial commit"

# Create & deploy
heroku create
heroku addons:create heroku-postgresql:essential-0
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
git push heroku main

# Run migration
heroku run python migrate_to_multitenancy.py

# Open app
heroku open
```

## ✅ Done!

Your app is live at: `https://your-app-name.herokuapp.com`

---

## 🎯 Or Use Automated Script

```bash
bash deploy_heroku.sh
```

This script does everything automatically!

---

## 📝 What You Get

- ✅ Live URL (https://your-app.herokuapp.com)
- ✅ PostgreSQL database
- ✅ SSL/HTTPS (automatic)
- ✅ Free tier (550-1000 hours/month)
- ✅ Auto-scaling
- ✅ Easy updates

---

## 🔄 Update Your App

```bash
# Make changes
git add .
git commit -m "Update"
git push heroku main
```

---

## 📊 Useful Commands

```bash
# View logs
heroku logs --tail

# Open app
heroku open

# View database
heroku pg:info

# Restart app
heroku restart

# Run command
heroku run python script.py
```

---

## 🆘 Troubleshooting

### App not loading?
```bash
heroku logs --tail
```

### Database error?
```bash
heroku config:get DATABASE_URL
heroku restart
```

### Need to reset?
```bash
heroku run python migrate_to_multitenancy.py
```

---

## 💰 Cost

**Free Tier:**
- 550-1000 dyno hours/month
- 10,000 database rows
- Perfect for testing!

**Upgrade Later:**
- Hobby: $7/month (never sleeps)
- Standard: $25/month (better performance)

---

## 🎉 Success!

Your pharmacy system is now live on Heroku!

**Login:** https://your-app.herokuapp.com/login

**Register Org:** https://your-app.herokuapp.com/register-org

---

**Full Guide:** See `HEROKU_DEPLOYMENT.md` for detailed instructions

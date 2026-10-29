# 60-SECOND DEPLOYMENT — TL;DR VERSION

**"Just tell me what to do in 60 seconds"**

Choose ONE based on your platform:

---

## 🚀 NETLIFY (Easiest — literally 30 seconds)

1. Go to **netlify.com** (free account if needed)
2. Click "New site from Git"
3. Select this repo
4. Click "Deploy" (uses default settings)
5. Wait 30 seconds
6. Copy your live URL
7. **DONE** ✅ Share the URL with your team

---

## 🚀 VERCEL (Easiest — 30 seconds)

1. Go to **vercel.com** (free account if needed)
2. Click "New Project"
3. Select this repo
4. Click "Deploy"
5. Wait 30 seconds
6. Copy your live URL
7. **DONE** ✅ Share the URL with your team

---

## 🚀 GITHUB PAGES (Free, already have GitHub — 2 minutes)

1. Go to your repo on GitHub
2. Settings → Pages
3. Source: Select "main" branch
4. Click Save
5. Wait 60 seconds
6. Your URL appears: `https://[your-username].github.io/[repo-name]`
7. **DONE** ✅ Share the URL with your team

---

## 🚀 AWS S3 (If you know AWS — 5 minutes)

```bash
# Create bucket
aws s3 mb s3://my-metro-system

# Upload everything
aws s3 sync . s3://my-metro-system --delete

# Enable website hosting
aws s3 website s3://my-metro-system --index-document index.html

# Your URL: http://my-metro-system.s3-website-us-east-1.amazonaws.com
```

---

## 🚀 DOCKER (If you want containers — 10 minutes)

```bash
# Create Dockerfile in repo root (see DEPLOYMENT_GUIDE.md)
docker build -t metro-system .

# Run it
docker run -p 8080:80 metro-system

# Visit: http://localhost:8080
```

---

## 🚀 AZURE STATIC APPS (2 minutes)

1. Go to **portal.azure.com**
2. Create "Static Web App"
3. Select this repo
4. Location: Select your region
5. Click "Create"
6. Wait 2 minutes
7. Your URL appears in overview
8. **DONE** ✅ Share the URL with your team

---

## 🚀 ON YOUR SERVER (30 minutes)

```bash
# 1. Copy everything
scp -r ./* user@your-server:/var/www/metro-system

# 2. Configure nginx
# (See DEPLOYMENT_GUIDE.md → On-Premise section)

# 3. Restart nginx
sudo systemctl restart nginx

# 4. Visit: http://your-domain.com
```

---

## ✅ VERIFICATION (30 seconds)

```
After deployment:
1. Open your live URL in browser
2. Press F12 (Developer Tools)
3. Click Console tab
4. Should be clean (no red errors)
5. Click one tool (any tool)
6. Should respond instantly
```

**If you see errors:** See FINAL_DEPLOYMENT_CHECKLIST.md → "If Something Goes Wrong"

---

## 📤 SHARE YOUR LIVE URL

Once deployed, copy your URL and send to team:

```
Hey team!

The Taipei Metro Circular Line system is now live:

[YOUR_LIVE_URL]

→ First time? Read README_FIRST.txt (in the system)
→ 5 minutes? Read QUICK_REFERENCE_ONE_PAGER.md
→ Your role? Use FIRST_TIME_USER.md

Let me know what you think!
```

---

## ⏱️ TIME ESTIMATES

| Platform | Time | Effort |
|----------|------|--------|
| Netlify | 30 sec | Click 3 buttons |
| Vercel | 30 sec | Click 3 buttons |
| GitHub Pages | 2 min | 3 clicks |
| Azure | 2 min | Fill form |
| AWS | 5 min | 3 bash commands |
| Docker | 10 min | Build & run |
| On-Premise | 30 min | Copy & configure |

**Pro tip:** Pick Netlify or Vercel. Literally just click "Deploy" and you're done.

---

## 🎯 YOU ARE HERE

```
┌─────────────────┐
│  Read this file │  ← You are here
└────────┬────────┘
         ↓
   ┌─────────────────┐
   │ Pick a platform │
   └────────┬────────┘
            ↓
   ┌──────────────────┐
   │ Follow the steps │
   │ for that platform│
   └────────┬─────────┘
            ↓
   ┌──────────────────┐
   │ Wait 30 sec-5 min│
   └────────┬─────────┘
            ↓
   ┌──────────────────┐
   │ Copy live URL    │
   └────────┬─────────┘
            ↓
   ┌──────────────────┐
   │ Share with team  │
   └──────────────────┘
   ✅ DONE
```

---

## ❓ QUESTIONS?

**"Which platform should I pick?"**  
→ Netlify or Vercel (easiest, literally 30 seconds)

**"I'm already on GitHub"**  
→ GitHub Pages (free, 2 minutes)

**"I need more control"**  
→ AWS or Docker

**"What if something breaks?"**  
→ See FINAL_DEPLOYMENT_CHECKLIST.md → Troubleshooting

**"What do I do after deployment?"**  
→ See POST_DEPLOYMENT_GUIDE.md (first 48 hours roadmap)

---

## 🚀 GO. NOW.

1. Pick your platform from above
2. Follow the 2-10 steps for that platform
3. Copy your live URL
4. Come back in 2 minutes
5. Tell your team

**That's it. You're done.** ✅

---

*For detailed guides, see DEPLOYMENT_GUIDE.md*  
*For verification checklist, see FINAL_DEPLOYMENT_CHECKLIST.md*  
*For what to do after, see POST_DEPLOYMENT_GUIDE.md*

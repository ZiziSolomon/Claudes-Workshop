# DEPLOYMENT TROUBLESHOOTING FAQ

**Common issues and exact solutions.**

---

## ❌ "Tools show blank/error"

**What you see:** A tool page is blank or shows an error

**Fix (30 seconds):**
1. Open your browser: F12 (Developer Tools)
2. Click Console tab
3. Look for red error messages
4. Take screenshot and see matching solution below

**Most common causes:**

### Error: "Cannot find file"
- **Solution:** Check that ALL files uploaded (not just HTML)
- **Netlify:** Check "Deploys" → "Files" → should see 65+ items
- **GitHub Pages:** Run `git push` again (sometimes takes 2-3 min)
- **AWS:** Run: `aws s3 ls s3://your-bucket` (verify files there)

### Error: "CORS error" or "blocked by browser"
- **Solution:** This is usually a false alarm. Refresh the page.
- If it persists: Your platform might be blocking data files
- **Fix:** Contact platform support, show them error message

### Error: "JSON parse error"
- **Solution:** Data file is corrupted
- **Fix:** Verify `taipei-metro-data.json` exists
- Run: `cat taipei-metro-data.json | head -5` (should show valid JSON)

### Page loads but tools don't respond
- **Solution:** JavaScript isn't loading
- **Fix:** Try in different browser (Chrome, Firefox, Safari)
- **Fix:** Clear browser cache: Ctrl+Shift+Delete
- **Fix:** Try in incognito/private mode

---

## ❌ "404 Not Found"

**What you see:** "Not Found" error or blank page

**Fix (2 minutes):**

### On Netlify
1. Go to site settings
2. Check "Build & deploy" → "Build settings"
3. Make sure "Publish directory" is set to `.` (current directory)
4. Trigger redeploy: "Deploys" → "Trigger deploy"

### On Vercel
1. Go to "Settings" → "General"
2. Check "Root Directory" is blank (uses repo root)
3. Redeploy: "Deployments" → rightclick → "Redeploy"

### On GitHub Pages
1. Settings → Pages → Source: Check it says "main branch"
2. Go to "Actions" tab
3. Check if "pages build and deployment" is green
4. If red: Click it → check error message

### On AWS S3
```bash
# List files
aws s3 ls s3://your-bucket --recursive

# Should see: index.html, taipei-metro-data.json, many .html files
# If not: Files didn't upload. Run:
aws s3 sync . s3://your-bucket --delete
```

### On Docker
```bash
# Check container is running
docker ps

# If not listed: Restart it
docker run -p 8080:80 metro-system

# Then visit: http://localhost:8080
```

---

## ❌ "Page is very slow"

**What you see:** Page takes 5+ seconds to load or tools lag

**Fix (5 minutes):**

### Check your connection
1. Run speed test: speedtest.net
2. If slow: Try again from different network (WiFi vs mobile)
3. If still slow on multiple networks: It's the platform issue (see below)

### Check platform status
- **Netlify:** https://www.netlify.com/status
- **Vercel:** https://vercel.status.io
- **GitHub:** https://www.githubstatus.com
- **AWS:** https://status.aws.amazon.com

### If everything shows "up" but still slow:
- Try a different tool (not the same one)
- Clear browser cache: Ctrl+Shift+Delete
- Refresh page: Ctrl+Shift+R (hard refresh)
- Try in incognito mode

### If one specific tool is slow:
- That tool might have a bug
- Try a different tool
- Report in DEPLOYMENT_LOG.txt that tool X is slow
- Plan to optimize it in v2.1

---

## ❌ "It worked 1 hour ago but now it's down"

**What you see:** Site was working, now gives error

**Fix (2 minutes):**

### Step 1: Is it really down?
- Check on your phone (different network)
- Check in different browser
- Check on a friend's computer
- If working elsewhere: Your internet is the issue

### Step 2: Check platform status
- Visit platform status page (see links above)
- Usually shows "All systems operational" ✅
- If something is orange/red: Wait 15 minutes and retry

### Step 3: Check your repo
```bash
# Make sure your latest code is pushed
git status              # Should show "nothing to commit"
git log -1              # Should show your most recent commit
git push origin main    # Push latest (even if already pushed)
```

### Step 4: Force redeploy
- **Netlify:** "Deploys" → "Trigger deploy"
- **Vercel:** "Deployments" → rightclick → "Redeploy"
- **GitHub Pages:** Go to "Actions" tab → check deploy status
- **AWS:** Run again: `aws s3 sync . s3://your-bucket`

### Step 5: Wait 2-3 minutes
- Most platforms redeploy in 30-90 seconds
- GitHub Pages sometimes takes 2-3 minutes
- Check live URL again after 3 minutes

---

## ❌ "I see my old version, not the new one"

**What you see:** Changes you made aren't showing up live

**Fix (2 minutes):**

### Step 1: Verify you pushed
```bash
git status              # Should be clean
git log -1              # Should show YOUR recent commit
git push               # Push just to be sure
```

### Step 2: Clear your cache
Browser: Ctrl+Shift+Delete → Select "All time" → Clear cache  
Then: Refresh page: Ctrl+Shift+R (hard refresh)

### Step 3: Force redeploy
- **Netlify/Vercel:** Click "Redeploy" button
- **GitHub Pages:** Go to "Actions" → rerun latest workflow
- **AWS:** `aws s3 sync . s3://your-bucket --delete`

### Step 4: Wait 2-3 minutes then check

### If STILL showing old version:
- Try incognito/private mode (forces fresh download)
- Try a completely different browser
- Wait 5 minutes (sometimes caching takes time)

---

## ❌ "File upload failed" (during deployment)

**What you see:** Deployment stops with "upload failed"

**Fix (5 minutes):**

### On Netlify
1. Go to "Deploys" → find failed deploy (red)
2. Click it → "Deploy log"
3. Look for specific error message
4. Common: "Timeout" → Try deploy again
5. Common: "File too large" → Check if any file is >100MB
   - Solution: Compress large media files

### On Vercel
1. Go to "Deployments"
2. Find failed one (red X)
3. Click → "Build logs"
4. Look for error message
5. Common: "Timeout" → Try again
6. Common: "Function too large" → We don't have functions, so this is wrong → Redeploy

### On GitHub Pages
1. Go to "Actions" tab
2. Find failed workflow (red X)
3. Click it → "Logs"
4. Look for error
5. Usually: Re-run → fixes it

### On AWS
```bash
# Check permissions
aws s3 ls              # This should work
aws s3 ls s3://       # This should show your bucket

# If not: You don't have AWS credentials set up
# Set them up: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

# Then try again:
aws s3 sync . s3://your-bucket --delete
```

---

## ❌ "I deleted something by mistake"

**What you see:** A file is missing, or accidentally deleted

**Fix (1 minute):**

### Option 1: Git (if you haven't committed yet)
```bash
git checkout -- .    # Restore all files to last commit
```

### Option 2: Git (if you committed the deletion)
```bash
git revert HEAD      # Creates a NEW commit that undoes the deletion
git push             # Push the revert
```

### Option 3: The platform still has the old version
- **Netlify/Vercel:** Go to previous deployment → "Redeploy"
- **GitHub Pages:** Go to "Actions" → rerun a previous workflow
- **AWS:** Find your backup (or reupload from your local copy)

### Best practice going forward:
- Always commit before deploying
- Never delete through the web interface
- Use git for all changes: `git rm filename` → commit → push

---

## ❌ "I don't remember my password / can't log in"

**What you see:** Can't access deployment platform

**Fix (varies):**

### Netlify
- Go to netlify.com
- Click "Log in"
- "Forgot your password?" → enter email → check email for reset link

### Vercel
- Go to vercel.com
- Click "Log in"
- Use GitHub/Google login (usually easier)

### GitHub
- Go to github.com
- Click "Sign in"
- "Forgot password?" → check email

### AWS
- Go to console.aws.amazon.com
- Click "Sign in"
- Choose your sign-in method
- If you forgot: Click "Can't sign in?" → follow recovery

### If you can't recover:
- You might need to create a new account
- Re-deploy to that new account
- Update your team with the new URL

---

## ❌ "The system won't start" (Docker)

**What you see:** Docker container won't run

**Fix (5 minutes):**

```bash
# Check if Docker is running
docker ps

# If command not found: Docker isn't installed
# Install it: https://docs.docker.com/install

# If Docker is running but container won't start:
docker run -p 8080:80 metro-system

# Check error message. Common ones:

# "Port 8080 is already in use"
# Solution: Use different port: docker run -p 9000:80 metro-system
# Then visit: http://localhost:9000

# "Image not found"
# Solution: Build it first: docker build -t metro-system .

# "Permission denied"
# Solution: Add yourself to docker group (Linux only)
# sudo usermod -aG docker $USER
# Then logout and login again
```

---

## ✅ "Is it deployed yet?"

**How to check:**

1. **Netlify:** netlify.com → Select your site → Check "Deploys" tab
2. **Vercel:** vercel.com → Select your project → Check "Deployments" tab
3. **GitHub Pages:** Your repo → "Actions" tab → Check latest workflow
4. **AWS:** AWS Console → S3 → Your bucket → Check "Objects"
5. **Docker:** Run `docker ps` → should show running container
6. **On-Premise:** SSH to server → `curl http://localhost` → should see HTML

---

## ✅ "How do I know it worked?"

**After deployment, verify with this checklist (2 minutes):**

```
1. [ ] Open your live URL in browser
2. [ ] Page loads (doesn't say "404" or "Error")
3. [ ] Press F12 → Console tab → should be clean (no red)
4. [ ] Click one tool → should respond in <1 second
5. [ ] Try on mobile browser (different size)
6. [ ] Try in incognito/private mode (fresh cache)
```

If all 6 ✅: **You're deployed successfully!**

---

## 🆘 "My issue isn't here"

**What to do:**

1. Check: FINAL_DEPLOYMENT_CHECKLIST.md (has more checks)
2. Check: DEPLOYMENT_GUIDE.md (your platform section)
3. Check: Platform's support docs
4. Check: Browser console error (F12 → Console) → Google the error
5. Last resort: Save this error, come back tomorrow fresh

**Remember:** 95% of deployment issues are just browser cache. Try:
- Ctrl+Shift+Delete (clear cache)
- Close browser completely and reopen
- Try different browser
- Wait 3-5 minutes (redeployment might still be in progress)

---

**Most common fix:** Clear your browser cache and try again. Seriously. 80% of "it's broken" is just a cache issue.

**Second most common:** Wait 5 minutes. Deployments take time.

**Third most common:** It's already working. You just didn't scroll down to see it.

Good luck! You've got this. 🚀

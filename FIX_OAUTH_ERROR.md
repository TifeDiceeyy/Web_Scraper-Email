# 🔧 Fix OAuth Redirect URI Error

**Error:** `Error 400: redirect_uri_mismatch`

**Cause:** Your Google Cloud Console OAuth credentials don't have the correct redirect URIs configured.

---

## ✅ Solution: Add Redirect URIs

### Step 1: Open Google Cloud Console
1. Go to: https://console.cloud.google.com/apis/credentials
2. Sign in with the Google account that created the credentials

### Step 2: Find Your OAuth Client
1. Look for **OAuth 2.0 Client IDs** section
2. Click on the client ID you're using (usually named "Desktop app" or similar)

### Step 3: Add Redirect URIs
1. In the OAuth client details, find **Authorized redirect URIs**
2. Click **+ ADD URI** and add these URIs:
   ```
   http://localhost:8080/
   http://localhost:8081/
   http://localhost:8082/
   http://localhost:8083/
   http://localhost:8084/
   http://localhost:8085/
   http://localhost:8086/
   http://localhost:8087/
   http://localhost:8088/
   http://localhost:8089/
   http://localhost/
   ```

3. Click **SAVE**

### Step 4: Re-download Credentials
1. After saving, click the **⬇ Download JSON** button
2. Save the file as `credentials.json`
3. Replace the old `credentials.json` in your project folder:
   ```bash
   # Move downloaded file to project
   mv ~/Downloads/client_secret_*.json "/Users/tifediceeyy/All projects/Agentic Workflows/Web_Scraper&Email/credentials.json"
   ```

### Step 5: Delete Old Token
```bash
cd "/Users/tifediceeyy/All projects/Agentic Workflows/Web_Scraper&Email"
rm -f token.pickle
```

### Step 6: Try Again
```bash
source venv/bin/activate
python agent.py
# Choose option 6 (Instagram)
```

---

## 🎯 Alternative: Use Service Account (No Browser Auth)

If you keep having OAuth issues, you can use a Service Account instead:

### Step 1: Create Service Account
1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click **+ CREATE SERVICE ACCOUNT**
3. Name: "Business Outreach Bot"
4. Click **CREATE AND CONTINUE**
5. Grant role: **Editor**
6. Click **DONE**

### Step 2: Create Key
1. Click on the service account you just created
2. Go to **KEYS** tab
3. Click **ADD KEY** → **Create new key**
4. Choose **JSON**
5. Click **CREATE** (downloads `service-account-key.json`)

### Step 3: Share Google Sheet
1. Open your Google Sheet
2. Click **Share** button
3. Add the service account email (looks like: `name@project-id.iam.gserviceaccount.com`)
4. Give **Editor** permissions

### Step 4: Update Code to Use Service Account
This would require code changes - let me know if you want to go this route.

---

## 📞 Quick Fix Checklist

- [ ] Add redirect URIs to OAuth client
- [ ] Re-download credentials.json
- [ ] Replace old credentials.json
- [ ] Delete token.pickle
- [ ] Try authentication again

---

## 💡 Why This Happens

Google OAuth is very strict about redirect URIs for security. The app tries to redirect to `http://localhost:PORT/` after authentication, but Google rejects it if that exact URI isn't pre-approved in the Cloud Console.

---

**After fixing, run the test again!** 🚀

# Quick Start Guide

## Get Running in 5 Minutes

### 1. Generate Security Keys

```bash
# Generate JWT secret
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"

# Generate encryption key
python -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())"
```

### 2. Create Environment File

Create `.env` in the project root:

```env
JWT_SECRET_KEY=<paste-jwt-secret-from-step-1>
ENCRYPTION_KEY=<paste-encryption-key-from-step-1>
```

### 3. Start with Docker

```bash
docker-compose up --build
```

Wait for all services to start (~2-3 minutes first time).

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432 (postgres/postgres)

### 5. Create Your First Account

1. Go to http://localhost:3000
2. You'll see the login page
3. Register a new account (TODO: use API directly for now)

**Quick API Test with curl**:

```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Save the `access_token` from the login response.

### 6. Configure Your Settings

Update user settings with your API keys:

```bash
# Set your token
export TOKEN="<your-access-token-from-login>"

# Update settings
curl -X PUT http://localhost:8000/api/auth/settings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "gemini_api_key": "your-gemini-api-key",
    "gmail_address": "your-email@gmail.com",
    "gmail_app_password": "your-app-password",
    "telegram_bot_token": "optional-bot-token",
    "telegram_chat_id": "optional-chat-id"
  }'
```

### 7. Create Your First Campaign

```bash
curl -X POST http://localhost:8000/api/campaigns \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dentists in SF",
    "business_type": "Dentist",
    "outreach_type": "general_help",
    "data_source": "google_maps"
  }'
```

### 8. Next Steps

Now you can:
- Scrape businesses: `POST /api/campaigns/{id}/scrape`
- Generate emails: `POST /api/campaigns/{id}/generate-emails`
- Send emails: `POST /api/campaigns/{id}/send-approved`
- Track responses: `POST /api/campaigns/{id}/track-responses`

See the full API documentation at http://localhost:8000/docs

## Development Mode

### Backend Only

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements-api.txt

# Set DATABASE_URL in backend/.env
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/business_outreach" > .env
echo "JWT_SECRET_KEY=dev-key" >> .env
echo "ENCRYPTION_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')" >> .env

# Run
uvicorn app.main:app --reload
```

### Frontend Only

```bash
cd frontend
npm install

# Create .env
echo "VITE_API_URL=http://localhost:8000" > .env

# Run
npm run dev
```

## Stopping

```bash
# Stop containers
docker-compose down

# Stop and remove volumes (⚠️ deletes database)
docker-compose down -v
```

## Common Issues

### Port Already in Use

```bash
# Change ports in docker-compose.yml
# Backend: "8001:8000"
# Frontend: "3001:80"
# Database: "5433:5432"
```

### Database Connection Failed

```bash
# Check if PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs db

# Connect manually
docker-compose exec db psql -U postgres business_outreach
```

### Frontend Can't Reach Backend

```bash
# Check CORS settings in backend/.env
# Make sure frontend URL is in CORS_ORIGINS

# Check network
docker-compose exec frontend ping backend
```

---

**Ready to Go!** 🚀

Check `WEB_APP_README.md` for full documentation.

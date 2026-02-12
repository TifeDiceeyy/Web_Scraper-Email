# Business Outreach Automation - Web Application

## Overview

This is a transformation of the CLI-based Business Outreach Automation tool into a modern, multi-user web application with:

- **Frontend**: React 18 + Vite + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT-based multi-user auth
- **Deployment**: Docker containers (AWS-ready)

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  React Frontend │ ───> │  FastAPI Backend │ ───> │   PostgreSQL    │
│  (Port 3000)    │      │   (Port 8000)    │      │   (Port 5432)   │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │
                                  v
                         ┌────────────────┐
                         │ Existing Tools │
                         │ (Reused 100%)  │
                         └────────────────┘
```

## What's Been Implemented

### Backend (FastAPI) ✅

#### Core Infrastructure
- [x] FastAPI application setup
- [x] PostgreSQL database models (User, UserSettings, Campaign)
- [x] JWT authentication (access + refresh tokens)
- [x] Password hashing (bcrypt)
- [x] API key encryption for user credentials
- [x] CORS middleware configuration

#### API Endpoints
- [x] **Authentication**
  - POST `/api/auth/register` - User registration
  - POST `/api/auth/login` - Login with JWT
  - GET `/api/auth/me` - Get current user
  - GET `/api/auth/settings` - Get user settings (masked)
  - PUT `/api/auth/settings` - Update API keys/credentials
  - POST `/api/auth/logout` - Logout

- [x] **Campaigns**
  - GET `/api/campaigns` - List user's campaigns
  - POST `/api/campaigns` - Create campaign
  - GET `/api/campaigns/{id}` - Get campaign details
  - PUT `/api/campaigns/{id}` - Update campaign
  - DELETE `/api/campaigns/{id}` - Delete campaign
  - GET `/api/campaigns/stats` - Get dashboard statistics

- [x] **Business Workflows**
  - POST `/api/campaigns/{id}/scrape` - Scrape Google Maps (Workflow 1)
  - POST `/api/campaigns/{id}/businesses/upload` - Upload JSON
  - POST `/api/campaigns/{id}/generate-emails` - Generate emails (Workflow 2)
  - POST `/api/campaigns/{id}/send-approved` - Send emails (Workflow 4)
  - POST `/api/campaigns/{id}/track-responses` - Track responses (Workflow 5)
  - GET `/api/campaigns/{id}/responses` - Get responses

#### Service Layer
- [x] `ScraperService` - Wraps scrape_google_maps
- [x] `EmailGenerationService` - Wraps generate_*_email tools
- [x] `SheetsService` - Wraps Google Sheets operations
- [x] `GmailService` - Wraps send_emails
- [x] `TrackingService` - Wraps track_responses

**Note**: All existing tools in `tools/` are reused without modification via service wrappers.

### Frontend (React + Vite + Tailwind) ✅

#### Core Setup
- [x] Vite + React 18 project
- [x] Tailwind CSS configuration
- [x] React Router for navigation
- [x] React Query for data fetching
- [x] Axios API client with interceptors
- [x] Toast notifications (react-hot-toast)

#### Authentication
- [x] AuthContext for global auth state
- [x] Login page with error handling
- [x] Protected route wrapper
- [x] JWT token management

#### Pages
- [x] Login page
- [x] Dashboard with statistics
- [ ] Register page (TODO)
- [ ] Campaign creation wizard (TODO)
- [ ] Campaign detail page (TODO)
- [ ] Business list/management (TODO)
- [ ] Email review/approval UI (TODO)
- [ ] Settings page for API keys (TODO)

#### API Integration
- [x] `api/client.js` - Axios instance with auth
- [x] `api/auth.js` - Auth endpoints
- [x] `api/campaigns.js` - Campaign endpoints

### Deployment ✅

- [x] Backend Dockerfile (Gunicorn + Uvicorn)
- [x] Frontend Dockerfile (Multi-stage with Nginx)
- [x] docker-compose.yml for local development
- [x] Nginx configuration
- [x] Environment variable templates

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── config.py            # Settings
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── dependencies.py      # FastAPI dependencies
│   │   ├── models/              # Database models
│   │   │   ├── user.py
│   │   │   └── campaign.py
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── campaign.py
│   │   │   └── business.py
│   │   ├── api/                 # Route handlers
│   │   │   ├── auth.py
│   │   │   ├── campaigns.py
│   │   │   └── businesses.py
│   │   ├── core/                # Auth & security
│   │   │   ├── auth.py          # JWT functions
│   │   │   └── security.py      # Password & encryption
│   │   └── services/            # Business logic wrappers
│   │       ├── scraper.py
│   │       ├── email_gen.py
│   │       ├── sheets.py
│   │       ├── gmail.py
│   │       └── tracking.py
│   ├── requirements-api.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main component with routing
│   │   ├── api/                 # API client
│   │   │   ├── client.js
│   │   │   ├── auth.js
│   │   │   └── campaigns.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── pages/
│   │   │   ├── Auth/
│   │   │   │   └── Login.jsx
│   │   │   └── Dashboard/
│   │   │       └── Dashboard.jsx
│   │   └── components/          # (TODO)
│   ├── package.json
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env.example
│
├── tools/                       # Existing tools (unchanged)
│   ├── scrape_google_maps.py
│   ├── generate_general_email.py
│   ├── generate_specific_email.py
│   ├── send_emails.py
│   └── track_responses.py
│
└── docker-compose.yml           # Local development setup
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or use Docker)
- Docker & Docker Compose (optional, recommended)

### Option 1: Docker (Recommended)

1. **Generate security keys**:
   ```bash
   # JWT secret
   python -c "import secrets; print(secrets.token_urlsafe(32))"

   # Encryption key
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

2. **Create `.env` file**:
   ```bash
   cat > .env << EOF
   JWT_SECRET_KEY=<your-jwt-secret>
   ENCRYPTION_KEY=<your-encryption-key>
   EOF
   ```

3. **Start all services**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend

1. **Create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements-api.txt
   ```

3. **Set up PostgreSQL** and create database:
   ```sql
   CREATE DATABASE business_outreach;
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

5. **Run the API**:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit VITE_API_URL if needed
   ```

3. **Start dev server**:
   ```bash
   npm run dev
   ```

## User Workflow

### 1. Registration & Setup
1. Create account at `/register`
2. Login at `/login`
3. Navigate to `/settings` to configure:
   - Gemini API key
   - Gmail credentials
   - Google Sheet ID (per campaign)
   - Telegram bot (optional)

### 2. Create Campaign
1. Go to `/campaigns/create`
2. Enter campaign details:
   - Name, business type
   - Outreach strategy (general vs specific)
   - Data source (Google Maps, JSON, manual)
3. Campaign created with dedicated Google Sheet

### 3. Scrape Businesses (Workflow 1)
- Click "Scrape Businesses" on campaign page
- System scrapes Google Maps
- Results uploaded to campaign's Google Sheet
- Real-time progress updates (TODO: WebSocket)

### 4. Generate Emails (Workflow 2)
- Click "Generate Emails"
- AI generates personalized emails for all draft businesses
- Uses user's Gemini API key
- Updates Google Sheet with subject + body

### 5. Review & Approve
- View generated emails
- Approve/reject individually or bulk
- Edit if needed

### 6. Send Emails (Workflow 4)
- Click "Send Approved Emails"
- System sends via user's Gmail
- Updates sheet status to "Sent"
- Rate limiting applied

### 7. Track Responses (Workflow 5)
- Click "Track Responses"
- System monitors Gmail for replies
- Updates sheet with response details
- Shows statistics on dashboard

## Multi-User Isolation

- Each user has separate account with encrypted credentials
- Each campaign has its own Google Sheet (isolated data)
- API keys stored encrypted per user
- JWT authentication ensures users only access their own data

## What Still Needs to Be Done

### High Priority

1. **Frontend Pages** (Tasks #9, #10):
   - [ ] Register page
   - [ ] Campaign creation wizard (multi-step form)
   - [ ] Campaign detail page
   - [ ] Business list with filters/search
   - [ ] Email review/approval UI
   - [ ] Settings page for API keys
   - [ ] Response tracking dashboard

2. **Real-time Features** (Tasks #6, #11):
   - [ ] WebSocket endpoint in backend
   - [ ] WebSocket hook in frontend
   - [ ] Real-time progress bars
   - [ ] Live status updates

3. **Google Sheet Creation**:
   - [ ] Implement automatic sheet creation per campaign
   - [ ] Use Google Sheets API to create/configure sheets
   - [ ] Set proper permissions

### Medium Priority

4. **Enhanced Workflows**:
   - [ ] Background tasks for long-running operations
   - [ ] Queue system for email sending
   - [ ] Retry logic for failed operations
   - [ ] Better error handling and user feedback

5. **Database Improvements**:
   - [ ] Alembic migrations
   - [ ] Database indexes for performance
   - [ ] Add business table (optional - could stay sheet-only)

6. **Testing**:
   - [ ] Backend unit tests (pytest)
   - [ ] API integration tests
   - [ ] Frontend component tests
   - [ ] E2E tests (Playwright)

### Low Priority

7. **AWS Deployment** (Task #13):
   - [ ] GitHub Actions workflows
   - [ ] AWS App Runner configuration
   - [ ] RDS PostgreSQL setup
   - [ ] Secrets Manager integration
   - [ ] CloudWatch logging

8. **Nice-to-Haves**:
   - [ ] Email templates library
   - [ ] Campaign analytics/reports
   - [ ] A/B testing for emails
   - [ ] Export functionality
   - [ ] Mobile app (React Native)

## API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Security Considerations

✅ **Implemented**:
- JWT authentication with refresh tokens
- Password hashing with bcrypt
- API key encryption in database (Fernet)
- CORS configuration
- SQL injection protection (SQLAlchemy ORM)
- Input validation (Pydantic)

⚠️ **TODO**:
- Rate limiting (implement with slowapi)
- Email verification
- Password reset flow
- 2FA (optional)
- API key rotation
- Session management improvements

## Cost Estimation

### AWS Deployment (Monthly)

**App Runner (Recommended)**:
- Backend: ~$25 (0.25 vCPU, 0.5GB RAM)
- Frontend: ~$5 (static Nginx) OR free with S3+CloudFront
- RDS PostgreSQL t3.micro: ~$15
- Secrets Manager: ~$1
- **Total: ~$46/month** (can optimize to $30 with S3)

**EC2 Alternative**:
- t3.medium instance: ~$30
- EBS storage: ~$8
- **Total: ~$38/month**

### Third-Party Services
- Gemini API: Pay-as-you-go (per user)
- Google Workspace: $6-$18/user/month (for Gmail + Sheets)
- Apify (scraping): Pay-as-you-go

## Troubleshooting

### Backend won't start
```bash
# Check database connection
psql -h localhost -U postgres -d business_outreach

# Check environment variables
echo $DATABASE_URL

# View logs
docker-compose logs backend
```

### Frontend can't connect to API
```bash
# Check VITE_API_URL in .env
cat frontend/.env

# Verify CORS settings in backend/.env
# Make sure frontend URL is in CORS_ORIGINS
```

### Database migrations
```bash
# Create migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Contributing

1. Create feature branch
2. Make changes
3. Test locally with Docker
4. Submit pull request

## License

MIT

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/business-outreach-web/issues
- Email: support@example.com

---

**Built with ❤️ using FastAPI, React, and Claude Code**

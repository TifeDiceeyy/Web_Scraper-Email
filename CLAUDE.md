# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Web Scraper Email** is a Python-based web scraping and email automation tool.

**Vision:** "Automated data extraction and intelligent email delivery at scale"

**Current State:** This repository is **scaffolded and ready for development**. Documentation, workflow commands, and skills are in place.

### Target Users

**Primary Market:** Developers and data analysts who need automated web scraping with email notifications

**Why This Matters:**

- Automates repetitive data collection tasks
- Provides timely notifications via email
- Free and self-hosted solution (no API costs)

---

## ⚠️ CRITICAL: Read Skills BEFORE Coding

**BEFORE implementing ANY feature, Claude will automatically activate relevant skills based on context.**

### 📖 Available Skills

Skills are interactive documentation that Claude activates on-demand:

1. **`.claude/skills/development-workflow/`** ⭐ CORE
   - Feature development process (10-step SOP)
   - Git workflow and conventions
   - Implementation planning templates
   - **Triggers:** "How do I implement features?", "Git workflow?", "Create implementation plan"

2. **`.claude/skills/project-standards/`** (Full mode only)
   - User story format and acceptance criteria
   - Documentation conventions
   - Code review standards
   - **Triggers:** "User story format?", "Documentation standards?", "Acceptance criteria?"

3. **`.claude/skills/exploration-helpers/`** (Full mode only)
   - Database exploration patterns
   - Codebase navigation guidance
   - Python code analysis approaches
   - **Triggers:** "Explore the database", "Understand codebase", "Analyze Python modules"

### 🚨 Why Skills Matter

- **On-demand:** Claude activates them when context matches
- **Interactive:** Ask questions, get detailed guidance
- **Maintainable:** Update skills as patterns evolve
- **Consistent:** Same knowledge base for all development

### 🔧 Skills Maintenance (IMPORTANT)

**Claude MUST keep skills accurate and up-to-date.**

**After completing any feature, review affected skills:**

1. **Add** new patterns discovered during implementation
2. **Update** outdated information that no longer applies
3. **Remove** incorrect or misleading guidance
4. **Consolidate** redundant sections

**When to update skills:**

- New tech stack patterns established
- Better approaches discovered
- Original guidance caused issues
- Project conventions changed

**How to propose skill updates:**

```
"I noticed the [skill-name] skill says X, but we're actually doing Y.
Should I update the skill to reflect this?"
```

**Never let skills become stale** - they should always reflect current project reality.

---

## Quick Start for Claude

### Key Files & Purposes

| File/Directory          | Purpose                                     |
| ----------------------- | ------------------------------------------- |
| `CLAUDE.md`             | This file - project hub and quick reference |
| `.claude/settings.json` | Hooks for auto-formatting                   |
| `.claude/commands/`     | Workflow commands for feature development   |
| `.claude/skills/`       | Interactive skills for guidance             |
| `.claude/project/`      | Project tracking (features, plans, roadmap) |

### Project Tracking

All project management files are in `.claude/project/`:

| File                         | Purpose                                                   |
| ---------------------------- | --------------------------------------------------------- |
| `high-level-user-stories.md` | ⭐ **START HERE** - Progress tracker for all user stories |
| `roadmap.md`                 | Phased implementation plan                                |
| `features/`                  | User story specifications (`us-XXX-name.md`)              |
| `plans/`                     | Implementation plans (`us-XXX-plan.md`)                   |

### Tech Stack

**Python 3.11+** - Core language

**Web Scraping:**
- **BeautifulSoup4** - HTML/XML parsing
- **Requests** - HTTP library
- **lxml** - Fast XML/HTML parser (optional)
- **Selenium** - For JavaScript-heavy sites (optional)

**Email:**
- **smtplib** - Built-in SMTP client
- **email** - Email message construction

**Data & Storage:**
- **SQLite** or **JSON** - Data persistence
- **pandas** - Data manipulation (optional)

**Scheduling:**
- **schedule** - Task scheduling
- **APScheduler** - Advanced scheduling (optional)

**Testing:**
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting

### Development Commands

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python main.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black .

# Lint code
flake8 src/
pylint src/
```

---

## Feature Development Workflow

This project follows a structured workflow (see `development-workflow` skill):

```
1. Story  → Create in .claude/project/features/
2. Plan   → Create in .claude/project/plans/
3. Approve → Get user approval before coding
4. Build  → Implement following the plan
```

**When you ask to build a feature, Claude will first create the story and plan.**

### 🚀 Quick Start with `/implement`

Run `/implement` to start the complete workflow:

```
/implement
```

This orchestrates all phases automatically with approval gates.

### 📋 Individual Phase Commands

1. **Phase 1+2: Discovery** → `/discovery`
   - Explores current app state
   - Reads documentation and standards
   - Asks clarifying questions

2. **Phase 3: Plan & Validate** → `/plan-and-validate`
   - Creates detailed implementation plan
   - Validates against schema and types
   - Presents plan for approval

3. **Phase 4: Implementation** → `/start-implementation`
   - Implements from approved plan
   - Tests comprehensively
   - Documents and commits

4. **Phase 4.5: Review** → `/review-implementation`
   - Reviews code quality
   - Checks standards compliance
   - Validates test coverage

### ⚡ Navigation Helper

Use `/next` to automatically proceed to the next phase.

---

## Development Workflow

### For EVERY Feature:

1. ✅ **Read relevant skills** - Ask about the topic, Claude activates appropriate skill
2. ✅ **Review existing patterns** - Check similar code in the codebase
3. ✅ **Implement following standards** - Follow patterns from skills
4. ✅ **Write tests** - Follow testing patterns
5. ✅ **Verify quality gates pass** - Lint, test, build
6. ✅ **Commit with conventional format** - feat:, fix:, chore:, etc.

**If you deviate from standards:**

- Document WHY in code comments
- Propose update to the skill if pattern is better
- Get user approval for major changes

---

## Claude Code Agent Usage

### When to Use Specialized Agents

**DO use agents for:**

- Complex multi-step implementation
- Codebase exploration
- Security reviews
- Creating comprehensive test suites

**DON'T use agents for:**

- Reading a specific file path (use Read tool)
- Searching for specific class/function (use Glob/Grep)
- Single straightforward tasks

### Recommended Agents

- **Explore Agent** - Codebase navigation
- **backend-api-engineer** - API implementation
- **solution-architect** - Architectural decisions
- **qa-automation-engineer** - Testing strategy

---

## Git Workflow

**Branching:** Feature branches (`feature/<description>`)

**Commits:** Conventional Commits format

```bash
git commit -m "feat: add [feature name]

- [Implementation detail]
- [Implementation detail]

"
```

**Types:** `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

---

## Project Structure

```
Web Scraper Email/
├── CLAUDE.md                    # This file
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── .claude/                     # Claude Code configuration
│   ├── settings.json            # Auto-formatting hooks
│   ├── commands/                # Workflow commands
│   ├── skills/                  # Interactive skills
│   └── project/                 # Project tracking
├── src/                         # Source code
│   ├── __init__.py
│   ├── scrapers/                # Web scraping modules
│   │   ├── __init__.py
│   │   ├── base_scraper.py      # Base scraper class
│   │   └── site_scrapers.py     # Site-specific scrapers
│   ├── email_service/           # Email functionality
│   │   ├── __init__.py
│   │   ├── smtp_client.py       # SMTP email client
│   │   └── templates.py         # Email templates
│   ├── utils/                   # Utilities
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration loader
│   │   └── logger.py            # Logging setup
│   └── storage/                 # Data persistence
│       ├── __init__.py
│       └── database.py          # Database operations
├── tests/                       # Test files
│   ├── __init__.py
│   ├── test_scrapers.py
│   └── test_email.py
├── data/                        # Data storage
│   └── scraped_data.db
├── logs/                        # Application logs
└── main.py                      # Entry point
```

---

## Python Best Practices

### Code Style
- Follow **PEP 8** style guide
- Use **type hints** for function signatures
- Maximum line length: 88 characters (Black default)
- Use **docstrings** for classes and functions

### Error Handling
- Use try/except blocks for network requests
- Implement retry logic for failed scrapes
- Log all errors with context
- Handle rate limiting gracefully

### Security
- **Never commit** `.env` files or credentials
- Use environment variables for sensitive data
- Validate and sanitize scraped data
- Respect robots.txt and rate limits

### Performance
- Use connection pooling for requests
- Implement caching where appropriate
- Process data in batches
- Use async/await for concurrent scraping (optional)

---

## Next Steps

1. ✅ **CLAUDE.md customized** - Python stack configured
2. **Create virtual environment** - Run `python -m venv venv`
3. **Create requirements.txt** - List your dependencies
4. **Set up project structure** - Create src/, tests/, data/ directories
5. **Start implementing** - Run `/implement` to begin your first feature

**Ready to start building?** Try:
- `/implement` - Start the full feature workflow
- Or tell me what you want to build first!

---

**This document will evolve as the project is implemented. Update it when new patterns emerge or architectural decisions are made.**

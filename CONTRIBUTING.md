# Contributing to Business Outreach Automation

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/business-outreach-automation.git
cd business-outreach-automation
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make install-dev
# Or: pip install -r requirements-dev.txt

# Validate environment
make validate
# Or: python validate_env.py
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# Or: git checkout -b fix/your-bug-fix
```

## Development Workflow

### Making Changes

1. **Write Code**
   - Follow existing code style
   - Add docstrings to functions/classes
   - Keep functions focused (single responsibility)

2. **Format Code**
   ```bash
   make format
   # Or: black tools/ tests/ --line-length=100
   ```

3. **Run Linters**
   ```bash
   make lint
   # Or: flake8 tools/ --max-line-length=100
   ```

4. **Write Tests**
   - Add tests for new features
   - Update tests for bug fixes
   - Aim for 80%+ coverage

5. **Run Tests**
   ```bash
   make test
   # Or with coverage:
   make test-cov
   ```

### Code Style Guidelines

**Python Style:**
- Follow PEP 8
- Use black formatter (line length: 100)
- Use type hints where helpful
- Write descriptive variable names

**Docstrings:**
```python
def function_name(arg1, arg2):
    """
    Brief description of function.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When this happens
    """
```

**Error Handling:**
- Use try/except for expected errors
- Log errors with context
- Provide helpful error messages
- Use tenacity for retries

### Testing Guidelines

**Test Structure:**
```python
import pytest

class TestFeature:
    """Test feature description"""

    def test_happy_path(self):
        """Test normal operation"""
        # Arrange
        input_data = "test"

        # Act
        result = function(input_data)

        # Assert
        assert result == expected
```

**What to Test:**
- Happy path (normal operation)
- Edge cases (empty input, max values)
- Error conditions (invalid input)
- Integration points (API calls, file I/O)

**Mocking:**
- Mock external APIs (Gemini, Gmail, Sheets)
- Mock file I/O when testing logic
- Use pytest fixtures for common setup

### Commit Guidelines

**Commit Message Format:**
```
type(scope): brief description

Longer explanation if needed.

- Bullet points for details
- Reference issues: Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(email): add retry logic for failed sends

- Retry up to 3 times with exponential backoff
- Log each retry attempt
- Fixes #42

fix(validation): handle empty email addresses

- Add check for empty string before regex
- Return clear error message
- Add test case for empty email
```

## Project Structure

```
business-outreach-automation/
├── agent.py              # Main orchestrator
├── constants.py          # Configuration constants
├── logger.py             # Logging setup
├── validators.py         # Input validation
│
├── tools/                # Execution layer
│   ├── generate_*.py     # Email generation
│   ├── scrape_*.py       # Data collection
│   ├── *_sheets.py       # Google Sheets operations
│   └── notify.py         # Notifications
│
├── workflows/            # Workflow documentation
│   └── *.md              # Step-by-step workflows
│
├── tests/                # Test files
│   ├── test_*.py         # Unit tests
│   └── README.md         # Testing guide
│
└── data/                 # Sample data
    └── sample_*.json     # Test data files
```

## Adding New Features

### 1. New Tool
If adding a new tool in `tools/`:

1. Create `tools/your_tool.py`
2. Add docstrings and error handling
3. Import in `tools/__init__.py`
4. Add workflow in `workflows/your_workflow.md`
5. Write tests in `tests/test_your_tool.py`
6. Update README if user-facing

### 2. New Email Strategy
If adding a third email strategy:

1. Create `tools/generate_new_strategy.py`
2. Update `constants.py` with new strategy constant
3. Update `agent.py` → `ask_outreach_type()`
4. Add tests
5. Document in workflows

### 3. New Data Source
If adding a new data collection method:

1. Create tool in `tools/`
2. Update `agent.py` → `ask_data_source()`
3. Update `agent.py` → `collect_businesses()`
4. Add validation if needed
5. Add sample data file
6. Write tests

## Pull Request Process

1. **Before Submitting:**
   - [ ] Code is formatted (`make format`)
   - [ ] Tests pass (`make test`)
   - [ ] Linters pass (`make lint`)
   - [ ] Documentation updated
   - [ ] Changelog updated (if applicable)

2. **PR Description:**
   - Describe what changed and why
   - Link related issues
   - Include screenshots if UI changes
   - Note any breaking changes

3. **Review Process:**
   - Address reviewer feedback
   - Keep commits clean
   - Update branch if needed

4. **After Merge:**
   - Delete your branch
   - Close related issues

## Questions?

- Open an issue for bugs or feature requests
- Ask questions in discussions
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Thank you for contributing!** 🎉

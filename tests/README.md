# Tests for Business Outreach Automation

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest tests/test_email_generation.py
```

### Run with coverage:
```bash
pytest --cov=tools --cov-report=html
```

### Run with verbose output:
```bash
pytest -v
```

## Test Files

- `test_email_generation.py` - Tests for email generation (general + specific)
- `test_config_manager.py` - Tests for configuration management

## Writing New Tests

Follow pytest conventions:
1. Test files start with `test_`
2. Test classes start with `Test`
3. Test methods start with `test_`
4. Use fixtures for setup/teardown
5. Use mocks to avoid API calls during testing

## Coverage Target

Aim for 80%+ coverage on all tools.

# Testing

## Installation

```bash
pip install -r requirements-test.txt
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_validator.py

# Run with verbose output
pytest -v

# Run only unit tests (fast)
pytest tests/test_validator.py tests/test_cleaner.py tests/test_chunker.py

# Run integration tests
pytest tests/test_pipeline.py
```

## Test Structure

```
tests/
├── __init__.py
├── test_validator.py    # File validation tests
├── test_cleaner.py      # Text cleaning tests
├── test_chunker.py      # Smart chunking tests
└── test_pipeline.py     # Integration tests
```

## Coverage

After running tests with coverage:
```bash
# Open HTML coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

## Writing New Tests

Follow pytest conventions:
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Use fixtures for setup
- Use `@pytest.mark.asyncio` for async tests

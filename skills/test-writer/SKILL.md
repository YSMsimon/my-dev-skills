---
name: test-writer
description: Write unit tests, integration tests, and test fixtures for any function, class, module, or API endpoint. Use this skill whenever the user wants to write tests, increase test coverage, test edge cases, set up pytest fixtures, mock external dependencies, test database operations, test an API endpoint, or debug a failing test. Trigger on phrases like "write tests for", "add unit tests", "test this function", "how do I test", "mock this", "pytest", "test coverage", "failing test", or "fixture".
---

# Test Writer

Write tests that actually catch bugs — not just tests that make coverage numbers go up.

---

## Core principles

**Test behaviour, not implementation.** Renaming a private variable should never break a test.

**Each test tests one thing.** One assertion (or closely related assertions) per test.

**Arrange-Act-Assert.** Set up state → call the thing → verify the result.

**Tests are documentation.** The test name and body should tell a reader what the code does.

---

## Naming

```python
# Pattern: test_<function>_<scenario>_<expected>
def test_get_user_by_email_returns_user_when_found():
def test_get_user_by_email_returns_none_when_missing():
def test_add_message_raises_on_empty_content():
def test_semantic_search_excludes_provided_ids():
```

---

## pytest patterns

### Testing exceptions
```python
def test_run_raises_value_error_on_empty_message():
    with pytest.raises(ValueError, match="message cannot be empty"):
        agent.run("")
```

### Parametrize — avoid duplicated test bodies
```python
@pytest.mark.parametrize("input,expected", [
    ("Hello World", "hello-world"),
    ("  spaces  ",  "spaces"),
    ("",            ""),
])
def test_slugify(input, expected):
    assert slugify(input) == expected
```

### Fixtures
```python
@pytest.fixture(scope="session")
def pg_connection():
    conn = psycopg2.connect(os.getenv("TEST_DATABASE_URL"))
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def rollback(pg_connection):
    yield
    pg_connection.rollback()
```

---

## Running tests

```bash
pytest                              # all tests
pytest tests/test_db.py             # specific file
pytest -k "profile"                 # tests matching name pattern
pytest -v                           # verbose
pytest -x                           # stop on first failure
pytest -s                           # show print output
pytest --cov=. --cov-report=term-missing  # coverage report
```

---

## Common issues

### Test passes alone but fails in suite
Use an `autouse` rollback fixture — state is leaking between tests.

### Mock not taking effect
```python
# Wrong: patching the library
with patch("smtplib.SMTP"):

# Right: patching where the name is looked up
with patch("myapp.email.smtplib.SMTP"):
```

### "fixture 'X' not found"
`conftest.py` must be in the `tests/` directory. Run pytest from the project root.

---

## Additional resources

- For project-specific examples (DB, mocking Ollama, threading), see [examples.md](examples.md)
- For shared fixtures, see [scripts/conftest.py](scripts/conftest.py)
- For test file template, see [template/test_file.py](template/test_file.py)

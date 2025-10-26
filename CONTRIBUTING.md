# Contributing to JSON Prompting LLM Examples

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment. We expect all contributors to:

- Be respectful and considerate
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling or insulting remarks
- Publishing others' private information
- Other unprofessional conduct

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**Bug Report Template:**
1. Description of the bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, etc.)
6. Screenshots if applicable

### Suggesting Features

Feature requests are welcome! Please provide:

1. Clear description of the feature
2. Use case and motivation
3. Example implementation (if applicable)
4. Potential alternatives considered

### Pull Requests

#### Before Starting

1. Check existing issues and PRs
2. Create an issue to discuss major changes
3. Fork the repository
4. Create a feature branch

#### Development Process

1. **Set Up Development Environment**

```bash
git clone https://github.com/YOUR_USERNAME/json-prompting-llm-examples.git
cd json-prompting-llm-examples
pip install -r requirements.txt
pip install -e .[dev]
```

2. **Create a Branch**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test additions/modifications
- `refactor/` - Code refactoring

3. **Make Your Changes**

Follow our code standards:

- **Code Style**: Follow PEP 8
- **Type Hints**: Use type annotations
- **Docstrings**: Include comprehensive docstrings
- **Comments**: Explain complex logic

Example:

```python
def extract_invoice_data(text: str) -> dict[str, Any]:
    """
    Extract structured data from invoice text.

    Args:
        text: Raw invoice text to process

    Returns:
        Dictionary containing extracted invoice fields

    Raises:
        ValueError: If text is empty or invalid
    """
    if not text:
        raise ValueError("Invoice text cannot be empty")
    # Implementation
```

4. **Add Tests**

All new features must include tests:

```python
def test_extract_invoice_data():
    """Test invoice data extraction with valid input."""
    sample_text = "Invoice #123..."
    result = extract_invoice_data(sample_text)
    assert result["invoice_number"] == "123"
    assert "total_amount" in result
```

5. **Run Tests Locally**

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_prompts.py -v

# Run linting
flake8 .
black --check .
mypy .
```

6. **Update Documentation**

- Update README.md if adding new examples
- Add docstrings to all functions/classes
- Update relevant documentation in `docs/`
- Add entry to CHANGELOG.md

7. **Commit Changes**

Follow conventional commits:

```bash
git add .
git commit -m "feat: add resume parsing example"
git commit -m "fix: correct JSON schema validation"
git commit -m "docs: update API examples"
git commit -m "test: add edge case for email summarization"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `style:` - Formatting changes
- `chore:` - Maintenance tasks

8. **Push and Create PR**

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title describing the change
- Detailed description of what and why
- Reference to related issues
- Screenshots if applicable

#### PR Review Process

1. Automated checks must pass (tests, linting)
2. Code review by maintainers
3. Requested changes addressed
4. Final approval and merge

## Development Standards

### Code Quality

1. **Type Hints**: Required for all functions

```python
def process_text(text: str, max_length: int = 100) -> dict[str, str]:
    pass
```

2. **Docstrings**: Required for all public functions/classes

```python
def complex_function(param1: str, param2: int) -> bool:
    """
    Brief description.

    Longer description if needed with implementation details
    and usage examples.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
        TypeError: When wrong type provided
    """
```

3. **Error Handling**: Handle errors gracefully

```python
try:
    result = api_call()
except APIError as e:
    logger.error(f"API call failed: {e}")
    raise
```

### Testing Standards

1. **Coverage**: Aim for >80% code coverage
2. **Edge Cases**: Test boundary conditions
3. **Mocking**: Mock external API calls
4. **Fixtures**: Use pytest fixtures for common setup

Example test structure:

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_feature_success(sample_data):
    """Test successful execution."""
    result = my_function(sample_data)
    assert result is not None

def test_feature_error():
    """Test error handling."""
    with pytest.raises(ValueError):
        my_function(None)

@patch('module.api_call')
def test_with_mock(mock_api):
    """Test with mocked API."""
    mock_api.return_value = {"status": "success"}
    result = function_using_api()
    assert result["status"] == "success"
```

### Documentation Standards

1. **README Updates**: Document new features
2. **Example Code**: Provide usage examples
3. **API Reference**: Document all public APIs
4. **Changelog**: Update for all user-facing changes

## Project-Specific Guidelines

### Adding New Examples

When adding a new example to `examples/`:

1. Create a new Python file with descriptive name
2. Include comprehensive docstring at top
3. Provide multiple use cases
4. Add error handling
5. Include sample output in comments
6. Update README.md with new example
7. Add tests in `tests/`

Template:

```python
"""
Module: examples/new_example.py
Description: Brief description of what this example demonstrates

This example shows how to...

Usage:
    python examples/new_example.py

Requirements:
    - API key for service X
    - Python 3.9+
"""

import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main execution function."""
    # Implementation
    pass

if __name__ == "__main__":
    main()
```

### Adding AssemblyAI Examples

For speech-to-text examples in `assemblyai/`:

1. Use AssemblyAI best practices
2. Handle audio file validation
3. Implement proper error handling
4. Document audio format requirements
5. Provide sample audio URLs or files

### Updating Documentation

For documentation updates in `docs/`:

1. Use clear, concise language
2. Include code examples
3. Provide visual aids if helpful
4. Cross-reference related docs
5. Update table of contents

## Getting Help

### Resources

- [Python Style Guide](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [AssemblyAI Docs](https://www.assemblyai.com/docs)

### Communication

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Pull Request Comments: Code review discussions

### Response Time

- Issues: Typically responded to within 48 hours
- Pull Requests: Initial review within 3-5 days
- Security Issues: Addressed immediately

## Recognition

Contributors will be:
- Listed in repository contributors
- Mentioned in release notes for significant contributions
- Credited in documentation for major features

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to JSON Prompting LLM Examples!

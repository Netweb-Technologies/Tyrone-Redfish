# Contributing to TyroneFish

We welcome contributions to TyroneFish! This guide will help you get started with contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.6 or higher
- Git
- A GitHub account
- Basic knowledge of Redfish API
- Familiarity with Python development

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/Netweb-Technologies/tyrone-redfish.git
   cd tyrone-redfish
   ```

3. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If exists
   ```

5. **Set up pre-commit hooks** (if configured):
   ```bash
   pre-commit install
   ```

## Development Setup

### Project Structure

```
TyroneFish/
├── Python Scripts/
│   └── Redfish/
│       ├── GetSetPowerStateRedfish.py    # Power management
│       └── GetSetLedIndicatorRedfish.py  # LED indicator control
├── docs/                                 # Documentation
├── tests/                               # Test files (if exists)
├── requirements.txt                     # Dependencies
├── README.md                           # Project overview
└── mkdocs.yml                          # Documentation config
```

### Development Dependencies

Create a `requirements-dev.txt` file for development dependencies:

```txt
pytest>=6.0.0
pytest-cov>=2.10.0
flake8>=3.8.0
black>=21.0.0
mypy>=0.800
pre-commit>=2.10.0
mkdocs>=1.2.0
mkdocs-material>=7.0.0
```

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes** - Fix issues in existing code
- **New features** - Add new Redfish operations or server support
- **Documentation** - Improve or add documentation
- **Testing** - Add or improve tests
- **Examples** - Add usage examples and tutorials
- **Performance** - Optimize existing code

### Before You Start

1. **Check existing issues** to see if someone is already working on it
2. **Create an issue** to discuss major changes before implementing
3. **Search existing PRs** to avoid duplicate work
4. **Read the documentation** to understand the project structure

## Code Standards

### Python Code Style

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Imports**: Organized and sorted
- **Docstrings**: Google style

### Code Formatting

Use Black for code formatting:

```bash
# Format all Python files
black "Python Scripts/"

# Check formatting without changes
black --check "Python Scripts/"
```

### Linting

Use flake8 for linting:

```bash
# Lint all Python files
flake8 "Python Scripts/"
```

### Type Hints

Add type hints for new code:

```python
def get_power_state(self) -> Optional[str]:
    """Get current power state of the server.
    
    Returns:
        Current power state or None if error occurred.
    """
    pass
```

### Docstring Standards

Use Google-style docstrings:

```python
def set_power_state(self, action: str) -> bool:
    """Set power state of the server.
    
    Args:
        action: Power action to perform. Valid actions include:
            'On', 'ForceOff', 'GracefulShutdown', etc.
    
    Returns:
        True if action executed successfully, False otherwise.
        
    Raises:
        ValueError: If action is not supported.
        
    Example:
        >>> manager = RedfishPowerManager(host, user, pass)
        >>> success = manager.set_power_state("On")
        >>> if success:
        ...     print("Server powered on")
    """
    pass
```

## Testing

### Writing Tests

Create test files in the `tests/` directory:

```python
# tests/test_power_manager.py
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Python_Scripts.Redfish.GetSetPowerStateRedfish import RedfishPowerManager

class TestRedfishPowerManager:
    def test_init(self):
        """Test RedfishPowerManager initialization."""
        manager = RedfishPowerManager("localhost", "user", "pass")
        assert manager.host == "localhost"
        assert manager.username == "user"
        assert manager.port == 443
    
    @patch('requests.Session.request')
    def test_get_power_state_success(self, mock_request):
        """Test successful power state retrieval."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {"PowerState": "On"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        manager = RedfishPowerManager("localhost", "user", "pass")
        
        # Mock endpoint discovery
        manager.systems_endpoint = "https://localhost/redfish/v1/Systems/Self"
        
        result = manager.get_power_state()
        assert result == "On"
    
    @patch('requests.Session.request')
    def test_get_power_state_failure(self, mock_request):
        """Test power state retrieval failure."""
        mock_request.side_effect = Exception("Connection failed")
        
        manager = RedfishPowerManager("localhost", "user", "pass")
        result = manager.get_power_state()
        assert result is None
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov="Python Scripts"

# Run specific test file
pytest tests/test_power_manager.py

# Run specific test
pytest tests/test_power_manager.py::TestRedfishPowerManager::test_init
```

### Test Categories

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test component interactions
3. **Functional Tests**: Test complete workflows
4. **Mock Tests**: Test with mocked external dependencies

## Documentation

### Documentation Standards

- **Clear and concise** writing
- **Code examples** for all features
- **Complete API documentation**
- **Usage examples** and tutorials
- **Error handling** documentation

### Building Documentation

```bash
# Install MkDocs dependencies
pip install mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

### Documentation Structure

```
docs/
├── index.md                    # Home page
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── configuration.md
├── scripts/
│   ├── power-management.md
│   └── led-indicator.md
├── api/
│   ├── power-manager.md
│   └── led-indicator.md
├── examples/
│   ├── basic-usage.md
│   └── advanced.md
├── contributing.md
└── changelog.md
```

## Submitting Changes

### Commit Guidelines

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Add or modify tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(power): add support for new power actions
fix(led): handle null response in get_led_indicator
docs(api): update power manager documentation
test(power): add unit tests for error handling
```

### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test your changes**:
   ```bash
   pytest
   flake8 "Python Scripts/"
   black --check "Python Scripts/"
   ```

4. **Update documentation** if needed

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat(power): add new power action support"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass and coverage is maintained
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format
- [ ] No breaking changes (or clearly documented)
- [ ] PR description explains the changes

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Documentation
- [ ] Documentation updated
- [ ] Code examples provided
- [ ] API documentation updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No breaking changes
- [ ] Commit messages are clear
```

## Code Review Process

### As a Reviewer

- **Be constructive** and helpful
- **Test the changes** when possible
- **Check for edge cases** and error handling
- **Verify documentation** is accurate
- **Ensure backwards compatibility**

### As a Contributor

- **Respond to feedback** promptly
- **Make requested changes** or explain why not
- **Ask questions** if feedback is unclear
- **Be patient** during the review process

## Development Tips

### Setting Up Test Environment

```bash
# Create test configuration
cat > test_config.json << EOF
{
  "test_servers": [
    {
      "host": "test-server.local",
      "username": "testuser",
      "password": "testpass",
      "port": 443
    }
  ]
}
EOF
```

### Debugging Tips

1. **Use verbose output** in scripts for debugging
2. **Add logging** to track execution flow
3. **Test with mock servers** when possible
4. **Use debugger** for complex issues

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_function():
    logger.debug("Debug information")
    logger.info("General information")
    logger.warning("Warning message")
    logger.error("Error message")
```

### Common Development Tasks

```bash
# Run formatter and linter
black "Python Scripts/" && flake8 "Python Scripts/"

# Run tests with coverage
pytest --cov="Python Scripts" --cov-report=html

# Build and serve documentation
mkdocs serve

# Check for type issues
mypy "Python Scripts/"
```

## Getting Help

### Resources

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and discuss ideas
- **Documentation**: Comprehensive guides and API reference
- **Code Examples**: Working examples in the repository

### Contact

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

## Recognition

Contributors will be recognized in:

- **Contributors file**: Listed in CONTRIBUTORS.md
- **Release notes**: Mentioned in changelog
- **Documentation**: Credits in appropriate sections

Thank you for contributing to TyroneFish! 🐟

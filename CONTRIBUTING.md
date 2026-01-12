# Contributing to Thanos

First off, thank you for considering contributing to Thanos! It's people like you that make Thanos such a great tool for the security community.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```
**Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.9.5]
- Docker Version (if applicable): [e.g., 20.10.7]
- Browser (if UI issue): [e.g., Chrome 95]

**Additional Context**
Any other relevant information.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use case**: Describe the problem or limitation you're addressing
- **Proposed solution**: How you envision the feature working
- **Alternatives considered**: Other approaches you've thought about
- **Additional context**: Mockups, examples, or references

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if applicable
4. **Update documentation** for user-facing changes
5. **Ensure tests pass** (if test infrastructure exists)
6. **Submit a pull request** with a clear description

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip
- Docker (optional)

### Local Setup

1. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/thanos.git
cd thanos
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
cd src
pip install -r requirements.txt
```

4. Initialize test database:
```bash
python load_data.py -f data/default.yaml
python load_data.py -f data/init/controls.yaml
```

5. Run the application:
```bash
streamlit run streamlit_app/app.py
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some flexibility. Key points:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Aim for 80-100 characters, max 120
- **Imports**: Group standard library, third-party, and local imports
- **Naming**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`

### Code Quality

- **Docstrings**: Use for all public functions and classes
```python
def get_component_controls(component_id: str) -> List[Control]:
    """
    Get all applicable controls for a component.
    
    Args:
        component_id: The unique identifier of the component
        
    Returns:
        List of Control objects applicable to the component
    """
    # Implementation
```

- **Type Hints**: Use type hints for function parameters and returns
```python
from typing import List, Optional

def query_threats(category_id: Optional[str] = None) -> List[Threat]:
    pass
```

- **Error Handling**: Use try-except blocks appropriately
```python
try:
    session.commit()
except IntegrityError as e:
    session.rollback()
    logger.error(f"Failed to commit: {e}")
    raise
```

### Database Changes

When modifying the schema:

1. **Update `schema.py`**: Add/modify ORM models
2. **Update `load_data.py`**: Add support for new node types if needed
3. **Provide migration notes**: Document schema changes in PR description
4. **Test thoroughly**: Ensure backward compatibility or provide migration path

### YAML Configuration

When adding YAML-based configuration:

- Use consistent indentation (2 spaces)
- Include all required fields
- Provide examples in documentation

Example:
```yaml
nodes:
  - kind: component_type
    id: azure_function
    name: Azure Function
    category: serverless
    provider: azure
```

## Commit Messages

Write clear, concise commit messages:

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add PostgreSQL support for production deployments

- Add PostgreSQL connection configuration
- Update Docker Compose with postgres service
- Add migration notes to documentation

Closes #42
```

```
fix: Resolve duplicate control display in threat model view

Components were showing inherited controls multiple times.
Added deduplication in get_component_controls function.

Fixes #58
```

## Testing

### Manual Testing

Before submitting a PR, test:

1. **Fresh installation**: Clone and setup on a clean system
2. **Database operations**: Create, read, update operations
3. **UI interactions**: Navigate through all pages
4. **Edge cases**: Empty states, invalid inputs
5. **Cross-browser** (for UI changes): Chrome, Firefox, Safari

### Automated Testing (Future)

We're working on adding automated tests. Contributions to test infrastructure are welcome!

## Documentation

Update documentation for:

- **User-facing changes**: Update README.md or USAGE.md
- **Architecture changes**: Update ARCHITECTURE.md
- **New features**: Add examples and use cases
- **Breaking changes**: Clearly document migration path

## Areas for Contribution

Looking for ideas? Here are areas that need help:

### High Priority
- [ ] Automated testing framework
- [ ] Export threat models to PDF
- [ ] Enhanced component visualization
- [ ] PostgreSQL/MySQL support for production
- [ ] User authentication and multi-tenancy

### Medium Priority
- [ ] Integration with cloud providers (AWS, Azure, GCP)
- [ ] REST API for programmatic access
- [ ] Threat analytics dashboard
- [ ] Import threat models from other tools
- [ ] Compliance framework templates (SOC2, ISO27001, NIST)

### Documentation
- [ ] Video tutorials
- [ ] Example threat models for common architectures
- [ ] Best practices guide
- [ ] API documentation
- [ ] Internationalization

### Good First Issues
Look for issues labeled `good first issue` for beginner-friendly contributions.

## Review Process

1. **PR Submission**: Submit PR with clear description
2. **Automated Checks**: CI/CD will run (when implemented)
3. **Code Review**: Maintainers review code
4. **Feedback**: Address review comments
5. **Approval**: Once approved, PR will be merged
6. **Release**: Changes included in next release

## Community

- **GitHub Discussions**: Ask questions, share ideas
- **GitHub Issues**: Report bugs, request features
- **Pull Requests**: Contribute code

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor graphs

## Questions?

Feel free to:
- Open a GitHub Discussion
- Comment on related issues
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Thanos! 🎉

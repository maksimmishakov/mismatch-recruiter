# Contributing to Lamoda AI Recruiter

Thank you for your interest in contributing to the Lamoda AI Recruiter project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We are committed to providing a welcoming and inclusive environment.

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Docker (optional)
- Git

### Development Setup

1. Fork the repository
   ```bash
   git clone https://github.com/YOUR_USERNAME/lamoda-ai-recruiter.git
   cd lamoda-ai-recruiter
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. Set up database
   ```bash
   python manage.py db migrate
   python manage.py db upgrade
   ```

5. Run development server
   ```bash
   python app.py
   ```

## Contributing Guidelines

### Before You Start

1. Check existing issues and pull requests
2. Create an issue for significant changes
3. Discuss major features in discussions section
4. Follow the existing code style

### Branching Strategy

```
main (production-ready)
└── develop (development branch)
    ├── feature/* (new features)
    ├── bugfix/* (bug fixes)
    └── hotfix/* (urgent production fixes)
```

### Branch Naming Convention

- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/issue-description` - Urgent fixes
- `docs/documentation-update` - Documentation updates
- `test/test-description` - Test additions

### Commit Messages

Use clear, descriptive commit messages:

```
[TYPE] Brief description

Detailed explanation if needed (optional)

Related issue: #123
```

Types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Adding or updating tests
- `chore:` - Build, dependencies, etc.

### Code Standards

#### Python

- Follow PEP 8
- Use type hints
- Max line length: 100 characters
- Use meaningful variable names
- Document functions with docstrings

Example:
```python
def parse_resume(file_path: str) -> Dict[str, Any]:
    """
    Parse a resume file and extract information.
    
    Args:
        file_path: Path to the resume file
        
    Returns:
        Dictionary containing parsed resume data
    """
    pass
```

#### Git Hooks

We use pre-commit hooks for code quality:

```bash
pip install pre-commit
pre-commit install
```

This will automatically check code before commits.

### Testing

All contributions must include tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test
pytest tests/test_resume_parser.py
```

Minimum coverage requirement: 80%

### Pull Request Process

1. Create a descriptive PR title
2. Link related issues
3. Describe changes clearly
4. Include before/after for UI changes
5. Ensure all tests pass
6. Update documentation

#### PR Title Format

```
[TYPE] Brief description (#issue-number)
```

#### PR Description Template

```markdown
## Description
Brief description of changes

## Related Issues
#123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Changes Made
- Change 1
- Change 2

## Testing
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] Manual testing performed

## Documentation
- [ ] Updated relevant documentation
- [ ] Updated API docs
- [ ] Updated README
```

### Code Review

Expect feedback on:
- Code quality and style
- Test coverage
- Performance implications
- Documentation clarity

Address all feedback before approval.

## Documentation

### How to Update Documentation

1. Edit relevant markdown files in `/docs`
2. Follow existing formatting
3. Keep language simple and clear
4. Include examples when relevant
5. Update table of contents if needed

### Documentation Standards

- Use clear headings (H2/H3)
- Include code examples
- Add links to related docs
- Keep paragraphs short
- Use lists for clarity

## Reporting Issues

### Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

### Feature Requests

Include:
- Clear problem statement
- Proposed solution
- Alternative solutions
- Use cases
- Acceptance criteria

## Performance Guidelines

- Consider scalability
- Optimize database queries
- Use caching appropriately
- Profile code for bottlenecks
- Document performance implications

## Security Considerations

- Never commit secrets
- Use environment variables for configuration
- Validate all user input
- Follow OWASP guidelines
- Report security issues responsibly

## Development Workflow

### Creating a Feature

```bash
# Update develop branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/my-feature

# Make changes, test, and commit
git add .
git commit -m "feat: add my feature"

# Push to remote
git push origin feature/my-feature

# Create pull request on GitHub
```

### Local Testing Before Submission

```bash
# Run linter
flake8 .

# Format code
black .

# Run tests
pytest

# Check coverage
pytest --cov

# Type checking
mypy .
```

## Release Process

Releases follow semantic versioning: MAJOR.MINOR.PATCH

The maintainers handle releases, but contributors should be aware that:
- All merges to main are releases
- Updates to CHANGELOG.md are required
- Version bumping is handled automatically

## Community

### Communication Channels

- **Issues**: Bug reports and feature requests
- **Discussions**: Questions and ideas
- **Email**: dev@lamoda-recruiter.com

### Getting Help

- Check documentation first
- Search existing issues
- Ask in GitHub Discussions
- Contact maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in commit messages

## License

By contributing, you agree that your contributions will be licensed under the project's license.

## Questions?

Don't hesitate to:
- Create a GitHub Discussion
- Email: dev@lamoda-recruiter.com
- Check [FAQ.md](FAQ.md) for common questions

---

Thank you for contributing to making Lamoda AI Recruiter better!

*Last Updated: December 25, 2024*

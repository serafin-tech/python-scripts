# AI Rules for python-scripts repo

The code in this repo is source of simple Python scripts to be used while developing bigger projects. It contains simple command line (CLI) tools prepared as a Python package to be easily reused while setting up new projects.

## CODING_PRACTICES

### Guidelines for SUPPORT_LEVEL

#### SUPPORT_EXPERT

- Favor elegant, maintainable solutions over verbose code. Assume understanding of language idioms and design patterns.
- Highlight potential performance implications and optimization opportunities in suggested code.
- Frame solutions within broader architectural contexts and suggest design alternatives when appropriate.
- Focus comments on 'why' not 'what' - assume code readability through well-named functions and variables.
- Proactively address edge cases, race conditions, and security considerations without being prompted.
- When debugging, provide targeted diagnostic approaches rather than shotgun solutions.
- Suggest comprehensive testing strategies rather than just example tests, including considerations for mocking, test organization, and coverage.

### Guidelines for VERSION_CONTROL

#### GIT

- Use conventional commits to create meaningful commit messages
- Use feature branches with descriptive names
- Write meaningful commit messages that explain why changes were made, not just what
- Keep commits focused on single logical changes to facilitate code review and bisection
- Use interactive rebase to clean up history before merging feature branches
- Leverage git hooks to enforce code quality checks before commits and pushes

#### GITHUB

- Use pull request templates to standardize information provided for code reviews
- Implement branch protection rules for `main` branch to enforce quality checks
- Configure required status checks to prevent merging code that fails tests or linting
- Use GitHub Actions for CI/CD workflows to automate testing and deployment

### Guidelines for PYTHON

#### PYTHON_CODING_STANDARDS

- Follow PEP 8 style guide for Python code formatting and conventions
- Use type hints for all function signatures and class attributes for better code clarity and static analysis
- Implement docstrings for all public modules, classes, and functions using Google style
- Use f-strings for string formatting for better readability and performance
- F-strings to be constructed using double quotes (") unless single quotes (') are necessary to avoid escaping
- Leverage list comprehensions and generator expressions for concise and efficient data processing
- Use context managers (with statement) for resource management (files, database connections, etc.)
- Implement logging using the built-in logging module instead of print statements for better control over log output
- ensure no `__future__` imports are used in code
- Follow naming conventions: snake_case for functions and variables, PascalCase for classes
- Ensure import order follows standard library, third-party, and local imports separated by a blank line
- Prefer single quotes for string literals, unless double quotes are necessary to avoid escaping

### Guidelines for CONTAINERIZATION

#### DOCKER

- Use multi-stage builds to create smaller production images
- Implement layer caching strategies to speed up builds for {{dependency_types}}
- Use non-root users in containers for better security
- Leverage Docker Compose for local development environments with multiple services
- Use .dockerignore files to exclude unnecessary files from the build context

## TESTING

### Guidelines for UNIT

#### PYTEST

- Use fixtures for test setup and dependency injection
- Implement parameterized tests for testing multiple inputs for {{function_types}}
- Use monkeypatch for mocking dependencies

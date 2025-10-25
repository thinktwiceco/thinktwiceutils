[![thinktwiceutils CI/CD](https://github.com/thinktwiceco/thinktwiceutils/actions/workflows/ci.yml/badge.svg)](https://github.com/thinktwiceco/thinktwiceutils/actions/workflows/ci.yml)
[![Version Management](https://github.com/thinktwiceco/thinktwiceutils/actions/workflows/version.yml/badge.svg)](https://github.com/thinktwiceco/thinktwiceutils/actions/workflows/version.yml)

# thinktwiceutils

A collection of lightweight Python utilities for common development patterns.

## Installation

```bash
pip install thinktwiceutils
```

## Usage

```python
import ttutils
from ttutils import SR, SE
```

## Packages

### SimpleReturns

A typed result handling utility for clean error handling without exceptions.

**Key Features:**
- `SR` (SimpleResult): Type-safe success/error result wrapper
- `SE` (SimpleError): Structured error representation
- Chainable operations with railway-oriented programming pattern

**Example:**
```python
from ttutils import SR, SE

def divide(a: int, b: int) -> SR[float, str]:
    if b == 0:
        return SR.error("Division by zero")
    return SR.success(a / b)

result = divide(10, 2)
if result.is_success:
    print(f"Result: {result.value}")  # Result: 5.0
```

[Full Documentation](./src/ttutils/simplereturns/README.md)

### Dependencies

A lightweight dependency injection utility that wraps callables for easy testing and mocking.

**Key Features:**
- Wrap any callable (function, method) as a dependency
- Override dependencies in tests with context managers
- Automatic hash-based registration prevents duplicates
- Maintains original function signatures

**Example:**
```python
from ttutils.dependencies.dependencies import Dependency

# Define and wrap a function
def get_database_url() -> str:
    return "postgresql://prod-server/db"

db_url = Dependency(get_database_url)

# Use it normally
print(db_url())  # "postgresql://prod-server/db"

# Override in tests
def test_database_url():
    return "postgresql://test-server/db"

with db_url.override(test_database_url):
    print(db_url())  # "postgresql://test-server/db"

# Automatically restored after context
print(db_url())  # "postgresql://prod-server/db"
```

[Full Documentation](./src/ttutils/dependencies/README.md)
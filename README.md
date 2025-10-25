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

A lightweight dependency injection utility for managing service dependencies.

**Key Features:**
- Simple registration and resolution of dependencies
- Type-safe dependency injection
- Minimal boilerplate

**Example:**
```python
from ttutils.dependencies.dependencies import Dependency

# Register a service
Dependency.register("database", my_db_instance)

# Resolve it later
db = Dependency.resolve("database")
```

[Full Documentation](./src/ttutils/dependencies/README.md)
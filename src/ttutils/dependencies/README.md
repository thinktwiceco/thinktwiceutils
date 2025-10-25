# Dependencies

A lightweight dependency injection utility that wraps callables for easy testing and mocking.

## Overview

The `Dependency` class wraps any callable (function, method) and allows you to override its behavior in specific contexts, making it ideal for testing and dependency injection patterns.

## Basic Usage

```python
from ttutils.dependencies.dependencies import Dependency

# Wrap a function
def get_api_key() -> str:
    return "prod-api-key-12345"

api_key = Dependency(get_api_key)

# Call it like the original function
print(api_key())  # "prod-api-key-12345"
```

## Working with Arguments

Dependencies maintain the original function's signature:

```python
def calculate_discount(price: float, discount_pct: float) -> float:
    return price * (1 - discount_pct / 100)

calc_discount = Dependency(calculate_discount)

# Call with arguments
result = calc_discount(100.0, 10.0)  # 90.0
result = calc_discount(price=100.0, discount_pct=20.0)  # 80.0
```

## Testing with Overrides

The `override()` context manager allows temporary replacement for testing:

```python
def get_database_connection():
    return DatabaseConnection("prod-server")

db_conn = Dependency(get_database_connection)

# In your tests
def test_database_query():
    def mock_db_connection():
        return MockDatabaseConnection("test-server")
    
    with db_conn.override(mock_db_connection):
        # Inside this block, db_conn() returns the mock
        conn = db_conn()
        assert conn.server == "test-server"
    
    # Outside the block, original behavior is restored
    conn = db_conn()
    assert conn.server == "prod-server"
```

## Key Features

- **Automatic Registration**: Each function is automatically registered using a hash-based key
- **Duplicate Prevention**: Attempting to register the same function twice raises `ValueError`
- **Safe Overrides**: Overrides are automatically restored even if exceptions occur
- **Type Preservation**: Maintains original function signatures and type hints
- **Zero Configuration**: No manual registration or setup required

## Use Cases

1. **External Services**: Wrap API clients, database connections, or external services
2. **Configuration**: Encapsulate configuration access for easy testing
3. **Feature Flags**: Override feature flags in different test scenarios
4. **Time/Random**: Make non-deterministic functions testable

## Example: Real-World Usage

```python
from ttutils.dependencies.dependencies import Dependency

# Production code
def get_current_timestamp() -> float:
    import time
    return time.time()

timestamp = Dependency(get_current_timestamp)

def create_record(name: str) -> dict:
    return {
        "name": name,
        "created_at": timestamp()
    }

# Test code
def test_create_record():
    def fixed_timestamp() -> float:
        return 1234567890.0
    
    with timestamp.override(fixed_timestamp):
        record = create_record("test")
        assert record["created_at"] == 1234567890.0
```
"""Unit tests for dependencies package."""

import pytest

from thinktwiceutils.dependencies.dependencies import Dependency


def test_dependency_registration():
    """Test registering a simple dependency."""

    def my_function():
        return "original"

    dep = Dependency(my_function)
    assert dep() == "original"


def test_dependency_with_args():
    """Test dependency with arguments."""

    def add(a: int, b: int) -> int:
        return a + b

    dep = Dependency(add)
    assert dep(2, 3) == 5
    assert dep(10, 20) == 30


def test_dependency_with_kwargs():
    """Test dependency with keyword arguments."""

    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    dep = Dependency(greet)
    assert dep("World") == "Hello, World!"
    assert dep("Alice", greeting="Hi") == "Hi, Alice!"


def test_duplicate_dependency_raises_error():
    """Test that registering the same dependency twice raises an error."""

    def my_function():
        return "value"

    Dependency(my_function)

    with pytest.raises(ValueError, match="already exists"):
        Dependency(my_function)


def test_dependency_override():
    """Test overriding a dependency."""

    def original():
        return "original"

    def override_fn():
        return "overridden"

    dep = Dependency(original)
    assert dep() == "original"

    with dep.override(override_fn):
        assert dep() == "overridden"

    assert dep() == "original"


def test_dependency_override_with_args():
    """Test overriding a dependency that takes arguments."""

    def original(x: int) -> int:
        return x * 2

    def override_fn(x: int) -> int:
        return x * 3

    dep = Dependency(original)
    assert dep(5) == 10

    with dep.override(override_fn):
        assert dep(5) == 15

    assert dep(5) == 10


def test_dependency_override_exception_handling():
    """Test that override restores original even on exception."""

    def original():
        return "original"

    def override_fn():
        return "overridden"

    dep = Dependency(original)

    try:
        with dep.override(override_fn):
            assert dep() == "overridden"
            raise RuntimeError("Test exception")
    except RuntimeError:
        pass

    assert dep() == "original"


def test_dependency_hash_uniqueness():
    """Test that different functions get different hashes."""

    def func1():
        return "func1"

    def func2():
        return "func2"

    dep1 = Dependency(func1)
    dep2 = Dependency(func2)

    assert dep1.key != dep2.key
    assert dep1() == "func1"
    assert dep2() == "func2"


def test_dependency_registry_isolation():
    """Test that each dependency has its own registry entry."""

    def func_a():
        return "A"

    def func_b():
        return "B"

    dep_a = Dependency(func_a)
    dep_b = Dependency(func_b)

    assert dep_a() == "A"
    assert dep_b() == "B"

    def override_a():
        return "A_override"

    with dep_a.override(override_a):
        assert dep_a() == "A_override"
        assert dep_b() == "B"

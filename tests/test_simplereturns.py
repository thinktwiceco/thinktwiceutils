"""Unit tests for simplereturns package."""

from ttutils import SE, SR


def test_sr_success_creation():
    """Test creating a success result."""
    result: SR[str, str] = SR.success("test_value")
    assert result.is_success
    assert not result.is_error
    assert result.value == "test_value"
    assert result.error_value is None


def test_sr_error_creation():
    """Test creating an error result."""
    result: SR[str, str] = SR.error("test_error")
    assert result.is_error
    assert not result.is_success
    assert result.error_value == "test_error"
    assert result.value is None


def test_sr_with_se():
    """Test SR with SE error type."""
    error = SE("Something went wrong", code="ERR001")
    result: SR[str, SE] = SR.error(error)
    assert result.is_error
    assert result.error_value == error
    assert result.error_value.message == "Something went wrong"
    assert result.error_value.code == "ERR001"


def test_se_basic():
    """Test SE basic initialization."""
    error = SE("Test error")
    assert error.message == "Test error"
    assert error.code is None
    assert error.context == {}


def test_se_with_code():
    """Test SE with error code."""
    error = SE("Test error", code="E001")
    assert error.message == "Test error"
    assert error.code == "E001"
    assert str(error) == "[E001] Test error"


def test_se_with_context():
    """Test SE with context."""
    context = {"user_id": 123, "action": "login"}
    error = SE("Test error", code="E001", context=context)
    assert error.context == context


def test_se_str_without_code():
    """Test SE string representation without code."""
    error = SE("Simple error")
    assert str(error) == "Simple error"


def test_se_repr():
    """Test SE repr."""
    error = SE("Test", code="E001", context={"key": "value"})
    assert repr(error) == "SE(message='Test', code='E001', context={'key': 'value'})"

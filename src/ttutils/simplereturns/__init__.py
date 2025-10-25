"""Simple typed result handling with SR (SimpleResult) and SE (SimpleError)."""


class SR[S, E]:
    """Generic result class that can represent either success or error.

    Type parameters:
        S: Success value type
        E: Error value type
    """

    def __init__(self, _success: bool, _value: S | None = None, _error: E | None = None) -> None:
        """Initialize SR. Use class methods success() or error() instead."""
        self._success = _success
        self._value = _value
        self._error = _error

    @classmethod
    def success(cls, value: S) -> "SR[S, E]":
        """Create a success result."""
        return cls(_success=True, _value=value)

    @classmethod
    def error(cls, error: E) -> "SR[S, E]":
        """Create an error result."""
        return cls(_success=False, _error=error)

    @property
    def is_success(self) -> bool:
        """Check if this is a success result."""
        return self._success

    @property
    def is_error(self) -> bool:
        """Check if this is an error result."""
        return not self._success

    @property
    def value(self) -> S | None:
        """Get the success value, or None if this is an error."""
        return self._value

    @property
    def error_value(self) -> E | None:
        """Get the error value, or None if this is a success."""
        return self._error


class SE:
    """Simple error wrapper for common error scenarios."""

    def __init__(self, message: str, code: str | None = None, context: dict | None = None) -> None:
        """Initialize a simple error.

        Args:
            message: Error message
            code: Optional error code
            context: Optional additional context
        """
        self.message = message
        self.code = code
        self.context = context or {}

    def __str__(self) -> str:
        """String representation of the error."""
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message

    def __repr__(self) -> str:
        """Detailed representation of the error."""
        return f"SE(message={self.message!r}, code={self.code!r}, context={self.context!r})"


__all__ = ["SR", "SE"]

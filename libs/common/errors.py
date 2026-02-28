class PanicError(Exception):
    """Base error type for scaffolded services."""


class ValidationError(PanicError):
    """Raised when contract or payload validation fails."""
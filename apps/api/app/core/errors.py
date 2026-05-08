class AppError(Exception):
    def __init__(self, code: str, message: str, suggestion: str | None = None):
        self.code = code
        self.message = message
        self.suggestion = suggestion
        super().__init__(message)


class ValidationError(AppError):
    def __init__(self, message: str, field: str | None = None):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            suggestion="Check the request body and try again.",
        )
        self.field = field


class EnhancementError(AppError):
    def __init__(self, message: str):
        super().__init__(
            code="ENHANCEMENT_FAILED",
            message=message,
            suggestion="Try rephrasing your description with more detail.",
        )


class GenerationError(AppError):
    def __init__(self, message: str):
        super().__init__(
            code="GENERATION_FAILED",
            message=message,
            suggestion="Try simplifying your description or selecting a specific diagram type.",
        )

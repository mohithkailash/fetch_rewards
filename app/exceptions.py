class ReceiptProcessorError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(ReceiptProcessorError):
    pass

class InvalidDateFormatError(ValidationError):
    def __init__(self, message="Invalid date format. Use YYYY-MM-DD"):
        super().__init__(message)

class InvalidTimeFormatError(ValidationError):
    def __init__(self, message="Invalid time format. Use HH:MM"):
        super().__init__(message)

class InvalidPriceFormatError(ValidationError):
    def __init__(self, message="Price must be a valid number"):
        super().__init__(message)

class MissingFieldError(ValidationError):
    def __init__(self, field):
        super().__init__(f"Missing required field: {field}")

class InvalidItemFormatError(ValidationError):
    def __init__(self, index, message):
        super().__init__(f"Item {index}: {message}")

class ReceiptNotFoundError(ReceiptProcessorError):
    def __init__(self):
        super().__init__("Receipt not found", status_code=404)

class InvalidJSONError(ReceiptProcessorError):
    def __init__(self):
        super().__init__("Invalid JSON format")
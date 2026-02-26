from frontpage.exceptions import DomainError


class SampleError(DomainError):
    pass


class SampleDiscardError(SampleError):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code

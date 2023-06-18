class SaladPyException(Exception):
    """
    General SaladPy exception.
    Packs together all the possible errors Salad API could give
    """

    def __init__(self, message: str) -> None:
        self.message = message

    def __repr__(self) -> str:
        return '<SaladPyException(message="{0}")>'.format(
            self.message
        )

class AlreadyLoggedIn(Exception):
    """
    Shown when the user *might* already be logged in.
    """
    
    def __init__(self, message: str) -> None:
        self.message = message

    def __repr__(self) -> str:
        return '<AlreadyLoggedIn(message="{0}")>'.format(
            self.message
        )
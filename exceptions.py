


class SearchPhraseEmptyException(Exception):
    """Exception raised when search_phrase is empty"""

    def __init__(self, search_phrase) -> None:
        message:str  = f"'search_phrase' is empty -- {search_phrase}"
        super().__init__(message)


class NumberOfMonthsEmptyException(Exception):
    """Exception raised when number_of_months is empty"""

    def __init__(self, number_of_months) -> None:
        message:str  = f"'number_of_months' is empty -- {number_of_months}"
        super().__init__(message)

class NumberOfMonthsInvalidTypeException(Exception):
    """Exception raised when number_of_months is invalid e.g not a numeral"""

    def __init__(self, number_of_months) -> None:
        message:str  = f"'number_of_months' is not a numeral -- {number_of_months}"
        super().__init__(message)

class NumberOfMonthsInvalidValueTypeException(Exception):
    """Exception raised when number_of_months is less than 0"""

    def __init__(self, number_of_months) -> None:
        message:str  = f"'number_of_months' is less than 0 -- {number_of_months}"
        super().__init__(message)
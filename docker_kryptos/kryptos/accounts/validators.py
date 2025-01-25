from rest_framework.exceptions import ValidationError

from tools.regex import (REGEX_PASSWORD_DIGIT,
                         REGEX_PASSWORD_UPPER,
                         REGEX_PASSWORD_LOWER,
                         REGEX_PASSWORD_SPECIAL,
                         regex_search,)


MSG_PASSWORD_MINIMUM = "Password must be more than 8 characters."
MSG_PASSWORD_NUMERIC = "Password must contain at least 1 digit."
MSG_PASSWORD_UPPER = "Password must contain at least one upper character."
MSG_PASSWORD_LOWER = "Password must contain at least one lower character."
MSG_PASSWORD_SPECIAL = "Password must contain at least one special character."
MSG_PASSWORD_SIMILARITY = "Password should not be similar with an email."
MSG_IPV4_ADDRESS = "Not a IP version 4 Format."


class SimilarityPasswordValidator:
    def __init__(self, similarity=0.2):
        self.similarity: float = similarity


    def validate(self, password, user=None) -> None:
        user: str = user.lower()
        password: str = password.lower()

        idx_number: int = len(user) if len(user) < len(password) else len(password)
        same_char: int = 0
        for idx in range(idx_number):
            if user[idx] == password[idx]:
                same_char += 1

        similarity_ratio = float(same_char/len(user))
        if similarity_ratio > self.similarity:
            raise ValidationError(MSG_PASSWORD_SIMILARITY,
                                  code=MSG_PASSWORD_SIMILARITY)

        return None


    def get_help_text(self) -> str:
        return MSG_PASSWORD_SIMILARITY


class MinimumLengthPasswordValidator:
    def __init__(self, min_length=8):
        self.min_length= min_length


    def validate(self, password, user=None) -> None:
        if len(password) < self.min_length:
            raise ValidationError(MSG_PASSWORD_MINIMUM,
                                  code=MSG_PASSWORD_MINIMUM)

        return None


    def get_help_text(self) -> str:
        return MSG_PASSWORD_MINIMUM


class NumericPasswordValidator:

    def validate(self, password, user=None) -> None:
        if regex_search(pattern=REGEX_PASSWORD_DIGIT, string=password) is None:
            raise ValidationError(MSG_PASSWORD_NUMERIC,
                                  code=MSG_PASSWORD_NUMERIC)

        return None


    def get_help_text(self) -> str:
        return MSG_PASSWORD_NUMERIC


class UpperPasswordValidator:

    def validate(self, password, user=None) -> None:
        if not regex_search(pattern=REGEX_PASSWORD_UPPER, string=password):
            raise ValidationError(MSG_PASSWORD_UPPER,
                                  code=MSG_PASSWORD_UPPER)

        return None


    def get_help_text(self) -> str:
        return MSG_PASSWORD_UPPER


class LowerPasswordValidator:
    def __init__(self):
        self.MESSAGE = "Password must contain at least one lower character."


    def validate(self, password, user=None) -> None:
        if not regex_search(pattern=REGEX_PASSWORD_LOWER, string=password):
            raise ValidationError(MSG_PASSWORD_LOWER,
                                  code=MSG_PASSWORD_LOWER)

        return None


    def get_help_text(self) -> str:
        return MSG_PASSWORD_LOWER


class SpecialPasswordValidator:

    def validate(self, password, user=None) -> None:
        if not regex_search(pattern=REGEX_PASSWORD_SPECIAL, string=password):
            raise ValidationError(MSG_PASSWORD_SPECIAL,
                                  code=MSG_PASSWORD_SPECIAL)

        return None


    def get_help_text(self) -> str:
        return MSG_PASSWORD_SPECIAL

from uuid import uuid4
import mongoengine as mg


from tools.clk import CLK
from tools.datetime import EPOCH_DATETIME, datetime
from tools.regex import (REGEX_URL_BODY,
                         REGEX_PASSWORD_UPPER,
                         REGEX_PASSWORD_LOWER,
                         REGEX_PASSWORD_SPECIAL,
                         REGEX_PASSWORD_DIGIT,
                         regex_search)


TUPLE_PROTOCOLS_CHOICE: tuple = (
    ("https", "HTTPS"),
    ("http", "HTTP"),
    ("ftp", "FTP"),
    ("jdbc", "Java DB Connect"),
    ("ssh", "SSH"),
    ("srv", "SRV"),
)


class Documents(mg.Document):
    uuid = mg.UUIDField(primary_key=True, required=True ,binary=False, default=uuid4)
    account = mg.UUIDField(required=True, binary=False)
    site = mg.StringField(required=True, max_length=64, regex=REGEX_URL_BODY)
    protocol = mg.StringField(required=True, min_length=3, max_length=5, choices=TUPLE_PROTOCOLS_CHOICE, default="https")
    username = mg.StringField(required=True, min_length=2, max_length=32, regex=r"^[\w@._-]+$")
    password = mg.StringField(required=True, min_length=4, max_length=256)
    description = mg.StringField(required=False, max_length=128, default="")

    is_length_violate = mg.BooleanField(required=True, default=False)
    is_lower_violate = mg.BooleanField(required=True, default=False)
    is_upper_violate = mg.BooleanField(required=True, default=False)
    is_special_violate = mg.BooleanField(required=True, default=False)
    is_digit_violate = mg.BooleanField(required=True, default=False)
    last_updated_datetime = mg.DateTimeField(default=EPOCH_DATETIME)
    registered_datetime = mg.DateTimeField(default=EPOCH_DATETIME)


    def __str__(self) -> str:
        return str(self.uuid)


    def check_password(self, **kwargs) -> bool:
        code: str | None = kwargs.get("code", None)
        password: str | None = kwargs.get("password", None)

        if code is None or password is None:
            return False

        return CLK(codebook=code, string=self.password).get_result() == password


    def get_res_data(self, extract_fields=None):
        res_data: dict = self.to_mongo(fields=extract_fields).to_dict()
        return res_data


    def __make_password(self, code) -> None:
        if len(self.password) != 256:
            self.is_length_violate = not len(self.password) >= 8
            self.is_upper_violate = not regex_search(pattern=REGEX_PASSWORD_UPPER, string=self.password)
            self.is_lower_violate = not regex_search(pattern=REGEX_PASSWORD_LOWER, string=self.password)
            self.is_digit_violate = not regex_search(pattern=REGEX_PASSWORD_DIGIT, string=self.password)
            self.is_special_violate = not regex_search(pattern=REGEX_PASSWORD_SPECIAL, string=self.password)
            self.password = CLK(codebook=code, string=self.password).get_result()
        return None


    def modify(self, *args, **kwargs) -> None:
        kwargs.update({"last_updated_datetime": datetime.now()})
        super(Documents, self).modify(*args, **kwargs)
        return None


    def save(self, *args, **kwargs) -> None:
        code = kwargs.pop("code", None)

        if self.registered_datetime == EPOCH_DATETIME:
            self.registered_datetime = datetime.now()

        self.__make_password(code=code)
        super(Documents, self).save(*args, **kwargs)
        return None

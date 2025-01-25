from datetime import (datetime,
                      timedelta,)


EPOCH_STRING: str = "1970-01-01T00:00:00.00000"
EPOCH_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%f"
EPOCH_DATETIME: datetime= datetime.strptime(EPOCH_STRING, EPOCH_FORMAT)
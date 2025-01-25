import re


REGEX_EMAIL = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
REGEX_PASSWORD_DIGIT = re.compile(r"[0-9]+")
REGEX_PASSWORD_UPPER = re.compile(r"[A-Z]+")
REGEX_PASSWORD_LOWER = re.compile(r"[a-z]+")
REGEX_PASSWORD_SPECIAL = re.compile(r"[!@#$%^&*(),.?\":{}|<>_\-]+")
REGEX_IPV4 = re.compile(r"^(?P<octet1>\d{1,3})\.(?P<octet2>\d{1,3})\.(?P<octet3>\d{1,3})\.(?P<octet4>\d{1,3})$")
REGEX_IPV4_PREFIX = re.compile(r"^(?P<octet1>\d{1,3})\.(?P<octet2>\d{1,3})\.(?P<octet3>\d{1,3})\.(?P<octet4>\d{1,3})/(?P<prefix>\d{1,2})$")
REGEX_URL_BODY = re.compile(r"^([A-z0-9_\-]+\.){1,3}[A-z0-9_\-]+(:\d{4,5})?$")
REGEX_UUID = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


def regex_search(pattern: re.compile, string: str):
    return re.search(pattern=pattern, string=string)


def regex_match(pattern: re.compile, string: str):
    return re.match(pattern=pattern, string=string)


def is_ipv4(ipv4: str):
    result = regex_match(pattern=REGEX_IPV4, string=ipv4)
    result = regex_match(pattern=REGEX_IPV4_PREFIX, string=ipv4) if result is None else result

    if ipv4 == "*" or "0.0.0.0" in ipv4:
        return "*"

    if result is not None:
        groups: tuple = result.groups()
        octet1: int = int(groups[0])
        octet2: int = int(groups[1])
        octet3: int = int(groups[2])
        octet4: int = int(groups[3])
        octet5: int = int(groups[4]) if len(groups) == 5 else None

        if 0 < octet1 <= 255 and 0 <= octet2 <= 255 and 0 <= octet3 <= 255 and  0 <= octet4 <= 255:
            if octet5 is None:
                if octet4 == 0:
                    if octet3 == 0:
                        if octet2 == 0:
                            octet5 = 8
                        else:
                            octet5 = 16
                    else:
                        octet5 = 24
                else:
                    octet5 = 32

            new_ip: str = f"{octet1}.{octet2}.{octet3}.{octet4}/{octet5}"
            if new_ip != "255.255.255.255/32":
                return new_ip

    return None
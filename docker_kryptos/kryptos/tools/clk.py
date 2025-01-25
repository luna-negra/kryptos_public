"""
WARNING: this file is only allowed to be used in private use.

[ clk.py ]
Beta
Version 0.1.1 : Initial version for test
Version 0.2.1 : Convert to class version to embed in the application.
                Will reflect a some of new password policies published on 2024.09
                Change the location of some keys and validator
Version 0.3.1 : Edit the logic to use CLK Class.
                Get rid of the codebook in encrypted string. User must create own Codebook and put it as an arguments.
                ex: Codebook in DB -> call Codebook from DB -> Calculate
"""


from random import randint, shuffle
from base64 import b64decode, b64encode


class Codebook:

    @staticmethod
    def generate() -> str:
        u_latin: list = [chr(n) for n in list(range(65, 91))]
        l_latin: list = [chr(n) for n in list(range(97, 123))]
        others: list = [chr(n) for n in list(range(48, 58))] + ["="]
        codebook: list = u_latin + l_latin + others
        shuffle(codebook)
        result: str = ""
        for a in codebook:result += a
        return result


    @staticmethod
    def validate(codebook: str) -> bool:
        condition1: bool = len(codebook) != 63
        condition2: bool = any([chr(a) not in codebook for a in range(65, 91)])
        condition3: bool = any([chr(a) not in codebook for a in range(97, 123)])
        condition4: bool = any([chr(a) not in codebook for a in range(48, 58)])
        condition5: bool = '=' not in codebook
        if condition1 and condition2 and condition3 and condition4 and condition5:
            raise ValueError("[CLK] Not a valid CLK codebook. Please check that whether there is any damage on your codebook or not.")
        return True


class CLK:
    def __init__(self,
                 codebook: str,
                 string: str,
                 enc_type: int = 256):
        self.__VERSION: str = "2024.0.3.1"
        self.__CODE: str = codebook
        self.__STRING: str = string
        self.__ENC_TYPE: int = len(self.__STRING) if len(self.__STRING) in (256, 512) else enc_type
        self.__ENCODING = "utf-8"
        self.__ERRMSG: str = "[CLK ERROR] This is not a CLK encrypted string."
        self.__CODE_SPLIT_NUMBER: int = int(len(self.__CODE) / 10)
        self.__LEN_MIN_PSTR: int = 4
        self.__LEN_MAX_PSTR: int = 64
        self.__LOC_KEY1 = 11
        self.__LOC_KEY2 = 24
        self.__LOC_KEY3 = 36
        self.__LOC_KEY4 = self.__ENC_TYPE - 20
        self.__LOC_KEY5 = 45
        self.__LOC_START_ECORE = 50
        self.__LOC_LIMIT_ECORE = self.__LOC_KEY4 - 100
        self.__LOC_ECORE = 0
        self.__prime_nums: list = self.__get_prime_nums()
        self.__CLK_TAG: str = "CLK==="
        self.__B64_STRING: str = ""
        self.__RESULT: str = ""
        if len(string) not in (256, 512):
            self.encrypt()
        else:
            self.decrypt()


    def __decrypt(self) -> str:
        key1: str = self.__STRING[self.__LOC_KEY1: self.__LOC_KEY1 + 3]
        key2: str = self.__STRING[self.__LOC_KEY2: self.__LOC_KEY2 + 3]
        key3: str = self.__STRING[self.__LOC_KEY3: self.__LOC_KEY3 + 3]
        key4: str = self.__STRING[self.__LOC_KEY4: self.__LOC_KEY4 + 5]
        key5: str = self.__STRING[self.__LOC_KEY5: self.__LOC_KEY5 + 3]
        str_key1: str = "".join([str(int(self.__CODE.index(c) / self.__CODE_SPLIT_NUMBER)) for c in key1])
        str_key2: str = "".join([str(int(self.__CODE.index(c) / self.__CODE_SPLIT_NUMBER)) for c in key2])
        str_key3: str = "".join([str(int(self.__CODE.index(c) / self.__CODE_SPLIT_NUMBER)) for c in key3])
        str_key4: str = "".join([str(int(self.__CODE.index(c) / self.__CODE_SPLIT_NUMBER)) for c in key4])
        str_key5: str = "".join([str(int(self.__CODE.index(c) / self.__CODE_SPLIT_NUMBER)) for c in key5])
        validator: str = f"{key1}{key4}{key2}"
        condition1 = int(str_key1) * int(str_key2) != int(str_key4)
        condition2 = abs(int(str_key1) - int(str_key2)) not in range(self.__LOC_START_ECORE + 1, self.__LOC_LIMIT_ECORE)

        if condition1 or condition2:
            return self.__ERRMSG
        str_validator: str = f"{str_key1}{str_key4}{str_key2}"
        loc_core: int = abs(int(str_key1) - int(str_key2))
        enc_core: str = self.__STRING[loc_core: loc_core + int(str_key3)]
        tmp_b64_str: str = self.__dec_mapper(validator=validator, core_string=enc_core)
        tmp_str: str = b64decode(tmp_b64_str.encode(self.__ENCODING)).decode(self.__ENCODING)
        if tmp_str == "" or len(tmp_str) != int(str_key5):
            return self.__ERRMSG
        return tmp_str

    def __dec_mapper(self, validator: str, core_string: str) -> str:
        e_to_p: str = ""
        validator = "".join([str(int(self.__CODE.index(n) / self.__CODE_SPLIT_NUMBER)) for n in validator])
        validator_reassemble = [validator[c] + validator[(c + 1) % len(validator)] for c in range(0, len(validator))]
        count = 0
        for c in core_string:
            index = (self.__CODE.index(c) - int(validator_reassemble[count % len(validator)])) - int(count / len(validator))
            e_to_p += self.__CODE[index % len(self.__CODE)]
            count += 1
        if e_to_p.startswith(self.__CLK_TAG):
            return e_to_p.replace(self.__CLK_TAG, "")
        return ""

    def __encrypt(self) -> str:
        while True:
            key1: int = self.__prime_nums[randint(0, len(self.__prime_nums) - 1)]
            key2: int = self.__prime_nums[randint(0, len(self.__prime_nums) - 1)]
            key3: int = len(self.__B64_STRING) + len(self.__CLK_TAG)
            key4: int = key1 * key2
            key5: int = len(self.__STRING)
            diff: int = abs(key2 - key1)
            if self.__LOC_START_ECORE < diff < self.__LOC_LIMIT_ECORE - len(self.__STRING) and key4 > 1000:
                self.__LOC_ECORE = diff
                break
        key1: str = "{:03d}".format(key1)
        key2: str = "{:03d}".format(key2)
        key3: str = "{:03d}".format(key3)
        key4: str = "{:05d}".format(key4)
        key5: str = "{:03d}".format(key5)
        code = self.__gen_code()
        str_key1 = "".join([code[c][randint(0, len(code[c]) - 1)] for c in key1])
        str_key2 = "".join([code[c][randint(0, len(code[c]) - 1)] for c in key2])
        str_key3 = "".join([code[c][randint(0, len(code[c]) - 1)] for c in key3])
        str_key4 = "".join([code[c][randint(0, len(code[c]) - 1)] for c in key4])
        str_key5 = "".join([code[c][randint(0, len(code[c]) - 1)] for c in key5])
        validator = key1 + key4 + key2
        ecore = self.__enc_mapper(validator=validator)
        enc_str: tuple = (self.__get_random_str(length=11),
                         str_key1,
                         self.__get_random_str(length=self.__LOC_KEY2 - self.__LOC_KEY1 - len(str_key1)),
                         str_key2,
                         self.__get_random_str(length=self.__LOC_KEY3 - self.__LOC_KEY2 - len(str_key2)),
                         str_key3,
                         self.__get_random_str(length=self.__LOC_KEY5 - self.__LOC_KEY3 - len(str_key3)),
                         str_key5,
                         self.__get_random_str(length=self.__LOC_ECORE - self.__LOC_KEY5 - len(str_key5)),
                         ecore,
                         self.__get_random_str(length=self.__LOC_KEY4 - self.__LOC_ECORE - len(ecore)),
                         str_key4,
                         self.__get_random_str(length=self.__ENC_TYPE - self.__LOC_KEY4 - len(str_key4))
                          )

        return "".join(enc_str)


    def __enc_mapper(self, validator: str) -> str:
        p_to_e: str = ""
        code_list: list = list(self.__CODE)
        validator_reassemble = [validator[c] + validator[(c + 1) % len(validator)] for c in range(0, len(validator))]
        count = 0
        for c in self.__CLK_TAG + self.__B64_STRING:
            index = (code_list.index(c) + int(validator_reassemble[count % len(validator)])) + int(count / len(validator))
            p_to_e += code_list[index % len(code_list)]
            count += 1
        return p_to_e


    def __gen_code(self) -> dict:
        result: dict = {}
        for n in range(0, len(self.__CODE), self.__CODE_SPLIT_NUMBER):
            result[str(int(n / self.__CODE_SPLIT_NUMBER))] = self.__CODE[n: n + self.__CODE_SPLIT_NUMBER]

        return result


    def __get_prime_nums(self, max_num=315) -> list:
        prime_nums = [2]
        def check_prime(a: int):
            flag: bool = True
            for pn in prime_nums:
                if a % pn == 0:
                    flag = False
                    break
            if flag: prime_nums.append(a)
        list(map(check_prime, range(3, max_num)))
        return prime_nums


    def __get_random_str(self, length: int) -> str:
        result = ""
        for n in range(length):result += self.__CODE[randint(0, len(self.__CODE) - 1)]
        return result


    def decrypt(self) -> None:
        self.__RESULT = self.__decrypt()
        return None


    def encrypt(self) -> None:
        self.__B64_STRING: str = b64encode(self.__STRING.encode(self.__ENCODING)).decode(self.__ENCODING)
        if self.__ENC_TYPE not in (256, 512): raise ValueError("[CLK Warning] CLK only support 256 and 512 type.")
        if self.__LEN_MIN_PSTR > len(self.__STRING) or len(self.__STRING) > self.__LEN_MAX_PSTR:
            raise ValueError(f"[CLK Warning] Plain string must be {self.__LEN_MIN_PSTR} ~ {self.__LEN_MAX_PSTR} in length ")
        self.__RESULT: str = self.__encrypt()
        return None


    def get_result(self) -> str:
        return self.__RESULT

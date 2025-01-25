

def apply_asterisk(string:str, visibility:float=0.3):
    add_flag: bool = False
    len_string: int = len(string)
    middle_index = int(len_string / 2) if len_string % 2 == 0 else int((len_string / 2) + 1)
    asterisk_number: int = int(round(len_string * (1 - visibility)) / 2)

    pre_string: list = list(string[:middle_index])
    post_string: list = list(string[middle_index:])
    pre_string.reverse()

    if len(pre_string) != len(post_string):
        pre_string.pop(0)
        add_flag = True

    for n in range(asterisk_number):
        pre_string[n] = "*"
        post_string[n] = "*"

    pre_string.reverse()
    return "".join(pre_string) + ("*" if add_flag else "") + "".join(post_string)

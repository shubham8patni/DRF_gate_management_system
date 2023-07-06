import random

def aadharNumVerify(adharNum: str) -> bool:
    """
    Takes a N digit aadhar number and
    returns a boolean value whether that is Correct or Not
    """
    verhoeff_table_d = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
        (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
        (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
        (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
        (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
        (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
        (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
        (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
        (9, 8, 7, 6, 5, 4, 3, 2, 1, 0))

    verhoeff_table_p = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
        (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
        (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
        (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
        (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
        (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
        (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))

    # verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

    def checksum(s: str) -> int:
        """For a given number generates a Verhoeff digit and
        returns number + digit"""
        c = 0
        for i, item in enumerate(reversed(s)):
            c = verhoeff_table_d[c][verhoeff_table_p[i % 8][int(item)]]
        return c

    # Validate Verhoeff checksum
    return checksum(adharNum) == 0 and len(adharNum) == 12


def password_generate(phone_number, first_name):
    jumbled_string = ""

    for i in range(len(first_name)):
        if i % 2 == 1:
            jumbled_string += phone_number[i]
        else:
            jumbled_string += first_name[i]
    
    shuffled_characters = []
    for character in jumbled_string:
        random_index = random.randint(0, len(shuffled_characters))
        shuffled_characters.insert(random_index, character)

    shuffled_string = "".join(shuffled_characters)


    if len(shuffled_string) > 10:
        shuffled_string = shuffled_string[0:9]
    return shuffled_string
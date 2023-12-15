def number_to_letters(number):
    if number <= 0:
        return ""

    result = ""
    while number > 0:
        remainder = (number - 1) % 26
        result = chr(ord('A') + remainder) + result
        number = (number - 1) // 26

    return result
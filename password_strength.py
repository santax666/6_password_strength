import datetime
import re
import sys
import math
import argparse


def has_bad_pass(value):
    top25pass = ['123456', 'password', '12345678', 'qwerty', '12345',
                 '123456789', 'football', '1234', '1234567', 'baseball',
                 'welcome', '1234567890', 'abc123', '111111', '1qaz2wsx',
                 'dragon', 'master', 'monkey', 'letmein', 'login',
                 'princess', 'qwertyuiop', 'solo', 'passw0rd', 'starwars']
    return value in top25pass


def has_digit(value):
    return bool(re.search(r'\d', value))


def has_letter(value):
    return bool(re.search(r'[А-Яа-яA-Za-zЁё]', value))


def has_low_letter(value):
    return bool(re.search(r'[а-яa-zё]', value))


def has_up_letter(value):
    return bool(re.search(r'[А-ЯA-ZЁ]', value))


def has_spec_char(value):
    return bool(re.search(r'[^А-Яа-яA-Za-zЁё0-9]', value))


def str_to_date(value):
    date_value = None
    date_formats = ['%Y%m%d', '%d%m%Y', '%Y.%m.%d', '%d.%m.%Y',
                    '%Y/%m/%d', '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']
    if (len(value) == 8 or len(value) == 10):
        for date_fmt in date_formats:
            try:
                date_value = datetime.datetime.strptime(value, date_fmt).date()
            except ValueError:
                pass
    return date_value


def has_calendar_date(value):
    return not bool(str_to_date(value))


def has_phone_number(value):
    if (re.match(r'[8]{1}[9]{1}[0-9]{9}', value) and len(value)) == 11:
        return False
    elif (re.match(r'[+]{1}[7]{1}[9]{1}[0-9]{9}', value) and len(value)) == 12:
        return False
    else:
        return True

def get_bit_resistance(value):
    sum_array = (((has_digit(value) + has_letter(value)) +
                (has_low_letter(value) + has_up_letter(value))) +
                ((has_spec_char(value) + has_calendar_date(value)) +
                has_phone_number(value)))
    length = len(value)
    bit_resist = math.log(sum_array) * (length / math.log(2))
    return bit_resist


def get_password_strength(value):
    if has_bad_pass(value):
        password_score = 1
    else:
        bit_resist = get_bit_resistance(value)
        password_score = math.ceil(bit_resist / 9)
    return password_score


def createParser():
    parser = argparse.ArgumentParser(usage='%(prog)s [аргументы]',
                                     description="Оценка сложности пароля"
                                                 " с помощью %(prog)s")
    parser.add_argument("password", nargs='?', help="пароль для оценки")
    return parser



if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    password = namespace.password

    if not password:
        password = input('Пожалуйста, введите пароль для оценки: ')
    password_score = get_password_strength(password)
    print('По 10-бальной шкале вашему паролю дана оценка:', password_score)

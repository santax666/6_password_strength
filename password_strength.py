import datetime
import re
import sys


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
    return bool(str_to_date(value))


def has_phone_number(value):
    if (re.match(r'[8]{1}[9]{1}[0-9]{9}', value) and len(value)) == 11:
        return True
    elif (re.match(r'[+]{1}[7]{1}[9]{1}[0-9]{9}', value) and len(value)) == 12:
        return True
    else:
        return False


def get_password_strength(value):
    if has_bad_pass(value):
        password_score = 1
    else:
        if (has_digit(value) and has_letter(value) and
                has_spec_char(value)):
            password_score = 10
        elif (not has_digit(value) and has_letter(value) and
              has_spec_char(value)):
            password_score = 9
        elif (has_digit(value) and not has_letter(value) and
              has_spec_char(value) and not has_calendar_date(value) and
              not has_phone_number(value)):
            password_score = 8
        elif (has_digit(value) and has_letter(value) and
              not has_spec_char(value)):
            password_score = 7
        elif (not has_digit(value) and not has_letter(value) and
              has_spec_char(value)):
            password_score = 6
        elif (not has_digit(value) and has_letter(value) and
              not has_spec_char(value)):
            if (has_low_letter(value) and has_up_letter(value)):
                password_score = 5
            else:
                password_score = 4
        else:
            if not (has_calendar_date(value) or has_phone_number(value)):
                password_score = 3
            else:
                password_score = 2
        if 3 < len(value) < 8:
            password_score = round(password_score / 2 + 0.1)
        elif len(value) < 4:
            password_score = round(password_score / 4 + 0.1)
    print('По 10-бальной шкале вашему паролю дана оценка:', password_score)


if __name__ == '__main__':
    print(True + True + True)

#    print(bool(re.search(r'\d', '567hghgh')))

"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print('Скрипт просит ввести пароль и выдает ему оценку от 1 до 10')
            print('Пароль можно указать аргументом в командной строке.')
            print('')
            print('Введите в терминале: python3.5 password_strength.py')
            print('или же')
            print('Введите в терминале: python3.5 password_strength.py pass')
        else:
            get_password_strength(sys.argv[1])
    else:
        password = input('Пожалуйста, введите пароль для оценки: ')
        get_password_strength(password)
"""
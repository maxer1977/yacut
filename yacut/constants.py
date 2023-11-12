import string

# Максимальная длина автоссылки
LINK_LEN = 6

# Список возможных символов и цифр для авто-ссылки
STRING_FOR_LINK = string.ascii_letters + string.digits

# Шаблон для проверки короткой ссылки
MATCH_SHORT_LINK = "^$|^[a-zA-Z0-9]*$"

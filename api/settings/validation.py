def validate_phone_number(value: str) -> str:
    if len(value) != 11:
        raise ValueError("Телефонный номер должен состоять из 11 цифр")
    if not value.startswith('8'):
        raise ValueError("Телефонный номер должен начинаться с 8")
    return value
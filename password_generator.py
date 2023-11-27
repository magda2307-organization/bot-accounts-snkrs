import random
import string

def generate_random_password(length=12, use_numbers=True, use_special_chars=True):
    characters = string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

import random
import string

def generate_random_key(length=30):
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for _ in range(length))
    return key

random_key = generate_random_key()
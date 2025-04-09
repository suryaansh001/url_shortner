import random
import string




def generate_short_code(length=7):
    characters = string.ascii_letters + string.digits 
    short_code = ''.join(random.choice(characters) for _ in range(length))
    return short_code
# print(generate_short_code())
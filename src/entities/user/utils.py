import random


def generate_verification_code(length=6) -> str:
    code = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return code

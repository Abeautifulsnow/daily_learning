# 在有django支持的时候，直接用这个方法
'''
from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
print(secret_key)
'''


# 在没有django的情况下，用这个生成方式
import random
def get_random_secret_key(length=50):
    """
    Return a 50 character random string usable as a SECRET_KEY setting value.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = ''.join(random.choice(chars) for i in range(length))
    return secret_key

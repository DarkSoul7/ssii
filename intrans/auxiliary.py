# -*- coding: utf-8 -*-
import random
import string


def generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

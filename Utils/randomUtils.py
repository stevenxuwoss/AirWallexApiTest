# encoding : utf-8
# @Author  : Steven Xu
# @Email   ：youzi5201@163.com

import random, string

class RandomUtils():

    def genRandomString(slen=10):
        return ''.join(random.sample(string.ascii_letters + string.digits, slen))

    def genRandomDigits(slen=10):
        return ''.join(str(random.choice(range(10))) for _ in range(slen)) 
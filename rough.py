from random import randint

def random_number():
    num=0
    for i in range(5):
        num = num*10 + randint(1,9)
    return num

print(random_number())